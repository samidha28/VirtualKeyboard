#importing packages
import cv2
import cvzone
from pynput.keyboard import Key, Controller
#to track hands
from cvzone.HandTrackingModule import HandDetector
from time import sleep

#videoCapture Object with (webcam) id=0
cap= cv2.VideoCapture(0)

#HD resolution
#setting width value (prop id=3)
cap.set(3, 1280)
#setting height value (prop id=4)
cap.set(4, 720)

#to detect hands with detectionConfidence=0.8 for more accuracy
detector= HandDetector(detectionCon=0.8)

#list of lists to store keys of keyboard in order
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "."],
        ["Z", "X", "C", "V", "B", "N", "M", ","],
        [" "]]

#to store typed words
finalText= ""

keyboard= Controller()

#opaque buttons
def drawAll(img, buttonList):
    # to create buttons using rectangles
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                                                  20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (219, 112, 147), cv2.FILLED)
        cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    return img

#to define attributes of a particular button
class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos=pos
        self.size= size
        self.text=text

buttonList= []

for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        if(key==" "):
            buttonList.append(Button([(x * 100) + 300, (100 * i) + 50], key, [350,75]))
        elif(key=='<-'):
            buttonList.append(Button([(x * 100) + 50, (100 * i) + 50], key, [130, 85]))
        else:
            buttonList.append(Button([(x * 100) + 50, (100 * i) + 50], key))

#running a loop
while True:
    success, img= cap.read()
    img= cv2.flip(img,1)

    #to find hands
    img= detector.findHands(img)
    #to find landmark points
    lmList, bboxInfo= detector.findPosition(img)

    img= drawAll(img,buttonList)
    # img= myButton.draw(img)

    #when a hand is detected
    if lmList:
        for button in buttonList:
            x,y= button.pos
            w,h= button.size

            #if index finger is inside the rectangle area of button
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), 	(186,85,211), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)

                #to check if it's a cl,ick (cond: if middle and index finger are too close it's a click)
                #8 and 12 are prop values for tip of index finger and middle finger respectively
                # '_' to avoid the other values as we'll consider only length
                l, _, _= detector.findDistance(8,12,img, draw=False)
                print(l)

                #when button is clicked
                if l<20:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (255,228,225), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

                    if (button.text == '<-'):
                        keyboard.press(Key.backspace)
                        sleep(0.1)
                        keyboard.release(Key.backspace)
                    else:
                        keyboard.press(button.text)

                    #to add the letter typed
                    if(button.text=='<-'):
                        finalText= finalText[:-1]
                        break
                    else:
                        finalText+=button.text
                    sleep(0.2)

        #displays word after each letter is typed
        cv2.rectangle(img,(50,650),(700,458),(175,0,175), cv2.FILLED)
        cv2.putText(img, finalText, (60,510), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 3)

    #to run the webcam
    cv2.imshow("Image", img)
    cv2.waitKey(1)

