import numpy
import cv2
import math


class Ball:
    def __init__(self, pt, color, imgw, imgh):
        self.radius = 25
        self.pt = pt
        self.color = color
        self.imgw = imgw
        self.imgh = imgh
        self.vx = 0
        self.vy = 0
        
    def draw(self, outputimg):
        cv2.circle(outputimg, (self.pt[0],self.pt[1]), self.radius, self.color, -1)
        
    def setpos(self, x, y):
        self.pt = (x, y)
        
    def stop(self):
        self.vx = 0
        self.vy = 0
    
    def move(self):
        # Use velocity to calculate new position.
        self.pt = (self.pt[0] + self.vx, self.pt[1] + self.vy)
    
    def collision(self, qr):
        # Collision! Calculate new ball velocities.
        self.vx = qr.vx + self.vx
        self.vy = qr.vy + self.vy
        #print "Collision",self.vx,self.vy
    
    
    # Check if any of the line segments intersect with the circle.
    # http://math.stackexchange.com/questions/228841/how-do-i-calculate-the-intersections-of-a-straight-line-and-a-circle    
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle/2844#2844
    def checkcollision(self, QRCodes):
        # Check for collision with image edges.
        if self.pt[0] < (0 + self.radius) or (self.imgw - self.radius) < self.pt[0]:
            print "past X"
            self.setpos(self.imgw/2, self.imgh/2)
            self.stop()
        
        # Check for collision with QR code.
        for qr in QRCodes.qrlist:
            for idx1 in range(0,4): 
                idx2 = 0 if (idx1==3) else idx1+1
                x1 = qr.location[idx1][0]
                y1 = qr.location[idx1][1]
                x2 = qr.location[idx2][0]
                y2 = qr.location[idx2][1]
                
                # Equation for the line segment
                # y - y1 = m * (x - x1)
                # y = m * x - (m * x1) + y1
                if x1 != x2:
                    m = (y2-y1)/(x2-x1)
                else:
                    m = 0.001    # This is a terrible hack.
                c = y1 - (m * x1)
                
                # Equation for the circle
                # (x - p)^2 + (y - q)^2 = r^2
                p = self.pt[0]
                q = self.pt[1]
                r = self.radius
                
                # Ax^2 + Bx + C = 0
                A = (m*m+1)
                B = 2*(m*c - m*q - p)
                C = (q*q - r*r + p*p - 2*c*q + c*c)
                
                discriminant = B*B - 4*A*C
                if discriminant >= 0:
                    x_1 = (-B + math.sqrt(discriminant))/(2*A)
                    y_1 = m*x_1 + c
                    x_2 = (-B - math.sqrt(discriminant))/(2*A)
                    y_2 = m*x_2 + c
                    if (x1 <= x_1 <= x2) or (x1>= x_1 >= x2) or (x1 <= x_2 <= x2) or (x1>= x_2 >= x2):
                        self.collision(qr)
                    
            #print
            
            
            
            

