from kafka import KafkaConsumer, KafkaProducer
import json
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from logger_config import setup_logger

class ModelTrainer:
    def __init__(self, bootstrap_servers):
        self.logger = setup_logger('ModelTrainer')
        self.bootstrap_servers = bootstrap_servers
        self.consumer = KafkaConsumer(
            'training-data',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
    def prepare_data(self, data):
        features = np.array([[
            d['current_over'],
            d['current_score'],
            d['wickets'],
            d['run_rate'],
            d['batting_strength'],
            d['pitch_condition']
        ] for d in data])
        
        labels = np.array([d['final_score'] for d in data])
        return features, labels
        
    def train_model(self):
        self.logger.info("Starting model training...")
        training_data = []
        
        # Collect training data
        for message in self.consumer:
            print("recieved: ", message.value)
            training_data.append(message.value)
            if len(training_data) >= 1000:  # Collect 1000 samples
                break
                
        if not training_data:
            self.logger.error("No training data received!")
            return
            
        self.logger.info(f"Collected {len(training_data)} training samples")
        
        # Prepare data
        X, y = self.prepare_data(training_data)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        self.logger.info(f"Model Training Complete - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
        # Save model and scaler
        with open('cricket_model.pkl', 'wb') as f:
            pickle.dump((model, scaler), f)
        
        self.producer.send('model-status', {
            'status': 'TRAINING_COMPLETE',
            'metrics': {
                'train_score': train_score,
                'test_score': test_score
            }
        })
        
        return model, scaler

import os
if __name__=='__main__':
    BOOTSTRAP_SERVERS = [os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')]
    trainer = ModelTrainer(BOOTSTRAP_SERVERS)
    trainer.train_model()
