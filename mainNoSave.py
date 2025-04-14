from ultralytics import YOLO
import cv2
from collections import defaultdict
from config import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN
from utils import draw_box_with_id, update_counts

# YOLOv8 model with ByteTrack support
model = YOLO("yolov8n.pt")  # You can use a heavier model like yolov8s.pt
cap = cv2.VideoCapture(VIDEO_SOURCE)

# People count for entering and exiting
people_in = defaultdict(int)
people_out = defaultdict(int)
last_positions = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Tracking using the model
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]

    # Processing detected boxes
    for box in results.boxes:
        if int(box.cls[0]) != 0:  # Only people
            continue

        # Box coordinates and tracking ID
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        track_id = int(box.id[0]) if box.id is not None else -1
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw the box and tracking ID
        draw_box_with_id(frame, x1, y1, x2, y2, track_id)

        # Check previous position and update counts
        prev = last_positions.get(track_id)
        if prev:
            px, py = prev
            for side in ['left', 'right', 'top', 'bottom']:
                update_counts(cx, cy, px, py, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN, people_in, people_out, side)

        last_positions[track_id] = (cx, cy)

    # Display the count of people entering and exiting from each side
    y_offset = 20
    for side in ['left', 'right', 'top', 'bottom']:
        cv2.putText(frame, f"In {side}: {people_in[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
        cv2.putText(frame, f"Out {side}: {people_out[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_offset += 30

    # Display the frame
    cv2.imshow("People Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
