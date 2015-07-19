import time, os
import animatedgif

class QRCode:
    def __init__(self, data, filename, location, imgh, imgw):
        self.timelastseen = time.time()
        self.data = data
        self.filename = filename
        self.gif = animatedgif.AnimatedGif(self.filename)
        self.imgh = imgh
        self.imgw = imgw
        # 0:top left, 1:bottom left, 2:bottom right, 3: top right
        # (x, y)
        self.location = []  
        self.roi = []
        self.updatelocation(location)
        
    def updatelocation(self, location):
        self.location = location
        # Calculate region of interest.
        xmin = self.imgw
        xmax = 0
        ymin = self.imgh
        ymax = 0
        for idx,point in enumerate(self.location):
            if point[0] > xmax:
                xmax = point[0]
            if point[0] < xmin:
                xmin = point[0]
            if point[1] > ymax:
                ymax = point[1]
            if point[1] < ymin:
                ymin = point[1]
        diff = 90
        ymax += diff
        if ymax >= self.imgh:
            ymax = self.imgh-1
        ymin -= diff
        if ymin < 0:
            ymin = 0
        xmax += diff
        if xmax >= self.imgw:
            xmax = self.imgw-1
        xmin -= diff
        if xmin < 0:
            xmin = 0
        self.roi = ((xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin))
        
class QRCodes:
    def __init__(self, imgh, imgw):
        self.qrlist = []
        self.expiretime = 1
        self.imgh = imgh
        self.imgw = imgw
        # Get the list of all gif's in the gif folder.
        self.gifidx = 0
        self.giflist = os.listdir("gifs")
        if len(self.giflist) == 0:
            quit("Error:No GIF files were found in gifs/.")
        print self.giflist,"\n"
        
    def update(self, data, location):
        for i,qr in enumerate(self.qrlist):
            if qr.data == data:
                qr.timelastseen = time.time()
                qr.updatelocation(location)
                return i
        return -1
        
    def add(self, data, location):
        giffilename = self.giflist[self.gifidx]
        self.qrlist.append(QRCode(data, giffilename, location, self.imgh, self.imgw))
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
                
            
