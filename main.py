from ultralytics import YOLO
import cv2
from collections import defaultdict
import os
from config import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN
from utils import draw_box_with_id, update_counts
from tracker import Tracker


# YOLOv8 model (you can use heavier models like yolov8s.pt)
model = YOLO("yolov8n.pt")

# Load video
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Video writer settings
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' for mp4 format
out = cv2.VideoWriter("output/people_output.mp4", fourcc, 20.0, (FRAME_WIDTH, FRAME_HEIGHT))

# Counters
people_in = defaultdict(int)
people_out = defaultdict(int)
last_positions = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame (to match VideoWriter resolution)
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Detection and tracking with YOLO + ByteTrack
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]

    for box in results.boxes:
        if int(box.cls[0]) != 0:  # Only person class (class 0)
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        track_id = int(box.id[0]) if box.id is not None else -1
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw bounding box and ID on frame
        draw_box_with_id(frame, x1, y1, x2, y2, track_id)

        # Check for entry/exit from sides
        prev = last_positions.get(track_id)
        if prev:
            px, py = prev
            for side in ['left', 'right', 'top', 'bottom']:
                update_counts(cx, cy, px, py, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN, people_in, people_out, side)

        last_positions[track_id] = (cx, cy)

    # Display entry/exit counts on frame
    y_offset = 20
    for side in ['left', 'right', 'top', 'bottom']:
        cv2.putText(frame, f"In {side}: {people_in[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
        cv2.putText(frame, f"Out {side}: {people_out[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_offset += 30

    # Show and save the video
    cv2.imshow("People Counter", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

