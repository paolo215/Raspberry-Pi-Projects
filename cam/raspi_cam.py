import numpy as np
import time
import cv2
import datetime
import sys

from camera import Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction

# Raspberry Pi Camera Module With IR
class RaspberryPiCamera(Camera):
    def __init__(self, prefix, resolution):
        super().__init__(prefix, resolution)
        self.camera = PiCamera()
        self.set_resolution(self.resolution) 

    def set_resolution(self, resolution):
        self.camera.resolution = resolution
    
    def record(self, seconds):
        try:
            filename = self.generate_filename("h264", "videos")
            self.camera.start_preview()
            self.camera.start_recording(filename)
            self.camera.wait_recording(seconds)
            self.camera.stop_recording()
            self.camera.stop_preview()
            return filename
        except KeyboardInterrupt:
            print("Keyboard Interrupt - Closing Camera")
            self.stop()

    def record_continuous_save_every(self, seconds):
        try:
            while True:
                filename = self.record(seconds)
                print(filename) 
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

    def take_picture_every(self, seconds):
        try:
            while True:
                filename = self.take_picture()
                time.sleep(seconds)
                print(filename) 
        except KeyboardInterrupt:
            print("KeyboardInterrupt - Closing Camera")
            self.stop()

if __name__ == "__main__":
    a = RaspberryPiCamera("test", (640, 480))
    #a.take_picture_every(10)
    a.record_continuous_save_every(10)


