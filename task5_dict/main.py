import numpy as np
import matplotlib.pyplot as plt

from skimage.measure import label, regionprops
from collections import defaultdict


def count_lakes_and_bays(prop, cut = False):
    b  = ~prop.image
    if cut:
        b = b[3:-3, 3:-3]
    lb = label(b)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        flag = True
        for y,x in reg.coords:
            if ( y == 0 or x == 0 or 
                y == prop.image.shape[0]-1 or 
                x == prop.image.shape[1] -1): # Boards
                flag = False
                break
        if flag:
            count_lakes+=1
        else:
            count_bays +=1
    
    return count_lakes, count_bays


def has_vline(prop):
    return 1. in prop.image.mean(0)


def filling_factor(prop):
    return prop.image.sum() / prop.image.size

arr = []
def recognize(image):
    result = defaultdict(lambda: 0)
    labeled = label(im)
    props = regionprops(labeled)
    i = 0
    for prop in props:
        lakes = count_lakes_and_bays(prop)[0]
        bays = count_lakes_and_bays(prop)[1]
        
        if np.all(prop.image):
            result["-"] +=1
        elif lakes == 2: # 8 or B
            if has_vline(prop) and bays == 2:
                result["B"] +=1
            else:
                result["8"] +=1
        elif lakes ==1: # A OR D OR P
            if bays == 3:
                result["A"] +=1
            elif bays == 2: # P or D
                cy, _ = prop.centroid
                cy /= prop.image.shape[0]
                if cy <25:
                    result["P"] +=1
                else:
                    result["D"] +=1
            else:
                result["0"] +=1
        elif lakes == 0: # 1 or / or X or * or 0 or W
            if has_vline(prop):
                result["1"] +=1
            elif bays == 2:
                result["/"] +=1
            elif bays ==4 and count_lakes_and_bays(prop, True)[1] :
                if prop.image[0][0]:
                    result["X"] +=1
                else:
                    result["*"] +=1
            else:
                if prop.image[0][0]:
                    result["W"] +=1
                else:
                    result["*"] +=1
                    
        else:
            result["unknown"] +=1
        i+=1
    return result
    


im = plt.imread('alphabet_check.png')
im = np.mean(im,2)
im[im>0] = 1



labeled = label(im)
props = regionprops(labeled)
rec = recognize(im)
print(rec)
print(f"Symbols = {np.max(labeled)}")
