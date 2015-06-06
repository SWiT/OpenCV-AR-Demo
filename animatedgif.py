import numpy as np
import cv2
from PIL import Image

class AnimatedGif:
        
    def __init__(self, filename = -1):
        self.frameidx = 0
        self.timelastused = 0
        self.img = 0
        self.gif = 0
        self.width = 0
        self.height = 0
        self.depth = 0
        self.warp = 0
        self.ww = 0
        self.wh = 0
        self.wd = 0
        if filename != -1:
            self.open(filename)
        return
        
    def nextFrame(self):
        self.frameidx += 1
        try:
            self.gif.seek(self.frameidx)
        except EOFError:
            self.frameidx = 0
            self.gif.seek(self.frameidx)
        self.gif2img()
        
    def open(self, filename = -1):
        if filename != -1:
            self.gif = Image.open("gifs/"+filename)
        self.img = self.gif2img()   # Convert Gif to a cvImage.

        
    def gif2img(self):
        self.img = np.array(self.gif)
        if len(self.img.shape) < 3:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        self.height, self.width, self.depth = self.img.shape

