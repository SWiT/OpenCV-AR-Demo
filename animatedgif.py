import numpy as np
import cv2
from PIL import Image

class AnimatedGif:
        
    def __init__(self, filename = -1):
        self.img = 0
        self.gif = 0
        self.width = 0
        self.height = 0
        self.depth = 0
        self.warp = 0
        self.ww = 0
        self.wh = 0
        self.wd = 0
        self.dminx = -1
        self.dmaxx = -1
        self.dminy = -1
        self.dmaxy = -1
        if filename != -1:
            self.open(filename)
        return
        
    def nextFrame(self):
        try:
            self.gif.seek(self.gif.tell()+1)
        except EOFError:
            self.gif.seek(0)
        self.gif2img()
        
    def open(self, filename):
        self.gif = Image.open("gifs/"+filename)
        print "OPEN:", self.gif.format, self.gif.size, self.gif.mode
        self.img = self.gif2img()   # Convert Gif to a cvImage.
        
    def gif2img(self):
        #self.img = np.array(self.gif.convert("RGB"))
        self.img = np.array(self.gif)
        if len(self.img.shape) < 3:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        self.height, self.width, self.depth = self.img.shape
        
        
    def warpimg(self, dstimg, symbol):
        dh,dw,dd = dstimg.shape
        self.dminx = dw
        self.dmaxx = 0
        self.dminy = dh 
        self.dmaxy = 0 
        for pt in symbol.location:
            if pt[0] > self.dmaxx:
                self.dmaxx = pt[0]
            if pt[0] < self.dminx:
                self.dminx = pt[0]
            if pt[1] > self.dmaxy:
                self.dmaxy = pt[1]
            if pt[1] < self.dminy:
                self.dminy = pt[1]
        dsize = (self.dmaxx-self.dminx, self.dmaxy-self.dminy)
        pts1 = np.float32([[0,0],[0,self.height],[self.width,self.height],[self.width,0]])
        p0 = [symbol.location[0][0]-self.dminx, symbol.location[0][1]-self.dminy]
        p1 = [symbol.location[1][0]-self.dminx, symbol.location[1][1]-self.dminy]
        p2 = [symbol.location[2][0]-self.dminx, symbol.location[2][1]-self.dminy]
        p3 = [symbol.location[3][0]-self.dminx, symbol.location[3][1]-self.dminy]
        pts2 = np.float32([p0, p1, p2, p3])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        # Get the destination for the warp from the output image. 
        # This is how transparency is done without alpha channel support.
        self.warp = dstimg[self.dminy:self.dmaxy, self.dminx:self.dmaxx]  
        self.wh, self.ww, self.wd = self.warp.shape
        cv2.warpPerspective(self.img, M, dsize, dst=self.warp, borderMode=cv2.BORDER_TRANSPARENT)
        

