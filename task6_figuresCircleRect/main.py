import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage import color

im = plt.imread('balls_and_rects.png')
hsv = color.rgb2hsv(im)[:, :, 0]
count = np.mean(im, 2)

count[count > 0] = 1
lb = label(count)

regions = regionprops(lb)
colors = []

dic = dict()
for region in regions:
    cy, cx = region.centroid
    color = hsv[int(cy), int(cx)]
    colors.append(color)

colors = sorted(colors)
diff = np.diff(colors)
delta = np.std(diff) * 2
result = [[colors[0]]]

for i in range(1, len(colors)):
    dc = colors[i] - colors[i - 1]
    if dc > delta:
        result.append([])
    result[-1].append(colors[i])

regColors = []
circl = dict()
rect = dict()


def minColor(colr):
    for i in result:
        if colr in i:
            return len(i)


for region in regions:
    cy, cx = region.centroid
    color = hsv[int(cy), int(cx)]
    color_reg = minColor(color)
    if np.all(region.image):
        if color_reg in rect:
            rect[color_reg] += 1
        else:
            rect[color_reg] = 1
    else:
        if color_reg in circl:
            circl[color_reg] += 1
        else:
            circl[color_reg] = 1

print("Кол-во", len(colors))
print("Оттенок: кол-во")
print("Прямоугольники", rect)
print("Круги", circl)
