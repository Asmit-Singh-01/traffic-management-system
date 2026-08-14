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




def calculate_mae(actual, predicted):
    """Calculate mean absolute error between actual and predicted values."""
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must be the same length")
    if len(actual) == 0:
        raise ValueError("actual/predicted must not be empty")
    errors = [abs(float(a) - float(p)) for a, p in zip(actual, predicted)]
    return sum(errors) / len(errors)


REQUIRED_QUEUE_FIELDS = [
    "North_Density", "South_Density", "East_Density", "West_Density", "Outflow_Throughput"
]

def calculate_average_queue_delay(telemetry_rows, tick_duration_seconds=1.0):
    """Estimate average queue delay from queue length and throughput.

    Uses a simplified Little's Law style estimate:
        delay = (average queue length / average throughput) * tick_duration_seconds

    Assumption (not defined elsewhere in this repo): if queue length is 0,
    delay is defined as 0 regardless of throughput. If queue length > 0 and
    throughput is 0, delay is defined as infinity (gridlock: cars waiting,
    nothing leaving).
    """
    if not telemetry_rows:
        return 0.0

    total_queue = 0.0
    total_throughput = 0.0
    for row in telemetry_rows:
        for field in REQUIRED_QUEUE_FIELDS:
            if field not in row:
                raise ValueError(f"Missing required field: {field}")
        queue = (
            row["North_Density"] + row["South_Density"]
            + row["East_Density"] + row["West_Density"]
        )
        total_queue += queue
        total_throughput += row["Outflow_Throughput"]

    avg_queue = total_queue / len(telemetry_rows)
    avg_throughput = total_throughput / len(telemetry_rows)

    if avg_queue == 0:
        return 0.0
    if avg_throughput == 0:
        return float("inf")
    return (avg_queue / avg_throughput) * tick_duration_seconds


def calculate_peak_flow_throughput(telemetry_rows):
    """Return the highest total network throughput recorded in a single tick."""
    from collections import defaultdict
    totals = defaultdict(int)
    for row in telemetry_rows:
        totals[row["Timestamp_Tick"]] += row["Outflow_Throughput"]
    return max(totals.values())


def calculate_baseline_improvement(current_value, baseline_value, *, higher_is_better):
    """Calculate percentage improvement over a static baseline."""
    if baseline_value == 0:
        raise ValueError("baseline_value must not be zero")
    if higher_is_better:
        return ((current_value - baseline_value) / baseline_value) * 100
    return ((baseline_value - current_value) / baseline_value) * 100