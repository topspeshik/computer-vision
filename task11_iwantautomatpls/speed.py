import cv2
import numpy as np
import time


def createMask(hsv, lower, higher):
    mask1 = cv2.inRange(hsv, lower, higher)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)
    return mask1


def millis():
    return int(round(time.time() * 1000))


ballBlue = [100, 175, 100]
lower = np.array([ballBlue[0] - 20, ballBlue[1] - 30, ballBlue[2] - 20])
higher = np.array([ballBlue[0] + 20, ballBlue[1] + 30, ballBlue[2] + 20])

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

prevX = 0
prevY = 0
speed = 0

prevTime = millis()

while cam.isOpened():
    _, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = createMask(hsv, lower, higher)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

            distance = ((x - prevX) ** 2 + (y - prevY) ** 2) ** 0.5

            speed = round((distance / (millis() - prevTime)) / 100, 2)

            prevTime = millis()
            prevX = 0
            prevY = 0


    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.putText(frame, f"Ball speed {speed}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0))
    cv2.imshow("Camera", frame)
