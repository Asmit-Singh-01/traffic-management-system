import pandas as pd
import os

class TrafficDashboard:
    def __init__(self, csv_path="traffic_telemetry.csv", output_html="dashboard.html"):
        self.csv_path = csv_path
        self.output_html = output_html

    def generate_analytics(self):
        if not os.path.exists(self.csv_path):
            print("[DASHBOARD ERROR] Telemetry data missing.")
            return

        # Reading the massive 6000+ rows dataset
        df = pd.read_csv(self.csv_path)

        # Calculating Core Metrics
        total_ticks = df["Timestamp_Tick"].max()
        avg_waiting_time = int(df["Allocated_Time"].mean())
        total_vehicles_cleared = df["Outflow_Throughput"].sum()
        
        # Finding the busiest junction
        busiest_junction = df.groupby("Junction_Name")["North_Density"].mean().idxmax()

        # Generating HTML + CSS Dashboard on the fly
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DATG Live AI Control Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
                .container {{ max-width: 1200px; margin: auto; }}
                header {{ text-align: center; padding: 20px; border-bottom: 2px solid #1e293b; }}
                h1 {{ color: #38bdf8; margin: 0; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }}
                .card {{ background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 5px solid #38bdf8; }}
                .card.emergency {{ border-left-color: #ef4444; }}
                .card h3 {{ margin: 0; color: #94a3b8; font-size: 14px; text-transform: uppercase; }}
                .card p {{ font-size: 28px; font-weight: bold; margin: 10px 0 0 0; color: #f1f5f9; }}
                .footer {{ text-align: center; margin-top: 5px; color: #64748b; font-size: 12px; padding: 40px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>DATG Autonomous Traffic Infrastructure</h1>
                    <p>Live Cloud Execution Analytics & MLOps Insights</p>
                </header>
                
                <div class="grid">
                    <div class="card">
                        <h3>Total Simulation Scale</h3>
                        <p>{total_ticks} Continuous Ticks</p>
                    </div>
                    <div class="card">
                        <h3>AI Avg Signal Budget</h3>
                        <p>{avg_waiting_time} Seconds</p>
                    </div>
                    <div class="card">
                        <h3>Network Throughput</h3>
                        <p>{total_vehicles_cleared} Vehicles Cleared</p>
                    </div>
                    <div class="card emergency">
                        <h3>Highest Congestion Node</h3>
                        <p>{busiest_junction.replace('_', ' ')}</p>
                    </div>
                </div>

                <div class="footer">
                    <p>System Status: <span style="color: #4ade80;">● Fully Autonomous (AI Inference Deployed)</span></p>
                </div>
            </div>
        </body>
        </html>
        """

        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[DASHBOARD] Visual UI successfully generated: {self.output_html}")

if __name__ == "__main__":
    dash = TrafficDashboard()
    dash.generate_analytics()
  
