import supervision as sv 
from config import *
imy = sv.VideoInfo.from_video_path(VIDEO_SOURCE)
print(imy)