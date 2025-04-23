from ultralytics import YOLO
import cv2
from collections import defaultdict
import os
from config import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN, TOP_ZONE
from utils import draw_box_with_id, update_counts, is_inside_zone

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize video capture
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Output video setup
os.makedirs("output", exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output/people_outputnew2.mp4", fourcc, 20.0, (FRAME_WIDTH, FRAME_HEIGHT))

# Tracking and count data
people_in = defaultdict(int)
people_out = defaultdict(int)
last_positions = {}
counted_ids = defaultdict(set)

# Zone-specific counts and memory
zone_in = 0
zone_out = 0
was_in_zone = {}
zone_fully_counted_ids = set()

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]

    for box in results.boxes:
        if int(box.cls[0]) != 0:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        track_id = int(box.id[0]) if box.id is not None else -1
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        draw_box_with_id(frame, x1, y1, x2, y2, track_id)

        # Entry/exit logic (frame sides)
        prev = last_positions.get(track_id)
        if prev:
            px, py = prev
            for side in ['left', 'right', 'top', 'bottom']:
                update_counts(cx, cy, px, py, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN,
                              people_in, people_out, side, track_id, counted_ids)

        # --- Zone-specific logic ---
        zx1, zy1, zx2, zy2 = TOP_ZONE["rect"]
        currently_in_zone = is_inside_zone(cx, cy, TOP_ZONE["rect"])

        # Remember: only count if they were inside before and now exited vertically
        if track_id in was_in_zone:
            if was_in_zone[track_id] and not currently_in_zone and track_id not in zone_fully_counted_ids:
                if cy < zy1:
                    zone_out += 1
                    zone_fully_counted_ids.add(track_id)
                elif cy > zy2:
                    zone_in += 1
                    zone_fully_counted_ids.add(track_id)
        else:
            # If track_id is new, just track whether they are in the zone or not
            was_in_zone[track_id] = currently_in_zone

        # Update zone memory
        was_in_zone[track_id] = currently_in_zone
        last_positions[track_id] = (cx, cy)

    # Display general side counts
    y_offset = 20
    for side in ['left', 'right', 'top', 'bottom']:
        cv2.putText(frame, f"In {side}: {people_in[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
        cv2.putText(frame, f"Out {side}: {people_out[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_offset += 30

    # Draw zone and zone counts
    zx1, zy1, zx2, zy2 = TOP_ZONE["rect"]
    cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), TOP_ZONE["color"], 2)

    cv2.putText(frame, f"{TOP_ZONE['name']} In: {zone_in}", (zx1, zy2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, TOP_ZONE["color"], 2)
    cv2.putText(frame, f"{TOP_ZONE['name']} Out: {zone_out}", (zx1, zy2 + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, TOP_ZONE["color"], 2)

    # Show frame
    cv2.imshow("People Counter", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()
