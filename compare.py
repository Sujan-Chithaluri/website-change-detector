from skimage.metrics import structural_similarity
from PIL import Image
import cv2
import numpy as np

before = cv2.imread('cbit1-crop.png')
after = cv2.imread('cbit2-crop.png')

k=cv2.imread('cbit2-crop.png')

# Convert images to grayscale
before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images
(score, diff) = structural_similarity(before_gray, after_gray, full=True)
print("Image similarity", score)

# The diff image contains the actual image differences between the two images
# and is represented as a floating point data type in the range [0,1] 
# so we must convert the array to 8-bit unsigned integers in the range
# [0,255] before we can use it with OpenCV
diff = (diff * 255).astype("uint8")

# Threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        x,y,w,h = cv2.boundingRect(c)
        #cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.drawContours(mask, [c], 0, (255,255,255), -1)
        #cv2.drawContours(filled_after, [c], 0, (0,0,255), -1)

#cv2.imwrite('before.png', before)
#cv2.imwrite('diff.png',diff)
cv2.imwrite('mask.png',mask)
cv2.imwrite('after.png',after)
#cv2.imwrite('filled after.png',filled_after)
#cv2.waitKey(0)

red_mask = np.copy(k)
red_mask[(mask==255).all(-1)] = [0,0,255]
red_mask= cv2.addWeighted(red_mask,0.4,k,0.6, 0,red_mask)
cv2.imwrite('compare.png',red_mask)
#cv2.waitKey(0)

Image.open('cbit1-crop.png').show()
Image.open('cbit2-crop.png').show()
Image.open('mask.png').show()
#Image.open('after.png').show()
Image.open('compare.png').show()
