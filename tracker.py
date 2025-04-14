from supervision.tracker.byte_tracker import ByteTrack
import numpy as np

class Tracker:
    def __init__(self):
        self.tracker = ByteTrack()

    def update(self, detections, frame_shape):
        return self.tracker.update(np.array(detections), frame_shape)
