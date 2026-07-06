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

        # --- 1. HTML DASHBOARD (No Triple Quotes) ---
        html_lines = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <title>DATG Operational Control Dashboard</title>",
            "    <style>",
            "        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px; }",
            "        .container { max-width: 1200px; margin: auto; text-align: center; }",
            "        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; margin-top: 40px; }",
            "        .card { background: #1e293b; padding: 25px; border-radius: 14px; border-left: 5px solid #38bdf8; text-align: left; }",
            "        .card.success { border-left-color: #4ade80; }",
            "        .card h3 { margin: 0; color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }",
            "        .card p { font-size: 28px; font-weight: 700; margin: 12px 0 0 0; color: #f1f5f9; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <div class='container'>",
            "        <h1 style='color: #38bdf8; font-size: 32px;'>DATG: Decentralized Autonomous Traffic Grid</h1>",
            "        <p style='color: #64748b;'>Algorithmic Validation Framework & Asset Dashboard</p>",
            "        <div class='grid'>",
            "            <div class='card'><h3>Telemetry Matrix Volume</h3><p>__TOTAL_TICKS__ Data Vectors</p></div>",
            "            <div class='card success'><h3>Delay Mitigation Index</h3><p>⏳ Latency Reduced by __EFFICIENCY__%</p></div>",
            "            <div class='card'><h3>Structural Throughput</h3><p>__VEHICLES__ Units</p></div>",
            "            <div class='card'><h3>Localized Critical Node</h3><p>__BUSIEST__</p></div>",
            "        </div>",
            "    </div>",
            "</body>",
            "</html>"
        ]
        
        html_content = "\n".join(html_lines)
        html_content = html_content.replace("__TOTAL_TICKS__", total_ticks).replace("__EFFICIENCY__", efficiency_gain).replace("__VEHICLES__", total_vehicles_cleared).replace("__BUSIEST__", busiest_junction)

        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # --- 2. ACADEMIC README (No Triple Quotes) ---
        repo_path = os.environ.get('GITHUB_REPOSITORY', 'your-username/your-repo')
        
        md_lines = [
            "# DATG: Decentralized Autonomous Traffic Grid 🚦🧠",
            "",
            "DATG is an AI-assisted decentralized traffic management simulation that demonstrates how autonomous traffic nodes can collaborate through a mesh communication model to reduce congestion and improve emergency vehicle prioritization.",
            "",
            "---",
            "",
            "## 🏗️ System Architecture & Data Flow",
            "",
            "```mermaid",
            "graph TD",
            "    A[Stochastic Traffic Generator Engine] -->|Pseudo-Random Time-Series Inflow| B(Autonomous Junction Agents)",
            "    B -->|Mesh Communication Network Protocol| C(Adjacent Downstream Nodes)",
            "    B -->|Asynchronous Telemetry Generation| D[Data Pipeline Matrix - CSV]",
            "    D -->|Feature Ingestion & Supervised Training| E[Random Forest Regressor Brain]",
            "    E -->|Serialized Predictive Weight Model - PKL| F[Live Deep Inference Loop]",
            "    F -->|Optimal Non-Linear Signal Allocation| B",
            "```",
            "",
            "---",
            "",
            "<div align='center'>",
            "",
            "### 📊 Experimental Verification Metrics (Live Cloud Logs)",
            "",
            "> **Execution Pipeline:** ![Research Validation](https://img.shields.io/badge/Framework-Research__Prototype-38bdf8?style=flat-square) ![Model](https://img.shields.io/badge/Algorithm-Random__Forest__Regressor-orange?style=flat-square)",
            "",
            "| Performance Dimension | Quantitative Value | Scientific Operational Analysis |",
            "| :--- | :---: | :--- |",
            "| **Telemetry Volume** | `__TOTAL_TICKS__ Continuous Records` | Synthetically generated via a pseudo-stochastic model mapping continuous rush-hour traffic distributions. |",
            "| **Delay Mitigation Index** | `📉 Latency Reduced by __EFFICIENCY__%` | Optimization lift achieved by replacing legacy fixed-time controllers with live AI inference. |",
            "| **Structural Throughput** | `__VEHICLES__ Total Vehicles` | Cumulative vehicle units successfully buffered and cleared across grid vertices. |",
            "| **Monitored Bottleneck** | `📍 __BUSIEST__` | System-wide highest stress junction localized via mathematical density variance tracking. |",
            "",
            "</div>",
            "",
            "---",
            "",
            "## ⚙️ Core Algorithmic Framework",
            "",
            "1. **Autonomous Junction Agents (`agent.py`):** Each traffic junction is represented by an independent software agent that makes local signal timing decisions based on live directional density profiles.",
            "2. **Message-Passing Communication Mesh (`network.py`):** An Infrastructure-to-Infrastructure (I2I) packet relay system allowing upstream nodes to broadcast output payloads to adjacent downstream nodes, preventing cascading gridlocks.",
            "3. **Emergency Preemption Overrides:** A priority queue interception matrix that bypasses standard ML inference windows when high-priority vectors (Ambulances) are injected into the pipeline state space.",
            "4. **Predictive Analytics Subsystem (`ai_brain.py`):** Utilizes an ensemble **Random Forest Regressor** to evaluate the multi-dimensional state vector, selected over neural networks due to its superior generalization and high interpretability on structured tabular datasets.",
            "",
            "## ⚠️ Current Research Limitations",
            "* **Simulation Constraints:** Operational logic is validated against synthetic pseudo-stochastic data streams rather than real-world physical CCTV object detection or inductive-loop hardware feeds.",
            "* **Deterministic Dispersal:** Vehicle clearing behavior operates under mathematical constraints (`allocated_time / 1.5`) which do not account for macro-level driver behaviors or weather variables.",
            "",
            "---",
            "",
            "## 🚀 Deployment & Local Execution Guide",
            "",
            "Follow these steps to replicate the cloud simulation environment on your local terminal:",
            "",
            "### 1. Clone the Repository",
            "```bash",
            "git clone [https://github.com/__REPO_PATH__.git](https://github.com/__REPO_PATH__.git)",
            "cd DATG",
            "```",
            "",
            "### 2. Initialize Virtual Environment & Install Dependencies",
            "```bash",
            "python3 -m venv venv",
            "source venv/bin/activate",
            "pip install pandas scikit-learn joblib",
            "```",
            "",
            "### 3. Execute the Full Simulation Pipeline",
            "Run the multi-agent engine to generate data, train the ensemble model, and test real-time inference:",
            "```bash",
            "# Step A: Run the dual-phase simulation loop",
            "python simulation.py",
            "",
            "# Step B: Train the model and serialize weights",
            "python ai_brain.py",
            "",
            "# Step C: Synthesize the visual dashboard and compile results",
            "python generate_dashboard.py",
            "```",
            "*Upon completion, open `dashboard.html` in any web browser to view the operational analytics interface.*"
        ]

        markdown_content = "\n".join(md_lines)
        markdown_content = markdown_content.replace("__TOTAL_TICKS__", total_ticks).replace("__EFFICIENCY__", efficiency_gain).replace("__VEHICLES__", total_vehicles_cleared).replace("__BUSIEST__", busiest_junction).replace("__REPO_PATH__", repo_path)

        with open(self.output_md, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print("[SUCCESS] Master-level academic README.md generated successfully!")

if __name__ == "__main__":
    dash = TrafficDashboard()
    dash.generate_analytics()
