import numpy as np
import time
import cv2
import datetime
import sys

from camera import Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction
from threading import Thread

# Raspberry Pi Camera Module With IR
class RaspberryPiCamera(Camera):
    def __init__(self, prefix, resolution):
        super().__init__(prefix, resolution)
        self.camera = PiCamera()
        self.set_resolution(self.resolution) 
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.writer = cv2.VideoWriter("output.avi", self.fourcc, 20.0, resolution)

    def set_resolution(self, resolution):
        self.camera.resolution = resolution
    
    def get_frame(self):
        self.camera.capture(self.raw_capture, format="bgr")
        frame = self.raw_capture.array
        self.raw_capture.truncate(0)
        return frame

    def collect_frames(self):
        while True:
            self.current_frame = self.get_frame()


    def record(self, seconds):
        try:
            start = time.time()
            filename = self.generate_filename("avi", "video")
            print(filename)
            while time.time() - start < seconds:
                image = self.current_frame
                if image is not None:
                    self.show_frame(image)

        except KeyboardInterrupt:
            print("Keyboard Interrupt - Closing Camera")
            self.stop()

    def stop(self):
        self.camera.close()
        sys.exit(1)

    def take_picture(self):
        try:
            filename = self.generate_filename("jpg", "pictures")
            self.camera.start_preview()
            self.camera.capture(filename)
            self.camera.stop_preview()
            return filename
        except KeyboardInterrupt:
            print("Keyboard Interrupt. Closing Camera.")
            self.stop()

    def show_frame(self, image):
        cv2.imshow("Frame", image)
        cv2.waitKey(1)

    def take_picture_every(self, seconds):
        try:
            while True:
                filename = self.take_picture()
                time.sleep(seconds)
                print(filename) 
        except KeyboardInterrupt:
            print("KeyboardInterrupt - Closing Camera")
            self.stop()

    def isOpened(self):
        if self.camera:
            return not self.camera.closed
        return False

if __name__ == "__main__":
    a = RaspberryPiCamera("test", (640, 480))
    #a.take_picture_every(10)
    a.start_record(10)


