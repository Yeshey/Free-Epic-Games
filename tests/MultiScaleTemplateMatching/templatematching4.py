# not working?
import cv2
import numpy as np
from PIL import ImageGrab

im = ImageGrab.grab()
im.save("screenshot.png", "PNG")

img_rgb = cv2.imread('screenshot.png')
template = cv2.imread('FREENOW.png')
h, w = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .4
loc = np.where(res >= threshold)
print(loc)
for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('result.png', img_rgb)