import math
from cv2 import VideoCapture
import cvzone
import numpy as np
import cv2
from math import hypot 
from cvzone.HandTrackingModule import HandDetector 


cap=VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


class snakeclas:
    def __init__(self):
        self.point=[] #all pointt of the snake
        self.lenghts=[] #distance between each point
        self.currentlength=0 #totale length of the snake
        self.allowedlength=150 #total allowedlenght
        self.previoseHead=0,0
    def update(self,imgMain,currentHead):
        px,py=self.previoseHead
        cx,cy=currentHead
        self.point.append([cx,cy])
        distance=math.hypot(cx-px,cy-py)
        self.lenghts.append(distance)
        self.currentlength +=distance
        self.previoseHead=cx,cy
        #length reduction
        if self.currentlength > self.allowedlength:
            for i,lenght in enumerate(self.lenghts):
                self.currentlength-=lenght
                self.lenghts.pop(i)
                self.point.pop(i)
                if self.currentlength < self.allowedlength:
                    break;
 
 
        #Draw snake
        if self.point:
            for i,point in enumerate(self.point):
                if i!=0 :
                    cv2.line(imgMain,self.point[i-1],self.point[i],(0,0,255),20)
            cv2.circle(imgMain,self.point[-1],20,(200,0,200),cv2.FILLED)
        return imgMain
    
    
game=snakeclas()
detector=HandDetector(detectionCon=0.8,maxHands=1)

while True:
    SUCCESS, img =cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    if hands:
        lmList=hands[0]["lmList"]
        pointindex=lmList[8][0:2]
        img =game.update(img,pointindex)
        
        
    cv2.imshow("Image",img)
    cv2.waitKey(1)