from kafka import KafkaConsumer, KafkaProducer
import json
import pickle
import numpy as np
from logger_config import setup_logger

class ScorePredictor:
    def __init__(self, bootstrap_servers):
        self.logger = setup_logger('ScorePredictor')
        self.consumer = KafkaConsumer(
            'match-events',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.model_loaded=False
            
    def predict(self, match_state):
        features = np.array([[
            match_state['current_over'],
            match_state['current_score'],
            match_state['wickets'],
            match_state['run_rate'],
            match_state['batting_strength'],
            match_state['pitch_condition']
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return round(prediction)

    def load_model(self):
        # Load model
        try:
            with open('cricket_model.pkl', 'rb') as f:
                self.model, self.scaler = pickle.load(f)
            self.logger.info("Model loaded successfully")
            self.model_loaded=True
        except FileNotFoundError:
            self.logger.error("Model file not found! Please train the model first.")
            raise


    def start(self):
        self.logger.info("Score predictor started. Waiting for match events...")
        for message in self.consumer:
            if not self.model_loaded:
                self.load_model()
            match_state = message.value
            predicted_score = self.predict(match_state)
            
            self.logger.info(
                f"Current: {match_state['current_score']}/{match_state['wickets']} "
                f"({match_state['current_over']} overs) - "
                f"Predicted Final Score: {predicted_score}"
            )
            
            self.producer.send('predictions', {
                'match_state': match_state,
                'predicted_score': predicted_score
            })

import os
if __name__=='__main__':
    BOOTSTRAP_SERVERS = [os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')]
    predictor = ScorePredictor(BOOTSTRAP_SERVERS)
    predictor.start()