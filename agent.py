import uuid

class JunctionAgent:
    def __init__(self, location_name, capacity=100):
        self.agent_id = str(uuid.uuid4())[:8]
        self.location_name = location_name
        self.capacity = capacity
        
        # Grid connection mappings: { 'Direction': 'Connected_Junction_Agent_ID' }
        self.neighbors = {}
        
        # Real-time Telemetry: Lane Density Tracking
        self.lanes = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.state = "IDLE"  # IDLE, PROCESSING, EMERGENCY_CORRIDOR
        
    def connect_neighbor(self, direction, neighbor_agent):
        """Builds the I2I (Infrastructure-to-Infrastructure) Network Mesh"""
        self.neighbors[direction] = neighbor_agent

    def receive_incoming_stream(self, lane, vehicle_count):
        """API simulation endpoint for live camera/sensor input"""
        predicted_load = self.lanes[lane] + vehicle_count
        if predicted_load > self.capacity:
            print(f"[CRITICAL] {self.location_name} - {lane} Lane Gridlock imminent! Overflowing.")
            self.lanes[lane] = self.capacity
        else:
            self.lanes[lane] = predicted_load

    def optimize_signal_matrix(self):
        """Advanced Priority-Index Matrix Scoring (Pre-AI Optimization layer)"""
        total_load = sum(self.lanes.values())
        if total_load == 0:
            return {"selected_lane": "North", "hold_time": 10, "outflow": 0}
            
        # Calculate mathematical weights for each lane considering sudden spikes
        lane_weights = {lane: (count / total_load) * 100 for lane, count in self.lanes.items()}
        target_lane = max(lane_weights, key=lane_weights.get)
        
        # Allocate dynamic budget window
        allocated_time = max(10, min(45, int((self.lanes[target_lane] / total_load) * 90)))
        
        # Calculate theoretical vehicle outflow (1 vehicle per 1.5 seconds)
        potential_outflow = int(allocated_time / 1.5)
        actual_outflow = min(self.lanes[target_lane], potential_outflow)
        
        # Process the depletion locally
        self.lanes[target_lane] -= actual_outflow
        
        return {
            "selected_lane": target_lane,
            "hold_time": allocated_time,
            "outflow": actual_outflow
        }
        
    def broadcast_to_neighbor(self, direction, vehicle_count):
        """Predictive messaging to downstream junctions"""
        if direction in self.neighbors and vehicle_count > 0:
            neighbor = self.neighbors[direction]
            # If we push vehicles North, they enter the neighbor's South lane
            opposite_directions = {"North": "South", "South": "North", "East": "West", "West": "East"}
            incoming_lane = opposite_directions.get(direction, "North")
            
            print(f"[I2I Telemetry] {self.location_name} broadcasting {vehicle_count} vehicles to {neighbor.location_name} ({incoming_lane} lane).")
            neighbor.receive_incoming_stream(incoming_lane, vehicle_count)
          
