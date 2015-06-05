import numpy as np
import cv2
import zbar
from PIL import Image

CV_CAP_PROP_FRAME_WIDTH     = 3
CV_CAP_PROP_FRAME_HEIGHT    = 4

colorCode = ((255,0,0), (0,240,0), (0,0,255), (29,227,245), (224,27,217)) #Blue, Green, Red, Yellow, Purple

def drawBorder(img, symbol, color, thickness):
    cv2.line(img, symbol[0], symbol[1], color, thickness)
    cv2.line(img, symbol[1], symbol[2], color, thickness)
    cv2.line(img, symbol[2], symbol[3], color, thickness)
    cv2.line(img, symbol[3], symbol[0], color, thickness)

cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720)
print cap.get(CV_CAP_PROP_FRAME_WIDTH), cap.get(CV_CAP_PROP_FRAME_HEIGHT)

cv2.namedWindow('AR_Demo', cv2.WINDOW_NORMAL)

scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) #disable all symbols
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) #enable QR codes


def gif2bgr(gifimg):
    gifframe = np.array(gifimg)
    if len(gifframe.shape) == 2:
        gifframe = cv2.cvtColor(gifframe, cv2.COLOR_GRAY2BGR) 
    return gifframe
gifimg = Image.open("gifs/surprise-kitten.gif")
gifframe = gif2bgr(gifimg)
gifframeindex = 0


print
print "Q to exit."
print

while(True):
    # Capture a frame
    ret, outputframe = cap.read()

    height, width, depth = outputframe.shape

    try:
        gifimg.seek(gifframeindex)
        gifframe = gif2bgr(gifimg)
        gifframeindex += 1
    except EOFError:
        gifframeindex = 0
        gifimg.seek(gifframeindex)
        gifframe = gif2bgr(gifimg)
    
        
    # Our operations on the frame come here
    gray = cv2.cvtColor(outputframe, cv2.COLOR_BGR2GRAY) #convert to grayscale
    image = zbar.Image(width, height, 'Y800', gray.tostring())
    scanner.scan(image)
    for symbol in image:
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print symbol.location
        drawBorder(outputframe, symbol.location, colorCode[0], 2)
        
    # Display the resulting frame
    cv2.imshow('AR_Demo', outputframe)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
