import math
import pytest
from metrics import (
    calculate_mae,
    calculate_average_queue_delay,
    calculate_peak_flow_throughput,
    calculate_baseline_improvement,
    TelemetryLogger,
)


def test_calculate_mae_known_values():
    assert calculate_mae([30, 45, 60], [28, 50, 58]) == pytest.approx(3.0)

def test_calculate_mae_empty():
    with pytest.raises(ValueError):
        calculate_mae([], [])

def test_calculate_mae_mismatched_length():
    with pytest.raises(ValueError):
        calculate_mae([1, 2], [1])

def test_calculate_mae_malformed_strings():
    with pytest.raises(ValueError):
        calculate_mae(["a", "b"], [1, 2])

def test_average_queue_delay_zero_traffic():
    rows = [{
        "North_Density": 0, "South_Density": 0,
        "East_Density": 0, "West_Density": 0,
        "Outflow_Throughput": 0,
    }]
    assert calculate_average_queue_delay(rows) == 0.0

def test_average_queue_delay_gridlock():
    rows = [{
        "North_Density": 400, "South_Density": 400,
        "East_Density": 400, "West_Density": 400,
        "Outflow_Throughput": 0,
    }]
    assert math.isinf(calculate_average_queue_delay(rows))

def test_queue_delay_under_300_percent_stress():
    baseline = [{
        "North_Density": 25, "South_Density": 25,
        "East_Density": 25, "West_Density": 25,
        "Outflow_Throughput": 20,
    }]
    stressed = [{
        "North_Density": 100, "South_Density": 100,
        "East_Density": 100, "West_Density": 100,
        "Outflow_Throughput": 20,
    }]
    normal_delay = calculate_average_queue_delay(baseline)
    stress_delay = calculate_average_queue_delay(stressed)
    assert stress_delay == pytest.approx(normal_delay * 4)

def test_peak_flow_sums_junctions_per_tick():
    rows = [
        {"Timestamp_Tick": 1, "Outflow_Throughput": 10},
        {"Timestamp_Tick": 1, "Outflow_Throughput": 15},
        {"Timestamp_Tick": 2, "Outflow_Throughput": 40},
        {"Timestamp_Tick": 2, "Outflow_Throughput": 20},
    ]
    assert calculate_peak_flow_throughput(rows) == 60

def test_queue_delay_rejects_missing_fields():
    rows = [{
        "North_Density": 10, "South_Density": 10,
        "East_Density": 10,
        "Outflow_Throughput": 5,
    }]
    with pytest.raises(ValueError, match="West_Density"):
        calculate_average_queue_delay(rows)

def test_baseline_improvement_higher_is_better():
    assert calculate_baseline_improvement(185, 140, higher_is_better=True) == pytest.approx(32.142857, rel=1e-4)

def test_baseline_improvement_lower_is_better():
    assert calculate_baseline_improvement(31.2, 42.8, higher_is_better=False) == pytest.approx(27.1028, rel=1e-3)

def test_logger_creates_csv_with_header(tmp_path):
    path = tmp_path / "telemetry.csv"
    logger = TelemetryLogger(filename=str(path))
    assert path.exists()
    header = path.read_text().splitlines()[0]
    assert "Timestamp_Tick" in header

def test_logger_appends_row(tmp_path):
    path = tmp_path / "telemetry.csv"
    logger = TelemetryLogger(filename=str(path))

    class FakeAgent:
        agent_id = "abc123"
        location_name = "Node_Test"
        lanes = {"North": 1, "South": 2, "East": 3, "West": 4}

    decision = {"selected_lane": "North", "hold_time": 15, "outflow": 5}
    logger.log_step(1, FakeAgent(), decision)

    lines = path.read_text().splitlines()
    assert len(lines) == 2
    assert "Node_Test" in lines[1]

def test_logger_does_not_erase_existing_csv(tmp_path):
    path = tmp_path / "telemetry.csv"
    logger1 = TelemetryLogger(filename=str(path))

    class FakeAgent:
        agent_id = "abc123"
        location_name = "Node_Test"
        lanes = {"North": 1, "South": 2, "East": 3, "West": 4}

    logger1.log_step(1, FakeAgent(), {"selected_lane": "North", "hold_time": 15, "outflow": 5})

    logger2 = TelemetryLogger(filename=str(path))  # re-init pointing at same file
    lines_after_reinit = path.read_text().splitlines()
    assert len(lines_after_reinit) == 2  # header + 1 row still there, not wiped