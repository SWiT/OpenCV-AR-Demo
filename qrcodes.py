import time, os
import animatedgif

class QRCode:
    def __init__(self, d, fn):
        self.timelastseen = time.time()
        self.data = d
        self.gif = animatedgif.AnimatedGif(fn)
        
class QRCodes:
    def __init__(self):
        self.found = []
        # Get the list of all gif's in the gif folder.
        self.gifidx = 0
        self.giflist = os.listdir("gifs")
        if len(self.giflist) == 0:
            quit("Error:No GIF files were found in gifs/.")
        print self.giflist
        
    def index(self, val):
        for i,qr in enumerate(self.found):
            if qr.data == val:
                qr.timelastseen = time.time()
                return i
        return -1
        
    def add(self, val):
        self.found.append(QRCode(val, self.giflist[self.gifidx]))
        self.gifidx += 1
        if self.gifidx >= len(self.giflist):
            self.gifidx = 0
        return len(self.found)-1
        
    def removeExpired(self):
        for qr in self.found:
            if (time.time() - qr.timelastseen) > 3:
                self.found.remove(qr)
                print "expired."
            
