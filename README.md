# traffic-management-system.

# DATG: Decentralized Autonomous Traffic Grid 🚦🧠

An advanced, multi-agent AI infrastructure designed to replace static traffic light systems with a predictive, highly scalable mesh network. Built natively for cloud-execution using MLOps pipelines.

## ⚙️ Core Architecture

This system fundamentally shifts traffic management from a **Reactive Model** (waiting for queues to build up) to a **Predictive Model** (Machine Learning forecasting).

1. **Autonomous Edge Agents (`agent.py`):** Every junction acts as an independent node calculating its own dynamic optimal signal budget based on live density weights.
2. **I2I Mesh Network (`network.py`):** Infrastructure-to-Infrastructure communication. Junctions broadcast incoming vehicle loads to downstream nodes for predictive clearing.
3. **Emergency Preemption:** Built-in chaos management. Automatically detects high-priority vehicles (Ambulances/Fire trucks) and dynamically re-routes system weights to create instant Green Corridors.
4. **Automated Telemetry (`metrics.py`):** Real-time extraction of lane densities, time-allocations, and state vectors into a tabular dataset.
5. **AI Neural Brain (`ai_brain.py`):** A Random Forest Regressor trained automatically via cloud CI/CD on the generated telemetry to predict mathematically optimal signal timings.

## 🚀 Cloud Execution & CI/CD

This project requires **Zero Local Compute**. It uses GitHub Actions to run the full simulation and AI training pipeline in the cloud.

### Pipeline Workflow:
1. Provisions an Ubuntu Linux server.
2. Installs Data Science dependencies (`pandas`, `scikit-learn`).
3. Executes `simulation.py` to generate real-time `traffic_telemetry.csv`.
4. Triggers `ai_brain.py` to ingest the dataset and output a trained `ai_model.pkl`.
5. Uploads the dataset and trained model as downloadable artifacts.

## 🧠 State Space & Telemetry Matrix
The system tracks the following vectors per simulation tick:
`Timestamp` | `Junction_ID` | `Directional_Density (N,S,E,W)` | `Selected_Priority_Lane` | `Hold_Time` | `Outflow`

---
*Built with Python, Scikit-Learn, and GitHub Actions.*
