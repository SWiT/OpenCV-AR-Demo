import numpy as np
import cv2
import zbar
import math, os
from PIL import Image

import animatedgif

CV_CAP_PROP_FRAME_WIDTH     = 3
CV_CAP_PROP_FRAME_HEIGHT    = 4

windowname = "Augmented Reality Demo: Cats in QR Codes"
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
        
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720)
print
print "\tResolution:",int(cap.get(CV_CAP_PROP_FRAME_WIDTH)),'x', int(cap.get(CV_CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) #disable all symbols
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) #enable QR codes

# Get the list of all gif's in the gif folder.
gifidx = 0
giflist = os.listdir("gifs")
if len(giflist) == 0:
    quit("Error:No GIF files were found in gifs/.")
print giflist

# Open the Gif.
gif = animatedgif.AnimatedGif(giflist[gifidx])

print "\tQ or Esc to exit."
print

while(True):
    # Capture a frame from the camera, and get it's shape.
    ret, outimg = cap.read()  
    outimgh, outimgw, outimgd = outimg.shape

    # Get the next frame of the GIF.
    gif.nextFrame()
        
    # Our operations on the frame come here
    gray = cv2.cvtColor(outimg, cv2.COLOR_BGR2GRAY) #convert to grayscale
    zbarimage = zbar.Image(outimgw, outimgh, 'Y800', gray.tostring())
    scanner.scan(zbarimage)
    for symbol in zbarimage:
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        #print symbol.location
        drawBorder(outimg, symbol.location, colorCode[0], 2)
        
        # Warp the GIF frame
        gif.warpimg(outimg, symbol)
        # Insert the warped Gif frame into the output image.
        outimg[gif.dminy:gif.dmaxy, gif.dminx:gif.dmaxx] = gif.warp

        
        
    # Display the resulting frame
    cv2.imshow(windowname, outimg)
    
    #Exit on Q or Esc
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key ==27: 
        break

# Release the capture, destory the windows
cap.release()
cv2.destroyAllWindows()
