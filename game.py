import numpy
import cv2



class Ball:
    def __init__(self, pt, color):
        self.radius = 20
        self.pt = pt
        self.color = color
        self.vx = 0
        self.vy = 0
        
    def draw(self, outputimg):
        cv2.circle(outputimg, (self.pt[0],self.pt[1]), self.radius, self.color, -1)
        
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle/2844#2844
    def checkcollision(self, QRCodes):
        for qr in QRCodes.qrlist:
            pts = qr.location
            for i1 in range(0,4): 
                i2 = 0 if (i1==3) else i1+1
                x1 = pts[i1][0]
                y1 = pts[i1][1]
                x2 = pts[i2][0]
                y2 = pts[i2][1]
                
                # Equation for the line segment
                # y - y1 = m * (x - x1)
                # y = m * x - (m * x1) + y1
                if x1 != x2:
                    m = (y2-y1)/(x2-x1)
                else:
                    m = 0.001    
                c = y1 - (m * x1)
                
                # Equation for the circle
                # (x - p)^2 + (y - q)^2 = r^2
                p = self.pt[0]
                q = self.pt[1]
                r = self.radius
                
                A = (m*m+1)
                B = 2*(m*c - m*q - p)
                C = (q*q - r*r + p*p - 2*c*q + c*c)
                
                if (B*B - 4*A*C) >= 0:
                    print "Maybe"
                else:
                    print "No"
               
                
                
            #print
