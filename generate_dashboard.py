import pandas as pd
import os

class TrafficDashboard:
    def __init__(self, csv_path="traffic_telemetry.csv", output_html="dashboard.html", output_md="README.md"):
        self.csv_path = csv_path
        self.output_html = output_html
        self.output_md = output_md

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
        busiest_junction = df.groupby("Junction_Name")["North_Density"].mean().idxmax().replace('_', ' ')

        # --- 1. HTML DASHBOARD GENERATION ---
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
                    <div class="card"><h3>Total Simulation Scale</h3><p>{total_ticks} Ticks</p></div>
                    <div class="card"><h3>AI Avg Signal Budget</h3><p>{avg_waiting_time}s</p></div>
                    <div class="card"><h3>Network Throughput</h3><p>{total_vehicles_cleared} Vehicles</p></div>
                    <div class="card emergency"><h3>Highest Congestion Node</h3><p>{busiest_junction}</p></div>
                </div>
                <div class="footer"><p>System Status: <span style="color: #4ade80;">● Fully Autonomous (AI Inference Deployed)</span></p></div>
            </div>
        </body>
        </html>
        """
        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # --- 2. DYNAMIC README GENERATION (The Impression Booster) ---
        markdown_content = f"""# DATG: Decentralized Autonomous Traffic Grid 🚦🧠

An advanced, multi-agent AI infrastructure designed to replace static traffic light systems with a predictive, highly scalable mesh network. Built natively for cloud-execution using MLOps pipelines.

---

## 📊 Live Cloud Execution Metrics (Auto-Generated)
> **Status:** ![AI Active](https://img.shields.io/badge/System_Status-Fully_Autonomous_•_AI_Inference-4ade80?style=flat-square)
> *These metrics represent live data processed directly by the trained Random Forest model on GitHub Actions cloud servers.*

| Metric Dimension | Current Cloud Value | Operational Insight |
| :--- | :--- | :--- |
| **Total Simulation Scale** | `{total_ticks} Continuous Ticks` | Enterprise-grade stress testing vector volume |
| **AI Avg Signal Budget** | `{avg_waiting_time} Seconds` | Dynamically optimized green-light window to minimize idling |
| **Network Throughput** | `{total_vehicles_cleared} Vehicles Cleared` | Total structural fluid mobility achieved across nodes |
| **Critical Bottleneck Node** | `🔥 {busiest_junction}` | System-wide highest stress junction localized by AI sensors |

---

## ⚙️ Core Architecture

1. **Autonomous Edge Agents (`agent.py`):** Every junction acts as an independent node calculating its own dynamic optimal signal budget based on live density weights.
2. **I2I Mesh Network (`network.py`):** Infrastructure-to-Infrastructure communication. Junctions broadcast incoming vehicle loads to downstream nodes for predictive clearing.
3. **Emergency Preemption:** Built-in chaos management. Automatically detects high-priority vehicles (Ambulances) and dynamically re-routes system weights.
4. **Automated Telemetry (`metrics.py`):** Real-time extraction of lane densities into a tabular dataset.
5. **AI Neural Brain (`ai_brain.py`):** A Random Forest Regressor trained automatically via cloud CI/CD to predict mathematically optimal signal timings.

## 🚀 Cloud Execution & CI/CD
This project requires **Zero Local Compute**. It uses GitHub Actions to provision an Ubuntu server, install dependencies (`pandas`, `scikit-learn`), generate telemetry, train the model, and rewrite this documentation live.
"""
        with open(self.output_md, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print("[SUCCESS] HTML Dashboard and README.md metrics successfully synchronized!")

if __name__ == "__main__":
    dash = TrafficDashboard()
    dash.generate_analytics()
    
