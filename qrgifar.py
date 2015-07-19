import numpy as np
import cv2
import zbar
import math, os
from PIL import Image

import qrcodes

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
print "\nResolution:",int(cap.get(CV_CAP_PROP_FRAME_WIDTH)),'x', int(cap.get(CV_CAP_PROP_FRAME_HEIGHT))

# Create the openCV window.
windowname = "Augmented Reality Demo: Cats in QR Codes"
cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

# Initialize the Zbar scanner
scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) # Disable all symbols.
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) # Enable just QR codes.

# Print how to quit.
print "\n\tQ or Esc to exit.\n"

QRCodes = qrcodes.QRCodes()

# Main Loop.
while(True):
    # Capture a frame from the camera, and get it's shape.
    ret, outimg = cap.read()  
    outimgh, outimgw, outimgd = outimg.shape

    # Convert to a RAW grayscale.
    gray = cv2.cvtColor(outimg, cv2.COLOR_BGR2GRAY) #convert to grayscale
    
    # Foreach QRCode already found
        # Scan the qrcode's roi
        # if found
            # update data, location, and timer
            # blank the region of the grayscaled image where the qrcode was found.
        # if not found
            # expand roi
            
    
    
    # Scan for New QR Codes.
    zbarimage = zbar.Image(outimgw, outimgh, 'Y800', gray.tostring())
    scanner.scan(zbarimage)
    # Foreach new symbol found
    for symbol in zbarimage:
        # try to update the QRCode if it exists
        i = QRCodes.update(symbol.data, symbol.location)
        if i == -1:
            # Add the QR Code
            i = QRCodes.add(symbol.data, symbol.location)
            
            
            
    # Output All QR Codes.
    for qr in QRCodes.qrlist:
        gif = qr.gif
            
        # Get the next frame of the GIF.
        gif.nextFrame()
        
        # Warp the GIF frame
        gif.warpimg(outimg, symbol)
        
        # Insert the warped Gif frame into the output image.
        outimg[gif.dminy:gif.dmaxy, gif.dminx:gif.dmaxx] = gif.warp
        
        # Draw a border around detected symbol.
        drawBorder(outimg, qr.location, colorCode[0], 2)

    # Remove Expired QRCodes
    QRCodes.removeExpired()
    
    # Display the resulting frame
    cv2.imshow(windowname, outimg)
    
    # Exit on Q or Esc.
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key ==27: 
        break

# Release the capture device and destory the windows.
cap.release()
cv2.destroyAllWindows()
