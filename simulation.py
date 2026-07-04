import time
import random
from network import CityGrid

class TrafficSimulator:
    def __init__(self, steps):
        self.steps = steps
        self.grid = CityGrid("Metro_Prime_Grid")
        self.setup_city_map()

    def setup_city_map(self):
        """Creates a linear arterial road: Alpha -> Beta -> Gamma"""
        self.grid.add_junction("Node_Alpha") # City Entry
        self.grid.add_junction("Node_Beta")  # City Center
        self.grid.add_junction("Node_Gamma") # City Exit
        
        # Linking the arterial route
        self.grid.link_junctions("Node_Alpha", "Node_Beta", "East")
        self.grid.link_junctions("Node_Beta", "Node_Gamma", "East")

    def generate_stochastic_traffic(self):
        """Simulates random vehicle arrivals at the city boundaries"""
        # Injecting vehicles randomly at the entry node (Node_Alpha)
        inflow = random.randint(10, 30)
        self.grid.junctions["Node_Alpha"].receive_incoming_stream("West", inflow)
        print(f"[LIVE SENSOR] {inflow} new vehicles entered Node_Alpha from West.")

    def run(self):
        """The Main Master Time-Loop Engine"""
        print("\n" + "="*50)
        print("INITIATING DATG LIVE SIMULATION PROTOCOL")
        print("="*50)
        
        for step in range(1, self.steps + 1):
            print(f"\n" + "-"*15 + f" [TIME TICK: {step}] " + "-"*15)
            
            # Step 1: Inject new random traffic
            self.generate_stochastic_traffic()
            
            # Step 2: Let the grid process the routing and networking
            self.grid.run_simulation_step()
            
            # In a real environment, this delay keeps the CPU load stable
            # time.sleep(0.5) 
            
        print("\n[SIMULATION TERMINATED] Cycle Complete.")

if __name__ == "__main__":
    # Running a test simulation for 5 continuous time-cycles
    sim = TrafficSimulator(steps=5)
    sim.run()
