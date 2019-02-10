
# References
#  https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

# helps construct n-dimensional numpy array from camera output
from picamera.array import PiRGBArray

# For using Raspberry Pi Camera
from picamera import PiCamera

import time

# computer vision
import cv2

# set up
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow camera to warm up
time.sleep(0.1)

# Captures a frame
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array
# cv2.imshow("Image", image)
# cv2.waitKey(0)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw numpy array representing the image
	image = frame.array

	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) 

	# clear the stream
	rawCapture.truncate(0)