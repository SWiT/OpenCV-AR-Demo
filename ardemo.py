import numpy as np
import cv2
import zbar
import math
from PIL import Image

CV_CAP_PROP_FRAME_WIDTH     = 3
CV_CAP_PROP_FRAME_HEIGHT    = 4

colorCode = ((255,0,0), (0,240,0), (0,0,255), (29,227,245), (224,27,217)) #Blue, Green, Red, Yellow, Purple


def drawBorder(img, symbol, color, thickness):
    cv2.line(img, symbol[0], symbol[1], color, thickness)
    cv2.line(img, symbol[1], symbol[2], color, thickness)
    cv2.line(img, symbol[2], symbol[3], color, thickness)
    cv2.line(img, symbol[3], symbol[0], color, thickness)

def findCenter(pts):
    x = 0
    y = 0
    for i in range(0,len(pts)):
        x += pts[i][0]
        y += pts[i][1]
    return (int(x/len(pts)), int(y/len(pts)))
    
def gif2img(g):
    img = np.array(g)
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) 
    return img
        
        
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720)
print
print "\tResolution:",int(cap.get(CV_CAP_PROP_FRAME_WIDTH)),'x', int(cap.get(CV_CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow('AR_Demo', cv2.WINDOW_NORMAL)

scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) #disable all symbols
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) #enable QR codes

gif = Image.open("gifs/surprise-kitten.gif")
gifimg = gif2img(gif)
gifidx = 0

print "\tQ or Esc to exit."
print

while(True):
    # Capture a frame from the camera, and get it's shape.
    ret, outimg = cap.read()  
    outimgh, outimgw, outimgd = outimg.shape

    # Get the next frame of the GIF.
    try:
        gif.seek(gifidx)
        gifimg = gif2img(gif)
        gifidx += 1
    except EOFError:
        gifidx = 0
        gif.seek(gifidx)
        gifimg = gif2img(gif)
    gifimgh, gifimgw, gifimgd = gifimg.shape
        
    # Our operations on the frame come here
    gray = cv2.cvtColor(outimg, cv2.COLOR_BGR2GRAY) #convert to grayscale
    zbarimage = zbar.Image(outimgw, outimgh, 'Y800', gray.tostring())
    scanner.scan(zbarimage)
    for symbol in zbarimage:
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        #print symbol.location
        drawBorder(outimg, symbol.location, colorCode[0], 2)
        
        # Warp the GIF frame
        maxx = 0
        maxy = 0 
        minx = outimgw
        miny = outimgh 
        for pt in symbol.location:
            if pt[0] > maxx:
                maxx = pt[0]
            if pt[0] < minx:
                minx = pt[0]
            if pt[1] > maxy:
                maxy = pt[1]
            if pt[1] < miny:
                miny = pt[1]
        dsize = (maxx-minx, maxy-miny)
        pts1 = np.float32([[0,0],[0,gifimgh],[gifimgw,gifimgh],[gifimgw,0]])
        p0 = [symbol.location[0][0]-minx, symbol.location[0][1]-miny]
        p1 = [symbol.location[1][0]-minx, symbol.location[1][1]-miny]
        p2 = [symbol.location[2][0]-minx, symbol.location[2][1]-miny]
        p3 = [symbol.location[3][0]-minx, symbol.location[3][1]-miny]
        pts2 = np.float32([p0, p1, p2, p3])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        gifwarp = outimg[miny:maxy, minx:maxx]
        cv2.warpPerspective(gifimg,M,dsize, dst=gifwarp, borderMode=cv2.BORDER_TRANSPARENT)
        gifwarph,gifwarpw,gifwarpd = gifwarp.shape
        
        # Insert the GIF frame
        x,y = findCenter(symbol.location)
        x -= gifwarpw/2
        y -= gifwarph/2
        gx0 = 0
        gx1 = gifwarpw
        gy0 = 0
        gy1 = gifwarph
        if x+gifwarpw > outimgw:
            gx1 = outimgw - x
        if x < 0:
            x = 0
            gx0 = 0
        if y+gifwarph > outimgh:
            gy1 = outimgh - y
        if y < 0:
            y = 0
            gy0 = 0
        outimg[y:(y+gy1), x:(x+gx1)] = gifwarp[gy0:gy1, gx0:gx1]
        
    # Display the resulting frame
    cv2.imshow('AR_Demo', outimg)
    
    #Exit on Q or Esc
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key ==27: 
        break

# Release the capture, destory the windows
cap.release()
cv2.destroyAllWindows()
