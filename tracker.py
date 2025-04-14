from ByteTrack import ByteTrack
import numpy as np

# A simple wrapper class for ByteTrack tracker
class Tracker:
    def __init__(self):
        # Initialize the ByteTrack tracker
        self.tracker = ByteTrack()

    def update(self, detections, frame_shape):
        # Update the tracker with new detections and the frame size
        return self.tracker.update(np.array(detections), frame_shape)
