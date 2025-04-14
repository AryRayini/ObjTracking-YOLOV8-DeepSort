from ultralytics import YOLO
import cv2
from collections import defaultdict
from config import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN
from utils import draw_box_with_id, update_counts

# مدل YOLOv8 با پشتیبانی از ByteTrack
model = YOLO("yolov8n.pt")  # می‌تونی مدل سنگین‌تر هم بذاری
cap = cv2.VideoCapture(VIDEO_SOURCE)

people_in = defaultdict(int)
people_out = defaultdict(int)
last_positions = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # رهگیری با استفاده از مدل
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]

    for box in results.boxes:
        if int(box.cls[0]) != 0:  # فقط اشخاص
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        track_id = int(box.id[0]) if box.id is not None else -1
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        draw_box_with_id(frame, x1, y1, x2, y2, track_id)

        prev = last_positions.get(track_id)
        if prev:
            px, py = prev
            for side in ['left', 'right', 'top', 'bottom']:
                update_counts(cx, cy, px, py, FRAME_WIDTH, FRAME_HEIGHT, BOUNDARY_MARGIN, people_in, people_out, side)

        last_positions[track_id] = (cx, cy)

    y_offset = 20
    for side in ['left', 'right', 'top', 'bottom']:
        cv2.putText(frame, f"In {side}: {people_in[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
        cv2.putText(frame, f"Out {side}: {people_out[side]}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_offset += 30

    cv2.imshow("People Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
