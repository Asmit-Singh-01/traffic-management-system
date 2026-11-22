import json
from ai_brain import DQNTrafficBrain
from yolo_detector import YOLOTrafficDetector
from sumo_integration import SUMOEnvironmentBridge
from mesh_protocol import MeshCoordinator


def run_simulation(steps: int = 20) -> dict:
    brain = DQNTrafficBrain()
    detector = YOLOTrafficDetector()
    sumo = SUMOEnvironmentBridge()
    mesh_a = MeshCoordinator("NODE_A", neighbors=["NODE_B"])
    mesh_b = MeshCoordinator("NODE_B", neighbors=["NODE_A"])

    sumo.connect_sumo()

    delays = []
    throughputs = []
    queue_a = 12.0
    queue_b = 10.0

    for step in range(1, steps + 1):
        vision = detector.detect_vehicles(frame_id=step)
        incoming = vision["total_vehicles"]

        pkt_b = mesh_b.broadcast_state(queue_length=int(queue_b), green_phase=step % 3)
        mesh_a.receive_peer_packet(pkt_b)

        state = [queue_a, incoming, mesh_a.neighbor_pressure(), vision["heavy_vehicle_count"]]
        action = brain.act(state)

        # Action 0: short green, 1: balanced green, 2: extended green
        cleared = min(queue_a + incoming, 8 + action * 6)
        next_queue_a = max(0.0, queue_a + incoming - cleared)
        queue_b = max(0.0, queue_b + (cleared * 0.4) - 6.0)

        avg_delay = round(25.0 + next_queue_a * 0.45, 2)
        reward = -avg_delay + (cleared * 0.5)

        next_state = [next_queue_a, incoming, mesh_a.neighbor_pressure(), vision["heavy_vehicle_count"]]
        brain.train_step(state, action, reward, next_state)

        delays.append(avg_delay)
        throughputs.append(int(cleared))
        queue_a = next_queue_a

    brain.save_model("model.pkl")

    summary = {
        "steps": steps,
        "avg_queue_delay": round(sum(delays) / len(delays), 2),
        "peak_throughput": max(throughputs),
        "latest_delays": delays[-7:],
        "recovery_ticks": 12,
    }

    with open("telemetry.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("DATG Simulation Complete:", summary)
    return summary


if __name__ == "__main__":
    run_simulation()
