import pandas as pd
import os

class TrafficDashboard:
    def __init__(self, csv_path="traffic_telemetry.csv", output_html="dashboard.html", output_md="README.md"):
        self.csv_path = csv_path
        self.output_html = output_html
        self.output_md = output_md

    def generate_analytics(self):
        if not os.path.exists(self.csv_path):
            print("[DASHBOARD ERROR] Telemetry dataset not localized.")
            return

        # Ingesting data
        df = pd.read_csv(self.csv_path)
        total_ticks = str(df["Timestamp_Tick"].max())
        total_vehicles_cleared = str(df["Outflow_Throughput"].sum())
        busiest_junction = str(df.groupby("Junction_Name")["North_Density"].mean().idxmax().replace('_', ' '))

        legacy_fixed_wait_time = 30.0
        ai_predicted_wait_time = df["Allocated_Time"].mean()
        efficiency_gain = f"{((legacy_fixed_wait_time - ai_predicted_wait_time) / legacy_fixed_wait_time) * 100:.1f}"

        # --- 1. HTML DASHBOARD GENERATION ---
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DATG Operational Control Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px; }
        .container { max-width: 1200px; margin: auto; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; margin-top: 40px; }
        .card { background: #1e293b; padding: 25px; border-radius: 14px; border-left: 5px solid #38bdf8; text-align: left; }
        .card.success { border-left-color: #4ade80; }
        .card h3 { margin: 0; color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }
        .card p { font-size: 28px; font-weight: 700; margin: 12px 0 0 0; color: #f1f5f9; }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="color: #38bdf8; font-size: 32px;">DATG: Decentralized Autonomous Traffic Grid</h1>
        <p style="color: #64748b;">Algorithmic Validation Framework & Asset Dashboard</p>
        <div class="grid">
            <div class="card"><h3>Telemetry Matrix Volume</h3><p>__TOTAL_TICKS__ Data Vectors</p></div>
            <div class="card success"><h3>Delay Mitigation Index</h3><p>⏳ Latency Reduced by __EFFICIENCY__%</p></div>
            <div class="card"><h3>Structural Throughput</h3><p>__VEHICLES__ Units</p></div>
            <div class="card"><h3>Localized Critical Node</h3><p>__BUSIEST__</p></div>
        </div>
    </div>
</body>
</html>"""

        html_content = html_template.replace("__TOTAL_TICKS__", total_ticks).replace("__EFFICIENCY__", efficiency_gain).replace("__VEHICLES__", total_vehicles_cleared).replace("__BUSIEST__", busiest_junction)

        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # --- 2. ACADEMIC README GENERATION ---
        repo_path = os.environ.get('GITHUB_REPOSITORY', 'your-username/your-repo')
        
        md_template = """# DATG: Decentralized Autonomous Traffic Grid 🚦🧠

DATG is an AI-assisted decentralized traffic management simulation that demonstrates how autonomous traffic nodes can collaborate through a mesh communication model to reduce congestion and improve emergency vehicle prioritization.

---

## 🏗️ System Architecture & Data Flow

```mermaid
graph TD
    A[Stochastic Traffic Generator Engine] -->|Pseudo-Random Time-Series Inflow| B(Autonomous Junction Agents)
    B -->|Mesh Communication Network Protocol| C(Adjacent Downstream Nodes)
    B -->|Asynchronous Telemetry Generation| D[Data Pipeline Matrix - CSV]
    D -->|Feature Ingestion & Supervised Training| E[Random Forest Regressor Brain]
    E -->|Serialized Predictive Weight Model - PKL| F[Live Deep Inference Loop]
    F -->|Optimal Non-Linear Signal Allocation| B

<div align="center">        
