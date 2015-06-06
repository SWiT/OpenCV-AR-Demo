import numpy as np
import cv2
import zbar
import math, os
from PIL import Image

import animatedgif

CV_CAP_PROP_FRAME_WIDTH     = 3
CV_CAP_PROP_FRAME_HEIGHT    = 4

colorCode = ((255,0,0), (0,240,0), (0,0,255), (29,227,245), (224,27,217)) #Blue, Green, Red, Yellow, Purple

def drawBorder(img, symbol, color, thickness):
    cv2.line(img, symbol[0], symbol[1], color, thickness)
    cv2.line(img, symbol[1], symbol[2], color, thickness)
    cv2.line(img, symbol[2], symbol[3], color, thickness)
    cv2.line(img, symbol[3], symbol[0], color, thickness)

# Initialize the camera.        
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720)
print
print "Resolution:",int(cap.get(CV_CAP_PROP_FRAME_WIDTH)),'x', int(cap.get(CV_CAP_PROP_FRAME_HEIGHT))

# Create the openCV window.
windowname = "Augmented Reality Demo: Cats in QR Codes"
cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

# Initialize the Zbar scanner
scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) # Disable all symbols.
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) # Enable just QR codes.

# Get the list of all gif's in the gif folder.
gifidx = 1
giflist = os.listdir("gifs")
if len(giflist) == 0:
    quit("Error:No GIF files were found in gifs/.")
print giflist

# Open the Gif.
gif = animatedgif.AnimatedGif(giflist[gifidx])

# Print how to quit.
print "\n\tQ or Esc to exit.\n"

# Main Loop.
while(True):
    # Capture a frame from the camera, and get it's shape.
    ret, outimg = cap.read()  
    outimgh, outimgw, outimgd = outimg.shape

    # Convert to a RAW grayscale and scan for QR Codes.
    gray = cv2.cvtColor(outimg, cv2.COLOR_BGR2GRAY) #convert to grayscale
    zbarimage = zbar.Image(outimgw, outimgh, 'Y800', gray.tostring())
    scanner.scan(zbarimage)
    for symbol in zbarimage:
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        #print symbol.location
        
        # Draw a border around detected symbols.
        drawBorder(outimg, symbol.location, colorCode[0], 2)
        
        # Get the next frame of the GIF.
        gif.nextFrame()
        
        # Warp the GIF frame
        gif.warpimg(outimg, symbol)
        
        # Insert the warped Gif frame into the output image.
        outimg[gif.dminy:gif.dmaxy, gif.dminx:gif.dmaxx] = gif.warp

    # Display the resulting frame
    cv2.imshow(windowname, outimg)
    
    # Exit on Q or Esc.
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key ==27: 
        break

# Release the capture device and destory the windows.
cap.release()
cv2.destroyAllWindows()
