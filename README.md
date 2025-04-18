# People Tracking with YOLOv8 and ByteTrack

This project demonstrates how to use YOLOv8 for object detection and ByteTrack for real-time tracking of people in a video. The main goal is to detect and track people, and count how many people enter and exit the scene from specific boundaries (left, right, top, and bottom).

## Features

- **YOLOv8 for Object Detection:** Detects people in each frame of the video.
- **ByteTrack for Object Tracking:** Tracks each person detected across frames.
- **Entry/Exit Counting:** Counts how many people enter or exit the scene from the defined boundaries.

## Requirements

Before running the project, ensure that you have the following libraries installed:

### Dependencies

- Python (3.8 or higher)
- `opencv-python` – For video processing.
- `torch` – For running YOLOv8.
- `numpy` – For handling arrays and computations.
- `matplotlib` – For visualizing results (optional).
- `ByteTrack` – For object tracking.

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/PeopleTracking.git
cd PeopleTracking
```
Create a Virtual Environment (Optional but Recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install dependencies:
Install the required Python libraries:
```bash
pip install opencv-python torch numpy matplotlib
```

## Clone and install ByteTrack:
Clone the ByteTrack repository and install its dependencies:
```bash
git clone https://github.com/ifzhang/ByteTrack.git
cd ByteTrack
pip install -r requirements.txt
```

## Download YOLOv8 Weights:
```bash
pip install ultralytics
```

## Project Structure
```
plaintext
PeopleTracking/
│
├── ByteTrack/               # ByteTrack repository (tracking code)
│
├── main.py                  # Main script to run detection and tracking
│
├── README.md                # This file
│
├── yolov8_weights.pt        # YOLOv8 weights file (downloaded)
│
└── requirements.txt         # Optional, if you want to freeze dependencies
```

