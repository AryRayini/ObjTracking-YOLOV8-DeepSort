# import supervision as sv 
# from config import *
# imy = sv.VideoInfo.from_video_path(VIDEO_SOURCE)
# print(imy)

import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: ({x}, {y})")  # Print coordinates when left button is clicked

def display_image(image_path):
    frame = cv2.imread(image_path)  # Load image

    # Create a window and bind the function to it
    cv2.namedWindow("Select Zone")
    cv2.setMouseCallback("Select Zone", click_event)

    while True:
        cv2.imshow("Select Zone", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press Q to quit
            break

    cv2.destroyAllWindows()
