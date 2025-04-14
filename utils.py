import cv2

def draw_box_with_id(frame, x1, y1, x2, y2, track_id):
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

def update_counts(cx, cy, px, py, frame_w, frame_h, margin, in_counts, out_counts, side):
    if side == "left":
        if px < margin and cx >= margin:
            in_counts["left"] += 1
        elif px >= margin and cx < margin:
            out_counts["left"] += 1
    elif side == "right":
        if px > frame_w - margin and cx <= frame_w - margin:
            in_counts["right"] += 1
        elif px <= frame_w - margin and cx > frame_w - margin:
            out_counts["right"] += 1
    elif side == "top":
        if py < margin and cy >= margin:
            in_counts["top"] += 1
        elif py >= margin and cy < margin:
            out_counts["top"] += 1
    elif side == "bottom":
        if py > frame_h - margin and cy <= frame_h - margin:
            in_counts["bottom"] += 1
        elif py <= frame_h - margin and cy > frame_h - margin:
            out_counts["bottom"] += 1
