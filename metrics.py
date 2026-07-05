import csv
import os

class TelemetryLogger:
    def __init__(self, filename="traffic_telemetry.csv"):
        self.filename = filename
        self.initialize_csv()

    def initialize_csv(self):
        """Creates the dataset file with headers if it doesn't exist"""
        # If file is not present, create it and write features for ML training
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp_Tick", 
                    "Junction_ID", 
                    "Junction_Name", 
                    "North_Density", 
                    "South_Density", 
                    "East_Density", 
                    "West_Density", 
                    "Selected_Lane", 
                    "Allocated_Time", 
                    "Outflow_Throughput"
                ])
            print(f"[TELEMETRY] Dataset initialized: {self.filename}")

    def log_step(self, tick, agent, decision_matrix):
        """Dumps real-time infrastructure state vectors into the CSV dataset"""
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                tick,
                agent.agent_id,
                agent.location_name,
                agent.lanes["North"],
                agent.lanes["South"],
                agent.lanes["East"],
                agent.lanes["West"],
                decision_matrix["selected_lane"],
                decision_matrix["hold_time"],
                decision_matrix["outflow"]
            ])
          
