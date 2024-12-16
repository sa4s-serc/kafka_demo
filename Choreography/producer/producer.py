from kafka import KafkaProducer
import json
import time
import random
import os

def generate_sensor_data():      
    return {
        'temperature': random.uniform(20, 30),
        'humidity': random.uniform(40, 80),
        'pressure': random.uniform(980, 1020)
    }

def main():
    print("Starting to send data")
    producer = KafkaProducer(
        bootstrap_servers=[os.environ.get('KAFKA_BROKER', 'localhost:9092')],
        value_serializer=lambda x: json.dumps(x).encode('utf-8') #converting a json to a string - bceasue cant send it as a dict - serialising
    )
    
    while True:
        data = generate_sensor_data()
        producer.send('sensor_data', value=data) # sensor data - topic; value - data
        print(f"Produced: {data}")
        time.sleep(5)

if __name__ == "__main__":
    print("I am a successfull producer waiting for the slow kafka")
    # time.sleep(30)  # Wait for Kafka to start
    main()
