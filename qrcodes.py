import time, os
import animatedgif

class QRCode:
    def __init__(self, data, filename, location):
        self.timelastseen = time.time()
        self.data = data
        self.filename = filename
        self.gif = animatedgif.AnimatedGif(self.filename)
        self.location = location
        self.roi = []
        
class QRCodes:
    def __init__(self):
        self.qrlist = []
        self.expiretime = 2
        # Get the list of all gif's in the gif folder.
        self.gifidx = 0
        self.giflist = os.listdir("gifs")
        if len(self.giflist) == 0:
            quit("Error:No GIF files were found in gifs/.")
        print self.giflist
        
    def update(self, data, location):
        for i,qr in enumerate(self.qrlist):
            if qr.data == data:
                qr.timelastseen = time.time()
                qr.location = location
                return i
        return -1
        
    def add(self, data, location):
        self.qrlist.append(QRCode(data, self.giflist[self.gifidx], location))
        self.gifidx += 1
        if self.gifidx >= len(self.giflist):
            self.gifidx = 0
        
        print '"%s" added' % data
        return len(self.qrlist)-1
        
    def removeExpired(self):
        for qr in self.qrlist:
            if (time.time() - qr.timelastseen) > self.expiretime:
                print '"%s" expired' % qr.data
                self.qrlist.remove(qr)
                
            
