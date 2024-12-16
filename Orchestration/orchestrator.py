from kafka import KafkaProducer
import json
import time
from data_generator import generate_cricket_data
from logger_config import setup_logger
import random

class MatchOrchestrator:
    def __init__(self, bootstrap_servers):
        self.logger = setup_logger('MatchOrchestrator')
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
    def start_training(self):
        self.logger.info("Generating and sending training data...")
        training_data = generate_cricket_data(1000)
        
        for data_point in training_data:
            print("Sending: ", data_point)
            self.producer.send('training-data', data_point)
        self.producer.flush()
        
        self.logger.info("Training data sent. Initiating model training...")
        
    def simulate_match(self, batting_strength=0.8, pitch_condition=0.85):
        self.logger.info("Starting match simulation...")
        current_score = 0
        wickets = 0
        
        for over in range(1, 21):
            for ball in range(1, 7):
                current_over = over + (ball - 1) / 6
                run_rate = current_score / current_over if current_over > 0 else 0
                
                match_state = {
                    'current_over': round(current_over, 1),
                    'current_score': current_score,
                    'wickets': wickets,
                    'run_rate': round(run_rate, 2),
                    'batting_strength': batting_strength,
                    'pitch_condition': pitch_condition
                }
                
                self.producer.send('match-events', match_state)
                
                # Simulate runs for this ball
                if wickets < 10:
                    runs = round(batting_strength * pitch_condition * random.uniform(0, 6))
                    wicket_probability = 0.05
                    
                    if random.random() < wicket_probability:
                        wickets += 1
                        self.logger.info(f"WICKET! Score: {current_score}/{wickets}")
                    else:
                        current_score += runs
                        
                time.sleep(1)  # Simulate real-time delay
            
            self.logger.info(f"End of over {over}: {current_score}/{wickets}")

import os
if __name__=='__main__':
    BOOTSTRAP_SERVERS = [os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')]
    orchestrator = MatchOrchestrator(BOOTSTRAP_SERVERS)
    time.sleep(5)
    orchestrator.start_training()
    print("training complete")
    time.sleep(2)
    print("waiting for the teams to be ready")
    time.sleep(4)
    print("match is about to begin")
    orchestrator.simulate_match()