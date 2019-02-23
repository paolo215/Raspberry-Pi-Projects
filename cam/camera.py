import os
import datetime

from abc import ABC
from abc import abstractmethod

class Camera(ABC):
    def __init__(self, prefix, resolution):
        self.prefix = prefix
        self.resolution = resolution

    @abstractmethod
    def set_resolution(self, resolution):
        raise NotImplementedError("")

    @abstractmethod
    def record(self, seconds):
        raise NotImplementedError("")

    @abstractmethod
    def record_continuous_save_every(self, seconds):
        raise NotImplementedError("")

    @abstractmethod
    def stop(self):
        raise NotImplementedError("")

    @abstractmethod
    def take_picture(self):
        raise NotImplementedError("")

    @abstractmethod
    def take_picture_every(self, seconds):
        raise NotImplementedError("")

    def generate_filename(self, extension, sub_folder="misc/"):
        now = datetime.datetime.now()
        now_full_str = now.strftime("%m-%d-%Y_%H:%M:%S")
        now_date_str = now.strftime("%m-%d-%Y")
        folder_path = "./%s/%s/%s" % (self.prefix, now_date_str, sub_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = folder_path + "/" + now_full_str + "." + extension
        return file_path



        

