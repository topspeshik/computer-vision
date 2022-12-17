import cv2
import numpy as np

balls = cv2.VideoCapture("balls.mp4")


def gammaCorrection(image, g=1):
    ig = 1 / g
    lut = (np.arange(256) / 255) ** ig * 255
    lut = lut.astype("uint8")
    return cv2.LUT(image, lut)


while balls.isOpened():
    ret, frame = balls.read()
    if ret:
        count = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gammaCorrection(gray, 2)
        gray[gray > 128] = 255
        gray[gray != 255] = 0

        contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if 40 < len(c) < 250:
                count += 1
            if len(c) > 250:
                count += round(len(c) / 200)

        cv2.putText(frame, f"Count balls {count}", (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0))
        cv2.imshow('Camera', frame)

        key = cv2.waitKey(20)

        if key == ord('q'):
            break
