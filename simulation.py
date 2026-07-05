import time
import random
import math
from network import CityGrid
from metrics import TelemetryLogger

class TrafficSimulator:
    def __init__(self, steps):
        self.steps = steps
        self.grid = CityGrid("Metro_Prime_Grid")
        self.logger = TelemetryLogger()
        self.setup_city_map()

    def setup_city_map(self):
        self.grid.add_junction("Node_Alpha") 
        self.grid.add_junction("Node_Beta")  
        self.grid.add_junction("Node_Gamma") 
        self.grid.link_junctions("Node_Alpha", "Node_Beta", "East")
        self.grid.link_junctions("Node_Beta", "Node_Gamma", "East")

    def generate_stochastic_traffic(self, step):
        """Simulates Real-World Traffic including Rush Hours & Night Time"""
        
        # Real-world logic: Using a sine wave pattern to create 'Rush Hours'
        # Sine wave goes from -1 to 1. We scale it to adjust traffic volume.
        time_factor = math.sin(step / 50.0) 
        
        if time_factor > 0.7:
            # Rush Hour (High Traffic Spike)
            inflow = random.randint(50, 120)
        elif time_factor < -0.5:
            # Night Time (Low Traffic)
            inflow = random.randint(0, 10)
        else:
            # Normal Day Traffic
            inflow = random.randint(15, 40)

        self.grid.junctions["Node_Alpha"].receive_incoming_stream("West", inflow)
        
        # 🚨 Chaos Injection: Random Emergencies (1% chance at any given tick)
        if random.random() < 0.01:
            random_node = random.choice(list(self.grid.junctions.keys()))
            print(f"\n[🚨 CRITICAL] EMERGENCY VEHICLE AT {random_node}!")
            self.grid.junctions[random_node].lanes["South"] += 500

    def run(self):
        print(f"\n[SYSTEM] Initiating Heavy-Duty Simulation for {self.steps} ticks...")
        
        for step in range(1, self.steps + 1):
            self.generate_stochastic_traffic(step)
            
            for name, agent in self.grid.junctions.items():
                decision = agent.optimize_signal_matrix()
                self.logger.log_step(step, agent, decision)
                
                if decision["outflow"] > 0:
                    agent.broadcast_to_neighbor(decision["selected_lane"], decision["outflow"])

            # Every 500 steps, print progress so we don't spam the cloud terminal
            if step % 500 == 0:
                print(f"[PROGRESS] Simulated {step}/{self.steps} time ticks...")

        print(f"\n[SIMULATION TERMINATED] {self.steps * len(self.grid.junctions)} vectors logged to CSV.")

if __name__ == "__main__":
    # SCALED UP: Running for 2000 continuous time-cycles instead of 5
    sim = TrafficSimulator(steps=2000)
    sim.run()
    
