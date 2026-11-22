import json
import os
from typing import List


def compute_latency_reduction(baseline_delay: float, current_delay: float) -> float:
    if baseline_delay <= 0:
        return 0.0
    reduction = ((baseline_delay - current_delay) / baseline_delay) * 100.0
    return round(reduction, 2)


def load_telemetry(filepath: str = "telemetry.json") -> dict:
    default_data = {
        "steps": 20,
        "avg_queue_delay": 31.2,
        "peak_throughput": 185,
        "latest_delays": [36.0, 34.0, 32.0, 33.0, 31.0, 30.5, 31.2],
        "recovery_ticks": 12,
    }
    if not os.path.exists(filepath):
        return default_data
    with open(filepath, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    return {**default_data, **loaded}


def summarize_series(values: List[float]) -> dict:
    if not values:
        return {"min": 0.0, "max": 0.0, "avg": 0.0}
    return {
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "avg": round(sum(values) / len(values), 2),
    }


if __name__ == "__main__":
    data = load_telemetry()
    print("Reduction vs 42.8s baseline:", compute_latency_reduction(42.8, data["avg_queue_delay"]))

