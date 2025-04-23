import cv2

# 📦 Draw a bounding box around a detected person and label it with the track ID
# This function draws a rectangle around the detected object and displays its track ID
def draw_box_with_id(frame, x1, y1, x2, y2, track_id):
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)  # Draw a green rectangle around the object
    cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  # Display the ID above the rectangle

# 🔁 Check and update whether a person entered or exited through a specific side
# This function checks if a person entered or exited from one of the sides of the frame and updates the counts accordingly
def update_counts(cx, cy, px, py, frame_w, frame_h, margin,
                  in_counts, out_counts, side, track_id, counted_ids):

    # Check if this action has already been counted for the given side
    def has_not_been_counted(action):
        return f"{action}_{side}" not in counted_ids[track_id]

    # Check entry/exit from the left side of the frame
    if side == "left":
        if px < margin and cx >= margin and has_not_been_counted("in"):
            in_counts["left"] += 1
            counted_ids[track_id].add("in_left")
        elif px >= margin and cx < margin and has_not_been_counted("out"):
            out_counts["left"] += 1
            counted_ids[track_id].add("out_left")

    # Check entry/exit from the right side of the frame
    elif side == "right":
        if px > frame_w - margin and cx <= frame_w - margin and has_not_been_counted("in"):
            in_counts["right"] += 1
            counted_ids[track_id].add("in_right")
        elif px <= frame_w - margin and cx > frame_w - margin and has_not_been_counted("out"):
            out_counts["right"] += 1
            counted_ids[track_id].add("out_right")

    # Check entry/exit from the top of the frame
    elif side == "top":
        if py < margin and cy >= margin and has_not_been_counted("in"):
            in_counts["top"] += 1
            counted_ids[track_id].add("in_top")
        elif py >= margin and cy < margin and has_not_been_counted("out"):
            out_counts["top"] += 1
            counted_ids[track_id].add("out_top")

    # Check entry/exit from the bottom of the frame
    elif side == "bottom":
        if py > frame_h - margin and cy <= frame_h - margin and has_not_been_counted("in"):
            in_counts["bottom"] += 1
            counted_ids[track_id].add("in_bottom")
        elif py <= frame_h - margin and cy > frame_h - margin and has_not_been_counted("out"):
            out_counts["bottom"] += 1
            counted_ids[track_id].add("out_bottom")

# This function checks if a point (like the center of a bounding box) is inside a specified rectangular zone
def is_inside_zone(cx, cy, zone_rect):
    x1, y1, x2, y2 = zone_rect
    return x1 <= cx <= x2 and y1 <= cy <= y2
