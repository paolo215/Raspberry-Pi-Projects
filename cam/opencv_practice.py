
# References
#  https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

# helps construct n-dimensional numpy array from camera output
from picamera.array import PiRGBArray

# For using Raspberry Pi Camera
from picamera import PiCamera

import numpy as np

import time

# computer vision
import cv2

from fractions import Fraction

# set up
resolution = (640, 480)
# resolution = (1280, 720)
camera = PiCamera()
camera.resolution = resolution
#camera.rotation = -90
#camera.framerate = Fraction(1,6)
camera.framerate_range = (Fraction(3, 6), 1)
camera.shutter_speed = 2000000
camera.brightness = 55
camera.annotate_frame_num = True
camera.sensor_mode = 3
camera.awb_mode = "sunlight"
camera.iso = 1600
rawCapture = PiRGBArray(camera, size=resolution)
#camera = cv2.VideoCapture(0)

#fourcc = cv2.cv.CV_FOURCC(*"XVID")
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, resolution)

print("Warming up")
# allow camera to warm up
time.sleep(10)
camera.exposure_mode = "verylong"



# Captures a frame
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array
# cv2.imshow("Image", image)
# cv2.waitKey(0)

# capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw numpy array representing the image
#     image = frame.array
# 
#     # show the frame
#     cv2.imshow("Frame", image)
#     key = cv2.waitKey(1) 
# 
#     # clear the stream
#     rawCapture.truncate(0)

#face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #while True:
        #ret, image = camera.read()
        image = frame.array
        print(np.average(image))
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        #print("Found " + str(len(faces)))

        #for (x, y, w, h) in faces:
        #    cv2.rectangle(gray, (x,y), (x+w,y+h), (255, 0,0), 2)

        out.write(image)
        cv2.imshow("Frame", image)
        cv2.waitKey(1) & 0xff
        rawCapture.truncate(0)

except Exception as e:
    print(e)
    pass
except KeyboardInterrupt:
    pass


cv2.destroyAllWindows()
out.release()
camera.close()
print("closed")



