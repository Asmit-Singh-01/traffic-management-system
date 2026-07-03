import time

class DynamicTrafficJunction:
    def __init__(self, name):
        self.name = name
        # Queue lengths for 4 roads
        self.lanes = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.current_green = None
        
        # System Constraints
        self.min_green_time = 10  # seconds
        self.max_green_time = 60  # seconds
        self.base_cycle_time = 120 # total cycle budget

    def update_traffic(self, n, s, e, w):
        """Simulating live vehicle sensor data input"""
        self.lanes["North"] = max(0, self.lanes["North"] + n)
        self.lanes["South"] = max(0, self.lanes["South"] + s)
        self.lanes["East"] = max(0, self.lanes["East"] + e)
        self.lanes["West"] = max(0, self.lanes["West"] + w)

    def calculate_dynamic_timer(self, lane):
        """Level 2 Core: Mathematical optimization based on current density"""
        total_vehicles = sum(self.lanes.values())
        if total_vehicles == 0:
            return self.min_green_time
            
        lane_vehicles = self.lanes[lane]
        # Ratio based distribution
        calculated_time = int((lane_vehicles / total_vehicles) * self.base_cycle_time)
        
        # Clamp between min and max boundaries
        return max(self.min_green_time, min(self.max_green_time, calculated_time))

    def process_highest_density(self):
        """Finds which lane needs priority immediately"""
        # Level 2 Algorithm: Starvation and Priority management
        highest_traffic_lane = max(self.lanes, key=self.lanes.get)
        
        if self.lanes[highest_traffic_lane] == 0:
            print("No traffic detected anywhere. Keeping system idle.")
            return

        self.current_green = highest_traffic_lane
        green_duration = self.calculate_dynamic_timer(highest_traffic_lane)
        
        print(f"\n--- Junction: {self.name} Status ---")
        print(f"Current Traffic Load: {self.lanes}")
        print(f"Priority Assigned To: {self.current_green} Lane")
        print(f"Allocated Green Time: {green_duration} seconds")
        
        # Simulate traffic clearing (Assuming 1 vehicle clears every 2 seconds)
        vehicles_cleared = int(green_duration / 2)
        actual_cleared = min(self.lanes[self.current_green], vehicles_cleared)
        self.lanes[self.current_green] -= actual_cleared
        
        print(f"Action: Cleared {actual_cleared} vehicles from {self.current_green}.")

if __name__ == "__main__":
    # Execution Test Case
    junction = DynamicTrafficJunction("Heavy_Intersection_01")
    
    # North has heavy traffic, West is nearly empty
    junction.update_traffic(45, 15, 20, 5)
    
    # Process Cycle 1
    junction.process_highest_density()
    
    # Process Cycle 2 (System should automatically switch to the next heavy lane)
    junction.process_highest_density()
    
