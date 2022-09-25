import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import face


def block_mean(arr, yb=8, xb=8):
    new_shape = yb, xb
    new_arr = np.zeros(new_shape)
    block_size_y = np.int(np.ceil(arr.shape[0] // yb))
    block_size_x = np.int(np.ceil(arr.shape[1] // xb))

    for y in range(0, arr.shape[0], block_size_y):
        for x in range(0, arr.shape[1], block_size_x):
            ny = y // block_size_y
            nx = x // block_size_x
            if (ny > yb - 1) or (nx > xb - 1):  break
            new_arr[ny, nx] = np.mean(arr[y:y + block_size_y, x:x + block_size_x])

    return new_arr


img = face(gray=True)

plt.subplot(121)
plt.imshow(img, cmap="gray")
plt.subplot(122)
new_img = block_mean(img, 50, 50)
plt.imshow(new_img, cmap="gray")
plt.show()