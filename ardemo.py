import numpy as np
import cv, cv2
import zbar

cap = cv2.VideoCapture(0)

print cap.get(cv.CV_CAP_PROP_FRAME_WIDTH),cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
print cap.get(cv.CV_CAP_PROP_FRAME_WIDTH),cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

cv2.namedWindow('AR_Demo', cv2.WINDOW_NORMAL)

scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0) #disable all symbols
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1) #enable QR codes

print
print "Q to exit."
print

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    height, width, depth = frame.shape
    
    # Our operations on the frame come here
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    raw = frame.tostring()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    for symbol in image:
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        
    # Display the resulting frame
    cv2.imshow('AR_Demo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
