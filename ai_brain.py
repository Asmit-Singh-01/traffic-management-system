import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
import warnings

# Suppress sklearn warnings for cleaner terminal output
warnings.filterwarnings("ignore")

class TrafficAI:
    def __init__(self, data_path="traffic_telemetry.csv", model_path="ai_model.pkl"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None

    def train_model(self):
        """Reads the CSV telemetry data and trains the AI model"""
        if not os.path.exists(self.data_path):
            print("[AI ERROR] Telemetry dataset missing. Run simulation first.")
            return

        print("\n[AI BRAIN] Initializing Neural Training Sequence...")
        df = pd.read_csv(self.data_path)
        
        if len(df) < 2:
            print("[AI WARNING] Dataset too small for training.")
            return

        # Features (X): Current traffic density in all lanes
        X = df[["North_Density", "South_Density", "East_Density", "West_Density"]]
        # Target (Y): The optimal green light time the system allocated previously
        y = df["Allocated_Time"]

        print(f"[AI BRAIN] Training Random Forest on {len(df)} telemetry vectors...")
        # Using Random Forest for robust, non-linear pattern recognition
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.model.fit(X, y)

        # Saving the trained 'Brain' as a binary file
        joblib.dump(self.model, self.model_path)
        print(f"[AI BRAIN] Training Complete. Intelligence saved to {self.model_path}")

    def load_brain(self):
        """Loads the pre-trained model for real-time predictions"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False

    def predict_optimal_time(self, n, s, e, w):
        """Predicts the exact seconds needed based on live sensor data"""
        if self.model is None and not self.load_brain():
            return 20 # Fallback time if AI fails or isn't trained yet
            
        prediction = self.model.predict([[n, s, e, w]])
        return int(prediction[0])

# Quick Cloud Execution Test
if __name__ == "__main__":
    ai = TrafficAI()
    ai.train_model()
  
