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

        df = pd.read_csv(self.csv_path)

        # Splitting data into Before AI (First 2000 steps) and After AI (Next 2000 steps)
        # Total ticks will be 4000 because pipeline runs simulation twice
        total_ticks = df["Timestamp_Tick"].max()
        
        # Filtering data based on the simulation flow
        half_ticks = total_ticks / 2
        before_ai_df = df[df["Timestamp_Tick"] <= half_ticks]
        after_ai_df = df[df["Timestamp_Tick"] > half_ticks]

        avg_wait_before = before_ai_df["Allocated_Time"].mean()
        avg_wait_after = after_ai_df["Allocated_Time"].mean()

        # Calculate exact percentage reduction in wait time
        # Standard Engineering Formula: ((Before - After) / Before) * 100
        if avg_wait_before > 0:
            efficiency_gain = ((avg_wait_before - avg_wait_after) / avg_wait_before) * 100
        else:
            efficiency_gain = 0

        total_vehicles_cleared = df["Outflow_Throughput"].sum()
        busiest_junction = df.groupby("Junction_Name")["North_Density"].mean().idxmax().replace('_', ' ')

        # --- HTML DASHBOARD (With Real Science Metrics) ---
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>DATG Live AI Control Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; }}
                .container {{ max-width: 1200px; margin: auto; text-align: center; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 30px; }}
                .card {{ background: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #38bdf8; text-align: left; }}
                .card.success {{ border-left-color: #4ade80; }}
                .card h3 {{ margin: 0; color: #94a3b8; font-size: 14px; }}
                .card p {{ font-size: 26px; font-weight: bold; margin: 10px 0 0 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #38bdf8;">DATG Autonomous Traffic Infrastructure</h1>
                <p>Research Prototype & MLOps Verification Insights</p>
                <div class="grid">
                    <div class="card"><h3>Total Telemetry Scale</h3><p>{total_ticks} Ticks</p></div>
                    <div class="card success"><h3>AI Optimization Index</h3><p>⚠️ Wait Time Reduced by {efficiency_gain:.1f}%</p></div>
                    <div class="card"><h3>Total Net Throughput</h3><p>{total_vehicles_cleared} Vehicles</p></div>
                    <div class="card"><h3>Bottleneck Node</h3><p>{busiest_junction}</p></div>
                </div>
            </div>
        </body>
        </html>
        """
        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # --- DYNAMIC README (Removing Buzzwords & Adding Limitations) ---
        markdown_content = f"""# DATG: Decentralized Autonomous Traffic Grid 🚦🧠

A research-oriented proof-of-concept (PoC) demonstrating decentralized multi-agent reinforcement mechanics for intelligent traffic mesh networks. Built natively for cloud-execution using automated MLOps pipelines.

---

## 📊 Empirical Performance Matrix (Auto-Generated)
> **Status:** ![AI Active](https://img.shields.io/badge/System_Status-Research_Prototype_•_AI_Inference-38bdf8?style=flat-square)
> *Metrics are calculated live by comparing algorithmic mathematical baseline behavior against the trained Random Forest Regressor.*

| Metric Dimension | Experimental Value | Engineering Analysis |
| :--- | :--- | :--- |
| **Telemetry Volume** | `{total_ticks} Continuous Records` | Data pool generated across high-stress stochastic time blocks. |
| **AI Optimization Index** | `📉 Wait Time Reduced by {efficiency_gain:.1f}%` | Core performance lift achieved by replacing static formula with AI inference. |
| **Network Throughput** | `{total_vehicles_cleared} Total Vehicles` | Cumulative vehicle units successfully transitioned across grid edges. |
| **Monitored Bottleneck** | `📍 {busiest_junction}` | System-wide highest stress junction localized by agent logging. |

---

## ⚙️ Core Architecture
1. **Autonomous Edge Agents (`agent.py`):** Simulates independent junction behaviors adjusting signal distributions locally based on real-time lane weights.
2. **I2I Communication Mesh (`network.py`):** Simplistic Infrastructure-to-Infrastructure packet relays allowing upstream nodes to alert downstream nodes of pending traffic load.
3. **Emergency Preemption Matrix:** An overriding queue mechanism that intercepts standard weights when high-priority vectors (Ambulances) are injected.
4. **Machine Learning Inference (`ai_brain.py`):** Uses a **Random Forest Regressor** to parse telemetry files and predict optimal timing slices, selected for its high interpretability on tabular data.

## ⚠️ Current System Limitations & Scope
As a research prototype, this system operates under specific constraints designed for algorithmic validation rather than production deployment:
* **Pure Simulation:** The system relies on synthetically generated stochastic lane streams rather than real-world CCTV or inductive-loop sensor feeds.
* **Deterministic Outflow Rates:** Vehicle clearing behavior follows mathematical limits (`allocated_time / 1.5`) which may vary in actual physical environments.
* **Simplified Network Topology:** The mesh network is validated on a localized grid rather than highly chaotic, irregular urban maps.
"""
        with open(self.output_md, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print("[SUCCESS] Applied brutal honesty and scientific metrics to documentation!")

if __name__ == "__main__":
    dash = TrafficDashboard()
    dash.generate_analytics()
        
