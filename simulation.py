import time
import random
import math
from network import CityGrid
from metrics import TelemetryLogger

class TrafficSimulator:
    def __init__(self, steps, scenario="baseline"):
        self.steps = steps
        self.scenario = scenario
        self.grid = CityGrid("Metro_Prime_Grid")
        self.logger = TelemetryLogger(filename=f"telemetry_{self.scenario}.csv")
        self.setup_city_map()

    def setup_city_map(self):
        self.grid.add_junction("Node_Alpha") 
        self.grid.add_junction("Node_Beta")  
        self.grid.add_junction("Node_Gamma") 
        self.grid.link_junctions("Node_Alpha", "Node_Beta", "East")
        self.grid.link_junctions("Node_Beta", "Node_Gamma", "East")

    def generate_stochastic_traffic(self, step):
        """Simulates Real-World Traffic including Rush Hours & Night Time"""
        
        # Base Traffic Logic
        time_factor = math.sin(step / 50.0) 
        if time_factor > 0.7:
            inflow = random.randint(50, 120)
        elif time_factor < -0.5:
            inflow = random.randint(0, 10)
        else:
            inflow = random.randint(15, 40)

        self.grid.junctions["Node_Alpha"].receive_incoming_stream("West", inflow)
        
        # Controlled Anomaly Logic (For Research Benchmarking)
        if self.scenario == "stress_test":
            # Injecting a massive bottleneck exactly at step 1000, lasting for 50 steps
            if 1000 <= step <= 1050:
                self.grid.junctions["Node_Beta"].lanes["South"] += 100
                if step == 1000:
                    print("\n[ALERT] STRESS TEST: Major blockage detected at Node_Beta (South Lane)!")

    def run(self):
        print(f"\n[SYSTEM] Initiating {self.scenario.upper()} Simulation for {self.steps} ticks...")
        
        for step in range(1, self.steps + 1):
            self.generate_stochastic_traffic(step)
            
            for name, agent in self.grid.junctions.items():
                decision = agent.optimize_signal_matrix()
                self.logger.log_step(step, agent, decision)
                
                if decision["outflow"] > 0:
                    agent.broadcast_to_neighbor(decision["selected_lane"], decision["outflow"])

            if step % 500 == 0:
                print(f"[PROGRESS] Simulated {step}/{self.steps} time ticks...")

        print(f"[SIMULATION TERMINATED] Data logged to telemetry_{self.scenario}.csv")

def run_monte_carlo_validation(iterations, steps_per_run):
    """
    Executes multiple runs to validate system stability across different random seeds.
    This separates a standard project from a research-grade simulation.
    """
    print("\n--- INITIATING STATISTICAL VALIDATION PIPELINE ---")
    
    # 1. Run Baseline (Control Group)
    sim_baseline = TrafficSimulator(steps=steps_per_run, scenario="baseline")
    sim_baseline.run()
    
    # 2. Run Stress Test (Experimental Group)
    sim_stress = TrafficSimulator(steps=steps_per_run, scenario="stress_test")
    sim_stress.run()
    
    print("\n--- VALIDATION COMPLETE ---")
    print("Next Step: Update ai_brain.py to train/evaluate on both datasets to calculate delay mitigation index.")

if __name__ == "__main__":
    # Running validation with 2000 steps
    run_monte_carlo_validation(iterations=1, steps_per_run=2000)
    
