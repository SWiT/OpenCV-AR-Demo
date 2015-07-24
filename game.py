import numpy
import cv2
import math
import time


class Message:
    def __init__(self, text, expiration):
        self.text = text
        self.expiration = expiration
        self.ttl = 3
    
    def settext(self, text):
        self.text = text
        self.expiration = time.time() + self.ttl
        
    def expired(self):
        if self.expiration <= time.time():
            return True
        else:
            return False
    
class Scores:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.maxscore = 5
        self.message = Message("",0)
        
    def reset(self):
        self.score1 = 0
        self.score2 = 0
            
    
    
class Ball:
    def __init__(self, pt, color, imgw, imgh):
        self.radius = 15
        self.pt = pt
        self.color = color
        self.imgw = imgw
        self.imgh = imgh
        self.maxv = 50
        self.vel = 0    # Velocity in pixel per frame
        self.dir = 0    # Direction
        self.vx = 0
        self.vy = 0
        
    def draw(self, outputimg):
        cv2.circle(outputimg, (self.pt[0],self.pt[1]), self.radius, self.color, -1)
        
    def setpos(self, x, y):
        self.pt = (x, y)
        
    def stop(self):
        self.vel = 0
        self.dir = 0
        self.vx = 0
        self.vy = 0
        
    def reset(self):
        self.setpos(self.imgw/2, self.imgh/2)
        self.stop()
            
    def move(self):
        # Use velocity (in pixels per frame) to calculate new position.
        if self.vel > self.maxv:
            self.vel = self.maxv
        self.vx = math.cos(self.dir)*self.vel
        self.vy = math.sin(self.dir)*self.vel
        self.pt = (int(self.pt[0] + self.vx), int(self.pt[1] + self.vy))
    
    
    # Check if any of the line segments intersect with the circle.
    # http://math.stackexchange.com/questions/228841/how-do-i-calculate-the-intersections-of-a-straight-line-and-a-circle    
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle
    # http://math.stackexchange.com/questions/2837/how-to-tell-if-a-line-segment-intersects-with-a-circle/2844#2844
    def checkcollision(self, QRCodes, scores):
        
        # Check for collision with image edges.
        # Team 1 goal wall.
        if self.pt[0] < (0 + self.radius):
            print "Team 1 scored."
            scores.score1 += 1
            if scores.score1 >= scores.maxscore:
                print "Team 1 Wins!"
                scores.message.settext("Team 1 Wins!")
                scores.reset()
            self.reset()
            
        # Team 2 goal wall.
        if (self.imgw - self.radius) < self.pt[0]:
            print "Team 2 scored."
            scores.score2 += 1
            if scores.score2 >= scores.maxscore:
                print "Team 2 Wins!"
                scores.message.settext("Team 2 Wins!")
                scores.reset()
            self.setpos(self.imgw/2, self.imgh/2)
            self.stop()
            
        # Bounce off horizontal walls.
        if self.pt[1] < (0 + self.radius):
            if self.vy < 0:
                self.dir = math.atan2(-self.vy, self.vx)
        if (self.imgh - self.radius) < self.pt[1]:
            if self.vy > 0:
                self.dir = math.atan2(-self.vy, self.vx)
            
        # Check for collision with QR code.
        for qr in QRCodes.qrlist:
            # Check is ball is inside a QR code.
            if self.point_in_poly(qr.location):
                print "INSIDE"
                if self.pt[0] < self.imgw/2:
                    if self.vx < 0:
                        self.dir = math.atan2(self.vy, -self.vx)
                else:
                    if self.vx > 0:
                        self.dir = math.atan2(self.vy, -self.vx)
                        
            # Check for collision with line segment.
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
                        self.collision(qr,x1,y1,x2,y2)


    def collision(self, qr, x1, y1, x2, y2):
        # Collision! Calculate new ball velocities.
        self.vel += 5
        self.dir = math.atan2((y2 - y1), (x2 - x1)) + math.pi/2
        print "QR Collision with \""+qr.data+"\"", self.vel, self.dir
    
    def point_in_poly(self, poly):
        x = self.pt[0]
        y = self.pt[1]
        n = len(poly)
        inside = False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside    
            
            

