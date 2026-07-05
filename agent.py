import uuid
from ai_brain import TrafficAI

class JunctionAgent:
    def __init__(self, location_name, capacity=100):
        self.agent_id = str(uuid.uuid4())[:8]
        self.location_name = location_name
        self.capacity = capacity
        
        self.neighbors = {}
        self.lanes = {"North": 0, "South": 0, "East": 0, "West": 0}
        
        # 🧠 Attaching the AI Brain to the Edge Agent
        self.brain = TrafficAI()
        self.ai_active = self.brain.load_brain()
        
    def connect_neighbor(self, direction, neighbor_agent):
        self.neighbors[direction] = neighbor_agent

    def receive_incoming_stream(self, lane, vehicle_count):
        predicted_load = self.lanes[lane] + vehicle_count
        if predicted_load > self.capacity:
            self.lanes[lane] = self.capacity
        else:
            self.lanes[lane] = predicted_load

    def optimize_signal_matrix(self):
        """Now uses Neural Network Inference instead of static math"""
        total_load = sum(self.lanes.values())
        if total_load == 0:
            return {"selected_lane": "North", "hold_time": 10, "outflow": 0}
            
        # 1. Determine which lane needs immediate priority
        lane_weights = {lane: (count / total_load) * 100 for lane, count in self.lanes.items()}
        target_lane = max(lane_weights, key=lane_weights.get)
        
                # 2. 🧠 AI INFERENCE: Ask the trained model for the exact time needed
        if self.ai_active:
            allocated_time = self.brain.predict_optimal_time(
                self.lanes["North"], self.lanes["South"], 
                self.lanes["East"], self.lanes["West"]
            )
            # 👇 YEH LINE ADD KARNI HAI VISUAL PROOF KE LIYE
            print(f"[🧠 AI INFERENCE ACTIVE] {self.location_name} timing predicted by AI Brain: {allocated_time}s")
            
            allocated_time = max(10, min(60, allocated_time))
        else:
            # 👇 YEH LINE BHI UPDATE KAR LO TAAKI FARQ DIKHE
            print(f"[⚠️ FALLBACK MATH ACTIVE] {self.location_name} using static formula.")
            allocated_time = max(10, min(45, int((self.lanes[target_lane] / total_load) * 90)))

        
        potential_outflow = int(allocated_time / 1.5)
        actual_outflow = min(self.lanes[target_lane], potential_outflow)
        
        self.lanes[target_lane] -= actual_outflow
        
        return {
            "selected_lane": target_lane,
            "hold_time": allocated_time,
            "outflow": actual_outflow
        }
        
    def broadcast_to_neighbor(self, direction, vehicle_count):
        if direction in self.neighbors and vehicle_count > 0:
            neighbor = self.neighbors[direction]
            opposite_directions = {"North": "South", "South": "North", "East": "West", "West": "East"}
            incoming_lane = opposite_directions.get(direction, "North")
            neighbor.receive_incoming_stream(incoming_lane, vehicle_count)
            
