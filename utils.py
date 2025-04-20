import cv2

# 📦 Draw a bounding box around a detected person and label it with the track ID
def draw_box_with_id(frame, x1, y1, x2, y2, track_id):
    # Draw the rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    # Draw the ID above the top-left corner of the bounding box
    cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# 🔁 Check and update whether a person entered or exited through a specific side
def update_counts(cx, cy, px, py, frame_w, frame_h, margin,
                  in_counts, out_counts, side, track_id, counted_ids):

    # Helper to make sure an event isn't counted multiple times
    def has_not_been_counted(action):
        return f"{action}_{side}" not in counted_ids[track_id]

    # 👈 Check for entry/exit through the left side
    if side == "left":
        if px < margin and cx >= margin and has_not_been_counted("in"):
            in_counts["left"] += 1
            counted_ids[track_id].add("in_left")
        elif px >= margin and cx < margin and has_not_been_counted("out"):
            out_counts["left"] += 1
            counted_ids[track_id].add("out_left")

    # 👉 Check for entry/exit through the right side
    elif side == "right":
        if px > frame_w - margin and cx <= frame_w - margin and has_not_been_counted("in"):
            in_counts["right"] += 1
            counted_ids[track_id].add("in_right")
        elif px <= frame_w - margin and cx > frame_w - margin and has_not_been_counted("out"):
            out_counts["right"] += 1
            counted_ids[track_id].add("out_right")

    # 🔼 Check for entry/exit through the top side
    elif side == "top":
        if py < margin and cy >= margin and has_not_been_counted("in"):
            in_counts["top"] += 1
            counted_ids[track_id].add("in_top")
        elif py >= margin and cy < margin and has_not_been_counted("out"):
            out_counts["top"] += 1
            counted_ids[track_id].add("out_top")

    # 🔽 Check for entry/exit through the bottom side
    elif side == "bottom":
        if py > frame_h - margin and cy <= frame_h - margin and has_not_been_counted("in"):
            in_counts["bottom"] += 1
            counted_ids[track_id].add("in_bottom")
        elif py <= frame_h - margin and cy > frame_h - margin and has_not_been_counted("out"):
            out_counts["bottom"] += 1
            counted_ids[track_id].add("out_bottom")
