# In this file we address things to avoid hard coding

# Video or RTSP path settings
VIDEO_SOURCE = "data/people.mp4"  # or 'rtsp://user:pass@ip:port'
MODEL_PATH = "yolov8n.pt"
FRAME_WIDTH = 640
FRAME_HEIGHT = 360
BOUNDARY_MARGIN = 20  # Margin area for entry/exit

# Custom zone definition (for zone-based counting)
TOP_ZONE = {
    "name": "Zone Blue",
    "color": (255, 0, 0),  # BGR
    "rect": (300, 120, 440, 200)  # x1, y1, x2, y2
}
