import random
import numpy as np

def generate_cricket_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        current_over = random.uniform(5, 20)
        current_score = current_over * random.uniform(5, 10)  # avg 5-10 runs per over
        wickets = random.randint(0, 9)
        run_rate = current_score / current_over
        
        # Features that affect final score
        batting_strength = random.uniform(0.6, 1.0)
        pitch_condition = random.uniform(0.7, 1.0)
        
        # Calculate final score (target variable)
        remaining_overs = 20 - current_over
        wicket_factor = (10 - wickets) / 10
        final_score = current_score + (remaining_overs * run_rate * wicket_factor * 
                                     batting_strength * pitch_condition)
        final_score = max(final_score * random.uniform(0.9, 1.1), current_score)  # Add some noise
        
        data.append({
            'current_over': round(current_over, 1),
            'current_score': round(current_score),
            'wickets': wickets,
            'run_rate': round(run_rate, 2),
            'batting_strength': round(batting_strength, 2),
            'pitch_condition': round(pitch_condition, 2),
            'final_score': round(final_score)
        })
    return data