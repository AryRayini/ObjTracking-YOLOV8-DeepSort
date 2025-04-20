import cv2

# Zone A configuration
def get_zone_a_line(frame_width, frame_height):
    line_y = frame_height - 20
    start_x = frame_width // 2 - 70
    end_x = frame_width // 2 + 30
    return start_x, end_x, line_y

# Draw Zone A label (and optionally the line itself)
def draw_zone_a(frame, start_x, end_x, line_y, show_line=False):
    if show_line:
        cv2.line(frame, (start_x, line_y), (end_x, line_y), (0, 0, 255), 2)
    cv2.putText(frame, "A", (start_x - 25, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# Check if a tracked person has crossed the Zone A line
def check_zone_a_crossing(cx, cy, prev_pos, start_x, end_x, line_y, track_id, counted_ids):
    px, py = prev_pos
    if ((py < line_y <= cy) or (py > line_y >= cy)) and (start_x < cx < end_x):
        if track_id not in counted_ids["zone_a"]:
            counted_ids["zone_a"].add(track_id)
            return True
    return False
