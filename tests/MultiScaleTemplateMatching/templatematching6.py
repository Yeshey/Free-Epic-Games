# https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
import numpy as np
import imutils
import glob
import cv2
from PIL import ImageGrab

im = ImageGrab.grab()
im.save("screenshot.png", "PNG")

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread('FREENOW.png')
# todo uncomment these next two lines to see if it makes a diference rather than using raw image
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # convert to greyscale 
template = cv2.Canny(template, 50, 200) # detect edges
(tH, tW) = template.shape[:2]
cv2.imshow("Template", template)
#cv2.waitKey(0)

# load the image, convert it to grayscale, and initialize the
# bookkeeping variable to keep track of the matched region
image = cv2.imread("screenshot.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray = image
found = None

# loop over the scales of the image
# np.linspace(size of ending image, size of final image, number of steps)
for scale in np.linspace(0.7, 1.6, 400)[::-1]: 
    # resize the image according to the scale, and keep track
    # of the ratio of the resizing
    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])

    # if the resized image is smaller than the template, then break
    # from the loop
    if resized.shape[0] < tH or resized.shape[1] < tW:
        break

    # detect edges in the resized, grayscale image and apply template
    # matching to find the template in the image
    edged = cv2.Canny(resized, 50, 200)
    #cv2.imshow("edged", resized)
    #cv2.waitKey(0)
    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    
    # draw a bounding box around the detected region
    clone = np.dstack([result, result, result])
    cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
        (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
    cv2.imshow("Visualize", edged)
    cv2.waitKey(1)

    # if we have found a new maximum correlation value, then update
    # the bookkeeping variable
    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)
        print(maxVal)
        '''
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # draw a bounding box around the detected result and display the image
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        '''

# unpack the bookkeeping variable and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
#cv2.imshow("Image", image)
#cv2.waitKey(0)
cv2.imwrite('result.png', image)