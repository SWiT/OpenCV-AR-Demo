import numpy as np
import cv2
import zbar
import math, os
from PIL import Image

import qrcodes

CV_CAP_PROP_FRAME_WIDTH     = 3
CV_CAP_PROP_FRAME_HEIGHT    = 4

# Blue, Green, Red, Yellow, Magenta, Cyan
def colorCode(color):
    color = color.lower()
    if color == "blue":
        return (255,0,0)
    elif color == "green":
        return (0,255,0)
    elif color == "red":
        return (0,0,255)
    elif color == "yellow":
        return (0,255,255)
    elif color == "magenta":
        return (255,0,255)
    elif color == "cyan":
        return (255,255,0)

def drawBorder(img, points, color, thickness):
    for idx0,point in enumerate(points):
        if idx0+1 >= len(points):
            idx1 = 0
        else:
            idx1 = idx0+1
        cv2.line(img, points[idx0], points[idx1], colorCode(color), thickness)
    
# Initialize the camera.        
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720)

print "\nResolution:", int(cap.get(CV_CAP_PROP_FRAME_WIDTH)), 'x', int(cap.get(CV_CAP_PROP_FRAME_HEIGHT))

# Create the openCV window.
windowname = "Augmented Reality Demo: Cats in QR Codes"
cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

# Initialize the Zbar scanner
scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) # Disable all symbols.
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) # Enable just QR codes.

# Print how to quit.
print "\n\tQ or Esc to exit.\n"

QRCodes = qrcodes.QRCodes(int(cap.get(CV_CAP_PROP_FRAME_HEIGHT)), int(cap.get(CV_CAP_PROP_FRAME_WIDTH)))

# Main Loop.
while(True):
    # Capture a frame from the camera, and get it's shape.
    ret, outimg = cap.read()  
    outimgh, outimgw, outimgd = outimg.shape

    # Convert to a RAW grayscale.
    gray = cv2.cvtColor(outimg, cv2.COLOR_BGR2GRAY) #convert to grayscale
    
    
    # Foreach QRCode already found scan the qrcode's roi.
    numfound = 0
    for qr in QRCodes.qrlist:
        roi = gray[qr.ymin:qr.ymax, qr.xmin:qr.xmax]
        h,w = roi.shape
        zbarimage = zbar.Image(w, h, 'Y800', roi.tostring())
        scanner.scan(zbarimage)
        for symbol in zbarimage:
            # If found update with offset.
            if symbol.data == qr.data:
                i = QRCodes.update(symbol.data, symbol.location, True)
                numfound += 1
                #print "\"%s\" UPDATED!" % qr.data
                
                # Blank the region of the grayscaled image where the qrcode was found.
                poly = np.array(qr.location, np.int32)
                cv2.fillConvexPoly(gray, poly, 0)
            
            
    # If too few QR Codes were found Scan for new QR Codes.
    if numfound < 2:
        zbarimage = zbar.Image(outimgw, outimgh, 'Y800', gray.tostring())
        scanner.scan(zbarimage)
        # Foreach new symbol found
        for symbol in zbarimage:
            # try to update the QRCode if it exists
            i = QRCodes.update(symbol.data, symbol.location)
            if i == -1:
                # Add the QR Code
                i = QRCodes.add(symbol.data, symbol.location)
            else:
                #print '"%s" updated' % symbol.data
                pass
                
    # Remove Expired QRCodes
    QRCodes.removeExpired()
    
    # Output All QR Codes.
    for qr in QRCodes.qrlist:
        # Get the QRCode's GIF
        gif = qr.gif
        # Get the next frame of the GIF.
        gif.nextFrame()
        # Warp the GIF frame and insert the warped Gif into the output image.
        gif.warpimg(outimg, qr)
        
        # Draw a border around symbol.
        if qr.data == "A":
            color = "blue"
        elif qr.data == "B":
            color = "green"
        elif qr.data == "C":
            color = "red"
        elif qr.data == "D":
            color = "yellow"
        else:
            color = "magenta"
        drawBorder(outimg, qr.location, color, 6)
        drawBorder(outimg, qr.roi, "cyan", 1)

    # Draw Circle
    pt = (300,300)
    color = (0,0,255)
    cv2.circle(outimg, (pt[0],pt[1]), 18, color, -1)
    cv2.circle(outimg, (pt[0]+34,pt[1]), 18, color, -1)
    poly = ((pt[0]-17,pt[1]),(pt[0]+34,pt[1]),(pt[0]+18,pt[1]+50))
    poly = np.array(poly, np.int32)
    cv2.fillConvexPoly(outimg, poly, color)
    
    
    # Display the resulting frame
    cv2.imshow(windowname, outimg)
    
    # Exit on Q or Esc.
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key ==27: 
        break

# Release the capture device and destory the windows.
cap.release()
cv2.destroyAllWindows()
