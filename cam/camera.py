import os
import datetime
import cv2

from abc import ABC
from abc import abstractmethod
from threading import Thread

class Camera(ABC):
    def __init__(self, prefix, resolution):
        self.prefix = prefix
        self.resolution = resolution
        self.current_frame = None

    @abstractmethod
    def set_resolution(self, resolution):
        raise NotImplementedError("")

    @abstractmethod
    def record(self, seconds):
        raise NotImplementedError("")

    def record_continuous_save_every(self, seconds):
        try:
            while True:
                if self.isOpened():
                    self.record(seconds)
        except KeyboardInterrupt:
            self.stop()

    @abstractmethod
    def stop(self):
        raise NotImplementedError("")

    @abstractmethod
    def take_picture(self):
        raise NotImplementedError("")

    def take_picture_every(self, seconds):
        try:
            while True:
                start = time.time()
                while time.time() - start and self.isOpened():
                    self.take_picture()
        except KeyboardInterrupt:
            self.stop()

    @abstractmethod
    def get_frame(self):
        raise NotImplementedError("")
    
    @abstractmethod
    def collect_frames(self):
        raise NotImplementedError("")
    
    @abstractmethod
    def isOpened(self):
        raise NotImplementedError("")

    def start_record(self, seconds):
        t1 = Thread(target=self.collect_frames)
        t2 = Thread(target=self.record_continuous_save_every, args=(seconds, ))
        threads = [t1, t2]

        for t in threads:
            t.daemon = True
            t.start()

        for t in threads:
            t.join()


    def generate_filename(self, extension, sub_folder="misc/"):
        now = datetime.datetime.now()
        now_full_str = now.strftime("%m-%d-%Y_%H:%M:%S")
        now_date_str = now.strftime("%m-%d-%Y")
        folder_path = "./%s/%s/%s" % (self.prefix, now_date_str, sub_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = folder_path + "/" + now_full_str + "." + extension
        return file_path

    def show_frame(self, image):
        cv2.imshow("Frame", image)
        cv2.waitKey(1)


        

