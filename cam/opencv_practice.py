
# References
#  https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

# Captures a frame
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array
# cv2.imshow("Image", image)
# cv2.waitKey(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) 

	rawCapture.truncate(0)
