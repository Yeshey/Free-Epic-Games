import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import ImageGrab

im = ImageGrab.grab()
im.save("screenshot.png", "png")

image = cv2.imread('screenshot.png')
template = cv2.imread('FREENOW.png')
heat_map = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

h, w, _ = template.shape
y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)
cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 5)

#plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
cv2.imwrite('result.png', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))