import cv2
from cvzone.HandTrackingModule import HandDetector
from matplotlib.pyplot import draw
import numpy as np
import cvzone
from time import sleep 
#create a vidio capture object
cap=cv2.VideoCapture(0)
#room of keybord
cap.set(3, 1280)
cap.set(4, 720)

#create a hand detector
detector=HandDetector(detectionCon=0.8 ,maxHands=2)
keys=[["A","Z","E","R","T","Y","U","I","O","P"],
      ["Q","S","D","F","G","H","J","K","L","M"],
      ["W","X","C","V","B","N",",",";",":","!"]]
finaltext=""

def drawall(img,buttonlist):
    for button in buttonlist:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+21,y+65),cv2.FONT_HERSHEY_PLAIN,
                4,(255,255,255),4)
    return img
# def drawlall(img,buttonlist):
#     imgNew=np.zero_like(img,np.uint8)
#     for button in buttonlist:
#         x,y=button.pos
#         cvzone.cornerRect(imgNew,)
        
        

class button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos ;
        self.size=size; 
        self.text=text;


buttonlist=[]
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonlist.append(button([100 * j +50 ,100 * i +50],key))
    
while True:
    SUCCESS ,img=cap.read()
    img=cv2.flip(img,1)
    #find the hand
    hands ,img = detector.findHands(img,flipType=False)
    img=drawall(img,buttonlist)
    #create le clavier   
    
    if hands:
        lmList=hands[0]["lmList"]
        pointindex=lmList[8][0:2]
        pointint=lmList[12][0:2]
        cv2.circle(img,pointindex,20,(0,255,255),cv2.FILLED)
        cv2.circle(img,pointint,20,(170,255,255),cv2.FILLED)
        for button in buttonlist:
            x,y =button.pos
            w,h =button.size
            if x <lmList[8][0] <x+w and y <lmList[8][1] <y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                cv2.putText(img,button.text,(x+21,y+65),cv2.FONT_HERSHEY_PLAIN,
                4,(255,255,255),4)
                l,_,_=detector.findDistance(pointindex, pointint , img )
                print(l)
                if l <80:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+21,y+65),cv2.FONT_HERSHEY_PLAIN,
                    4,(255,255,255),4)
                    finaltext +=button.text
                    sleep(0.3)
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finaltext,(66,425),cv2.FONT_HERSHEY_PLAIN,
                4,(255,255,255),4)    
    # img=mybouton.draw(img)
    
    cv2.imshow('Image',img)
    cv2.waitKey(1)
    