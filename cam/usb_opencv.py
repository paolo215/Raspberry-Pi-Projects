import os
import datetime
import cv2
import time
import datetime
import sys

from camera import Camera
from queue import Queue
from threading import Thread

class USB_OpenCV(Camera):
    def __init__(self, prefix, resolution, stream=False):
        super().__init__(prefix, resolution)
        self.camera = cv2.VideoCapture(0)
        self.set_resolution(self.resolution)
        self.fourcc = cv2.VideoWriter_fourcc(*"MPEG")
        self.writer = None

        # Only for recording videos
        self.current_frame = None

    def set_resolution(self, resolution):
        # Reference:
        # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
        # 3 = width
        # 4 = height
        self.camera.set(3, resolution[0])
        self.camera.set(4, resolution[1])

    def get_frame(self):
        if self.camera.isOpened():
            return self.camera.read()
        return None

    def collect_frames(self):
        while True:
            return_value, frame = self.get_frame()
            if return_value:
                self.current_frame = frame

    def show_frame(self, image):
        cv2.imshow("Frame", image)
        cv2.waitKey(1)
        
    def write_frame(self, writer, image):
        self.writer.write(image)
        
    def start_record(self, seconds):
        t1 = Thread(target=self.collect_frames)
        t2 = Thread(target=self.record_continuous_save_every, args=(seconds,))
        threads = [t1, t2]

        for t in threads:
            t.daemon = True
            t.start()
        
        for t in threads:
            t.join()


    def record(self, seconds):
        try:
            start = time.time()
            filename = self.generate_filename("avi", "video")
            print(filename)
            self.writer = self.createVideoWriter(filename)
            while time.time() - start < seconds \
                and self.camera.isOpened():
                image = self.current_frame
                if image != None:
                    self.show_frame(image)
        except KeyboardInterrupt:
            self.stop()

        print("END")
        return None


    def record_continuous_save_every(self, seconds):
        try:
            while True:
                self.record(seconds)
        except KeyboardInterrupt:
            self.stop()


    def stop(self):
        self.camera.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
        print("Exiting...")
        sys.exit(1)

    def take_picture(self):
        try:
            filename = self.generate_filename("jpg", "pics")
            if self.camera.isOpened():
                return_value, image = self.camera.read()
                if return_value == True:
                    cv2.imwrite(filename, image)
                    cv2.imshow("Frame", image)
                    cv2.waitKey(1)
                    return filename
        except KeyboardInterrupt:
            self.stop()
        return None 

    def take_picture_every(self, seconds):
        try:
            while True:
                start = time.time()
                while time.time() - start and \
                    self.camera.isOpened():
                    self.take_picture()
        except KeyboardInterrupt:
            self.stop()

    def createVideoWriter(self, filename):
        return cv2.VideoWriter(filename, self.fourcc, 30.0, self.resolution)


if __name__ == "__main__":
    a = USB_OpenCV("test", (640, 480)) 
    #a.record_continuous_save_every(60*10)
    a.start_record(60)
    #a.take_picture_every(10)
    #a.take_picture()