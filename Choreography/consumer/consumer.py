from kafka import KafkaConsumer
import json
import time
import os
from model import AnomalyDetector

def main():
    consumer = KafkaConsumer(
        'sensor_data',
        bootstrap_servers=[os.environ.get('KAFKA_BROKER', 'localhost:9092')],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')), # converting string back to a json - 
        auto_offset_reset='earliest'
    )
    print("Connected to kafka")
    detector = AnomalyDetector()
    buffer = []
    
    for message in consumer:
        data = message.value
        print(data)
        buffer.append(data)
        
        if len(buffer) >= 10 and not detector.is_trained:
            detector.train(buffer)
            print("Model trained!")
        
        if detector.is_trained:
            prediction = detector.predict(data)
            status = "NORMAL" if prediction == 1 else "ANOMALY"
            print(f"Consumed: {data} - Status: {status}")
        else:
            print(f"Consumed: {data} - Collecting training data...")

if __name__ == "__main__":
    print("I am a successful consumer waiting for the slow kafka and producer")
    # time.sleep(30)  # Wait for Kafka to start
    main()