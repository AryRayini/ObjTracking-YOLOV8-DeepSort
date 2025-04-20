from ultralytics import YOLO
import cv2
from collections import defaultdict
import os
from config import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN
from utils import draw_box_with_id, update_counts
## from utils_zone_A import get_zone_a_line, draw_zone_a, check_zone_a_crossing

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize video capture
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Prepare output video writer
os.makedirs("output", exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output/people.mp4", fourcc, 20.0, (FRAME_WIDTH, FRAME_HEIGHT))

# Initialize tracking and counting data
people_in = defaultdict(int)
people_out = defaultdict(int)
last_positions = {}
counted_ids = defaultdict(set)
zone_a_count = 0

# Get Zone A coordinates
## start_x, end_x, line_y = get_zone_a_line(FRAME_WIDTH, FRAME_HEIGHT)

# Main video processing loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to desired resolution
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Drawing Zone A Label
    ## draw_zone_a(frame, start_x, end_x, line_y, show_line=False)  

    # Perform object detection + tracking with YOLO + ByteTrack
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]

    for box in results.boxes:
        # Skip non-person detections (class 0 = person)
        if int(box.cls[0]) != 0:
            continue

        # Get bounding box and center point
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        track_id = int(box.id[0]) if box.id is not None else -1
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw bounding box and ID on frame
        draw_box_with_id(frame, x1, y1, x2, y2, track_id)

        # Update boundary-based entry/exit counters
        prev = last_positions.get(track_id)
        if prev:
            px, py = prev
            for side in ['left', 'right', 'top', 'bottom']:
                update_counts(cx, cy, px, py, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN,
                              people_in, people_out, side, track_id, counted_ids)
                
            # Check Zone A crossing
            ##if check_zone_a_crossing(cx, cy, prev, start_x, end_x, line_y, track_id, counted_ids):
                ##zone_a_count += 1

        # Save current position for next frame
        last_positions[track_id] = (cx, cy)

    # Display in/out counts for each frame edge
    y_offset = 20
    for side in ['left', 'right', 'top', 'bottom']:
        cv2.putText(frame, f"In {side}: {people_in[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
        cv2.putText(frame, f"Out {side}: {people_out[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_offset += 30

    # Display Zone A counter in bottom-right corner
    ##label = f"A: {zone_a_count}"
    ##text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    ##text_x = FRAME_WIDTH - text_size[0] - 10
    ##text_y = FRAME_HEIGHT - 10
    ##cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show processed frame and write to output video
    cv2.imshow("People Counter", frame)
    out.write(frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
