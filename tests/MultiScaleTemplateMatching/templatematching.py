
# https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image
# working sort of !!!
import cv2
from PIL import ImageGrab

method = cv2.TM_SQDIFF_NORMED
# Read the images from the file

im = ImageGrab.grab()
im.save("screenshot.png", "png")

small_image = cv2.imread('FREENOW.png')
large_image = cv2.imread('screenshot.png')
result = cv2.matchTemplate(small_image, large_image, method)
# We want the minimum squared difference
mn,_,mnLoc,_ = cv2.minMaxLoc(result)
# Draw the rectangle:
# Extract the coordinates of our best match
MPx,MPy = mnLoc
# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2]
# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
# Display the original image with the rectangle around the match.
cv2.imwrite('result.png', large_image)

# -----------------------------------------------------

'''
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
'''

# -----------------------------------------------------

'''
import cv2
import numpy as np
from PIL import ImageGrab

im = ImageGrab.grab()
im.save("screenshot.png", "png")

image= cv2.imread('screenshot.png')
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template= cv2.imread('FREENOW.png',0)


result= cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
print(result)
min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)

height, width= template.shape[:2]

top_left= max_loc
bottom_right= (top_left[0] + width, top_left[1] + height)
cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)

cv2.imwrite('result.png', image)
'''