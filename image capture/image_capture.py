import threading
import cv2
import time


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


# capture an image every 1 hour
def capture_image():
    vidcap = cv2.VideoCapture(0)
    success, image = vidcap.read()
    if success:
        cv2.imwrite("images/frame_" + time.strftime("%Y%m%d-%H%M%S") + ".jpg", image)  # save frame as JPEG file
    vidcap.release()


# set up the timer
capture_image()
timer = set_interval(capture_image, 3600)