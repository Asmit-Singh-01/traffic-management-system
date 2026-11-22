import time
from typing import Dict, List


class MeshCoordinator:
    """
    Lightweight decentralized peer-to-peer state exchange layer
    for adjacent traffic junctions without a central controller.
    """

    def __init__(self, node_id: str, neighbors: List[str] | None = None):
        self.node_id = node_id
        self.neighbors = neighbors or []
        self.peer_states: Dict[str, dict] = {}

    def broadcast_state(self, queue_length: int, green_phase: int) -> dict:
        packet = {
            "sender": self.node_id,
            "timestamp": round(time.time(), 3),
            "queue_length": queue_length,
            "green_phase": green_phase,
        }
        return packet

    def receive_peer_packet(self, packet: dict) -> None:
        sender = packet.get("sender")
        if sender and sender != self.node_id:
            self.peer_states[sender] = packet

    def neighbor_pressure(self) -> float:
        if not self.peer_states:
            return 0.0
        total_q = sum(p.get("queue_length", 0) for p in self.peer_states.values())
        return round(total_q / len(self.peer_states), 2)


if __name__ == "__main__":
    j1 = MeshCoordinator("J1", neighbors=["J2"])
    j2 = MeshCoordinator("J2", neighbors=["J1"])
    pkt = j1.broadcast_state(queue_length=18, green_phase=1)
    j2.receive_peer_packet(pkt)
    print("J2 neighbor pressure:", j2.neighbor_pressure())
