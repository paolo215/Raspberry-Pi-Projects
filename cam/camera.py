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
        pass

    @abstractmethod
    def record(self, seconds):
        pass

    @abstractmethod
    def record_continuous_save_every(self, seconds):

        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def take_picture(self):
        pass

    @abstractmethod
    def take_picture_every(self, seconds):
        pass

    def generate_filename(self, extension):
        now = datetime.datetime.now()
        now_full_str = now.strftime("%m-%d-%Y %H:%M")
        now_date_str = now.strftime("%m-%d-%Y")
        folder_path = "./%s/%s" % (self.prefix, now_date_str)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = folder_path + "/" + now_date_str + "." + extension
        return file_path



        

