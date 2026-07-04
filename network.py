from agent import JunctionAgent

class CityGrid:
    def __init__(self, city_name):
        self.city_name = city_name
        self.junctions = {}

    def add_junction(self, junction_name):
        """Creates a new autonomous agent and adds it to the grid"""
        agent = JunctionAgent(junction_name)
        self.junctions[junction_name] = agent
        print(f"[GRID ALERT] Added Junction Agent: {junction_name}")
        return agent

    def link_junctions(self, j1_name, j2_name, direction_j1_to_j2):
        """Bi-directional linking of two junctions using Graph logic"""
        if j1_name not in self.junctions or j2_name not in self.junctions:
            print("Error: Junctions must be added to the grid first.")
            return
            
        j1 = self.junctions[j1_name]
        j2 = self.junctions[j2_name]
        
        # Link J1 to J2
        j1.connect_neighbor(direction_j1_to_j2, j2)
        
        # Calculate reverse direction for J2 to J1
        opposite_directions = {"North": "South", "South": "North", "East": "West", "West": "East"}
        reverse_direction = opposite_directions.get(direction_j1_to_j2)
        
        j2.connect_neighbor(reverse_direction, j1)
        print(f"[NETWORK LINK] {j1_name} ({direction_j1_to_j2}) <---> {j2_name} ({reverse_direction})")

    def run_simulation_step(self):
        """Triggers a single time-step across the entire city grid"""
        print(f"\n--- Running City Grid Simulation: {self.city_name} ---")
        for name, agent in self.junctions.items():
            print(f"\nProcessing Agent: {name}")
            
            # Agent calculates its own optimal signal configuration
            decision = agent.optimize_signal_matrix()
            
            # If vehicles are cleared, broadcast them to the connected neighbor
            if decision["outflow"] > 0:
                target_lane = decision["selected_lane"]
                agent.broadcast_to_neighbor(target_lane, decision["outflow"])

# Quick Execution Test for the Mesh
if __name__ == "__main__":
    grid = CityGrid("Core_Traffic_Grid")
    
    # 1. Add Junctions
    grid.add_junction("Alpha_Node")
    grid.add_junction("Beta_Node")
    
    # 2. Link them (Alpha's East connects to Beta's West)
    grid.link_junctions("Alpha_Node", "Beta_Node", "East")
    
    # 3. Inject Traffic Manually (Simulating Live Sensors)
    grid.junctions["Alpha_Node"].receive_incoming_stream("East", 40)
    grid.junctions["Beta_Node"].receive_incoming_stream("West", 10)
    
    # 4. Run one cycle of the network
    grid.run_simulation_step()
  
