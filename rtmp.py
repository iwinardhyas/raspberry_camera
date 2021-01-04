import cv2
import subprocess as sp
import numpy
from imutils.video import VideoStream

# VIDEO_URL = "/home/iwin/Documents/react/video-streaming-service/storage/live/stream/index.m3u8"
# VIDEO_URL = "http://localhost:3002/live/stream/index.m3u8"
camera1 = VideoStream("http://18.217.115.28:3002/live/stream/index.m3u8").start()

# cap = cv2.VideoCapture(VIDEO_URL)

while True:
    frame1 = camera1.read()
    # err, frame = cap.read()
    frame1 = cv2.resize(frame1,(640,480))
    print(frame1)

    cv2.imshow("GoPro",frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()