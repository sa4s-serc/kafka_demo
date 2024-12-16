# kafka_diagnostic.py
from kafka import KafkaProducer, KafkaConsumer
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaDiagnostic:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        
    def test_producer(self):
        """Test if we can produce messages"""
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            
            # Send test message
            future = producer.send('training-data', {'test': 'message'})
            result = future.get(timeout=10)
            logger.info(f"Producer test successful - Message sent to partition {result.partition}")
            producer.close()
            return True
            
        except Exception as e:
            logger.error(f"Producer test failed: {str(e)}")
            return False

    def test_consumer(self):
        """Test if we can consume messages"""
        try:
            consumer = KafkaConsumer(
                'training-data',
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                consumer_timeout_ms=5000  # 5 second timeout
            )
            
            logger.info("Consumer connected, waiting for messages...")
            
            # Try to consume messages
            messages = []
            start_time = time.time()
            while time.time() - start_time < 5:  # Wait up to 5 seconds
                msg_pack = consumer.poll(timeout_ms=1000)
                if msg_pack:
                    for tp, msgs in msg_pack.items():
                        messages.extend(msgs)
                        logger.info(f"Received {len(msgs)} messages from partition {tp.partition}")
            
            consumer.close()
            
            if messages:
                logger.info(f"Consumer test successful - Received {len(messages)} messages")
                return True
            else:
                logger.warning("Consumer test - No messages received")
                return False
                
        except Exception as e:
            logger.error(f"Consumer test failed: {str(e)}")
            return False

    def list_topics(self):
        """List all available topics"""
        try:
            consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
            topics = consumer.topics()
            logger.info(f"Available topics: {topics}")
            consumer.close()
            return topics
            
        except Exception as e:
            logger.error(f"Failed to list topics: {str(e)}")
            return set()

    def run_diagnostics(self):
        """Run all diagnostic tests"""
        logger.info(f"Starting Kafka diagnostics on {self.bootstrap_servers}")
        
        logger.info("\n1. Checking available topics...")
        topics = self.list_topics()
        
        logger.info("\n2. Testing producer...")
        producer_ok = self.test_producer()
        
        logger.info("\n3. Testing consumer...")
        consumer_ok = self.test_consumer()
        
        return {
            'topics_available': bool(topics),
            'producer_working': producer_ok,
            'consumer_working': consumer_ok,
            'topics': topics
        }

if __name__ == "__main__":
    import os
    
    # Get Kafka bootstrap servers from environment or use default
    bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    # Run diagnostics
    diagnostic = KafkaDiagnostic(bootstrap_servers)
    results = diagnostic.run_diagnostics()
    
    # Print summary
    print("\nDiagnostic Results:")
    print(f"Topics Available: {'✓' if results['topics_available'] else '✗'}")
    print(f"Producer Working: {'✓' if results['producer_working'] else '✗'}")
    print(f"Consumer Working: {'✓' if results['consumer_working'] else '✗'}")
    print(f"\nAvailable Topics: {results['topics']}")