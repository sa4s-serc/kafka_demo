from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.2,
            random_state=42
        )
        self.is_trained = False
        self.training_data = []
    
    def train(self, data):
        if len(data) >= 10:  # Train after collecting enough samples
            self.model.fit([[d['temperature'], d['humidity'], d['pressure']] for d in data])
            self.is_trained = True
    
    def predict(self, data):
        if not self.is_trained:
            return 0  # Return normal if model isn't trained yet
        
        prediction = self.model.predict([[
            data['temperature'],
            data['humidity'],
            data['pressure']
        ]])[0]
        
        return 1 if prediction == 1 else -1  # 1 for normal, -1 for anomaly
    
