# THE IF STATEMENT OF THE PROGRAM IS RIGHT HERE >>> Here we check who came in or out 

import cv2

# Function to draw bounding box and track ID on the frame
def draw_box_with_id(frame, x1, y1, x2, y2, track_id):
    # Draw a rectangle on the frame around the detected object
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    # Display the track ID above the bounding box
    cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Function to update counts of people entering and exiting through boundaries
def update_counts(cx, cy, px, py, frame_w, frame_h, margin, in_counts, out_counts, side):
    # Check for "left" side boundary crossing
    if side == "left":
        if px < margin and cx >= margin:  # Person crosses into the left side
            in_counts["left"] += 1
        elif px >= margin and cx < margin:  # Person crosses out from the left side
            out_counts["left"] += 1
    # Check for "right" side boundary crossing
    elif side == "right":
        if px > frame_w - margin and cx <= frame_w - margin:  # Person crosses into the right side
            in_counts["right"] += 1
        elif px <= frame_w - margin and cx > frame_w - margin:  # Person crosses out from the right side
            out_counts["right"] += 1
    # Check for "top" side boundary crossing
    elif side == "top":
        if py < margin and cy >= margin:  # Person crosses into the top side
            in_counts["top"] += 1
        elif py >= margin and cy < margin:  # Person crosses out from the top side
            out_counts["top"] += 1
    # Check for "bottom" side boundary crossing
    elif side == "bottom":
        if py > frame_h - margin and cy <= frame_h - margin:  # Person crosses into the bottom side
            in_counts["bottom"] += 1
        elif py <= frame_h - margin and cy > frame_h - margin:  # Person crosses out from the bottom side
            out_counts["bottom"] += 1
