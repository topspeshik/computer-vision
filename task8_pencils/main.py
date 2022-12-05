import numpy as np
import cv2
import math


count = 0

for i in range(12):
    
    image = cv2.imread(f"images/img ({i+1}).jpg", cv2.IMREAD_GRAYSCALE)

    gray = cv2.GaussianBlur(image, (91, 91), 0)
    gray[gray > 126] = 255
    gray[gray != 255] = 0

    contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        contour = np.array(cv2.boxPoints(cv2.minAreaRect(c)))
        width = math.dist(contour[0], contour[1])
        height = math.dist(contour[1], contour[2])
        if height * 5 < width:
            count += 1
        if width * 5 < height:
            count += 1


print("Total pencils: ", count)
