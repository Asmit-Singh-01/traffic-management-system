import time
import random
from network import CityGrid
from metrics import TelemetryLogger

class TrafficSimulator:
    def __init__(self, steps):
        self.steps = steps
        self.grid = CityGrid("Metro_Prime_Grid")
        self.logger = TelemetryLogger()  # Data Pipeline Activated
        self.setup_city_map()

    def setup_city_map(self):
        """Creates a linear arterial road: Alpha -> Beta -> Gamma"""
        self.grid.add_junction("Node_Alpha") # City Entry
        self.grid.add_junction("Node_Beta")  # City Center
        self.grid.add_junction("Node_Gamma") # City Exit
        
        self.grid.link_junctions("Node_Alpha", "Node_Beta", "East")
        self.grid.link_junctions("Node_Beta", "Node_Gamma", "East")

    def generate_stochastic_traffic(self, step):
        """Simulates random arrivals AND Emergency Events"""
        inflow = random.randint(10, 30)
        self.grid.junctions["Node_Alpha"].receive_incoming_stream("West", inflow)
        print(f"[LIVE SENSOR] {inflow} new vehicles entered Node_Alpha (West).")
        
        # 🚨 Chaos Injection: Emergency Vehicle Override at Tick 3
        if step == 3:
            print("\n[🚨 CRITICAL ALERT] AMBULANCE DETECTED AT Node_Beta (South Lane)!")
            # Injecting a massive artificial weight (500) to force the algorithm to preemptively clear this lane.
            self.grid.junctions["Node_Beta"].lanes["South"] += 500

    def run(self):
        """Master Time-Loop Engine with Integrated Telemetry"""
        print("\n" + "="*60)
        print("INITIATING DATG LIVE SIMULATION WITH TELEMETRY & EMERGENCY")
        print("="*60)
        
        for step in range(1, self.steps + 1):
            print(f"\n--- [TIME TICK: {step}] ---")
            self.generate_stochastic_traffic(step)
            
            # Executing grid simulation and logging simultaneously
            for name, agent in self.grid.junctions.items():
                decision = agent.optimize_signal_matrix()
                
                # Data Pipeline: Logging this exact moment into CSV
                self.logger.log_step(step, agent, decision)
                
                # Routing cleared vehicles to the next junction
                if decision["outflow"] > 0:
                    agent.broadcast_to_neighbor(decision["selected_lane"], decision["outflow"])

        print("\n[SIMULATION TERMINATED] All data vectors successfully logged to CSV.")

if __name__ == "__main__":
    # Running simulation for 5 continuous time-cycles
    sim = TrafficSimulator(steps=5)
    sim.run()
    
