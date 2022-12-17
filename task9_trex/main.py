import keyboard
import mss
import numpy as np
import cv2
from time import sleep, time

screen = {"top": 320, "left": 650, "width": 880, "height": 200}

i = 100
j = 210
sleep(2)

img = np.array(mss.mss().grab(screen))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray[gray > 126] = 0
gray[gray != 0] = 255
scoreHundreds = gray[:40, 800:818]
dino = gray[180:190, 30:80]
counterHundreds = 0
curTime = time()
isSpace = False
isBig = False
isMedium = False
isSmall = False
countDistance = 0
sumAll = 0
while True:
    with mss.mss() as sct:
        img = np.array(sct.grab(screen))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray[gray > 126] = 0
        gray[gray != 0] = 255


        if (scoreHundreds.any() != gray[:40, 800:818].any()) and time() - 7 > curTime:
            curTime = time()
            counterHundreds += 1
            if counterHundreds%2==0 and counterHundreds != 0 and counterHundreds < 7:
                j += 15            + counterHundreds
            elif counterHundreds < 9:
                j += counterHundreds
            elif counterHundreds < 12:
                j += 5

            scoreHundreds = gray[:40, 800:818]
        box = gray[150:180  , i:j]


        if box.sum() > 0 and gray[180:190, 30:80].sum() == dino.sum():
            if box.sum() > 30000:
                isSpace = True
                isBig = True
                keyboard.press('space')

                sleep(0.4-counterHundreds/100)
                keyboard.release('space')

            elif box.sum() >10000:
                isSpace = True
                isMedium = True
                keyboard.press('space')
                sleep(0.3- counterHundreds/100)
                keyboard.release('space')

            elif box.sum() > 5000:
                isSpace = True
                isMedium = True
                keyboard.press('space')
                sleep(0.25  -counterHundreds/100)
                keyboard.release('space')
            else:
                isSpace = True
                isSmall = True
                keyboard.press('space')
                sleep(0.15-counterHundreds/100)
                keyboard.release('space')


        if isSpace:

            if    isBig     and gray[140:190, i:j+30+counterHundreds*5].sum() == 0:
                keyboard.press('down')
                sleep(0.05)
                keyboard.release('down')
                isSpace = False
                isBig = False
            elif isSmall  and gray[140:190, i:j+15+counterHundreds*6].sum() == 0 and counterHundreds < 5:
                print(isSmall)
                keyboard.press('down')
                sleep(0.05 )
                keyboard.release('down')
                isSpace = False
                isSmall = False
            elif isMedium    and gray[140:190, i:j+25+counterHundreds*5].sum() == 0:
                keyboard.press('down')
                sleep(0.05)
                keyboard.release('down')
                isSpace = False
                isMedium   = False
            elif isSmall  and gray[140:190, i:j+15+counterHundreds*9].sum() == 0 and counterHundreds >5:
                print(isSmall)
                keyboard.press('down')
                sleep(0.05 )
                keyboard.release('down')
                isSpace = False
                isSmall = False

