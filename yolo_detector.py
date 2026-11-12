import random

class YOLOTrafficDetector:
    """
    Simulated YOLOv8 / Computer Vision module for real-time vehicle 
    detection and density classification at intersection nodes.
    """
    def __init__(self):
        self.classes = ['car', 'bike', 'bus', 'truck', 'emergency_vehicle']

    def detect_vehicles(self, frame_id=1):
        """Simulate bounding box object detection feed."""
        num_detections = random.randint(10, 45)
        detections = []
        
        for _ in range(num_detections):
            cls = random.choices(self.classes, weights=[55, 25, 10, 5, 5])[0]
            confidence = round(random.uniform(0.80, 0.99), 2)
            bbox = [random.randint(0, 640), random.randint(0, 480), random.randint(40, 120), random.randint(40, 120)]
            detections.append({
                "class": cls,
                "confidence": confidence,
                "bbox": bbox
            })
            
        heavy_vehicles = sum(1 for d in detections if d['class'] in ['bus', 'truck', 'emergency_vehicle'])
        
        return {
            "frame_id": frame_id,
            "total_vehicles": len(detections),
            "heavy_vehicle_count": heavy_vehicles,
            "density_index": round(len(detections) / 50.0, 2),
            "detections": detections
        }

if __name__ == "__main__":
    detector = YOLOTrafficDetector()
    print("YOLO Detector Initialized:", detector.detect_vehicles())
  
