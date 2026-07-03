import time

class TrafficJunction:
    def __init__(self, name):
        self.name = name
        # 4 Roads: North, South, East, West
        # Initializing queue of vehicles on each road
        self.lanes = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.current_green = "North"

    def update_traffic(self, n, s, e, w):
        """Simulate vehicle arrival"""
        self.lanes["North"] += n
        self.lanes["South"] += s
        self.lanes["East"] += e
        self.lanes["West"] += w

    def cycle_signals(self):
        """Level 1: Static timer-based switching"""
        directions = list(self.lanes.keys())
        current_index = directions.index(self.current_green)
        
        # Move to next direction linearly
        next_index = (current_index + 1) % 4
        self.current_green = directions[next_index]
        
        # Level 1 Flaw/Limitation: It clears fixed vehicles without checking density
        cleared = min(self.lanes[self.current_green], 5) 
        self.lanes[self.current_green] -= cleared
        
        print(f"Signal Changed! Green: {self.current_green} | Cleared: {cleared} vehicles.")

# Quick execution check
if __name__ == "__main__":
    junction = TrafficJunction("Chauraha_Main")
    junction.update_traffic(10, 5, 8, 3)
    print(f"Initial State: {junction.lanes}")
    junction.cycle_signals()
    print(f"Post-Cycle State: {junction.lanes}")
  
