import cv2 as cv
import numpy as np
import copy
#Read the pic, split them into bgr grey scale
pic_name = raw_input("Picture Name: ")
raw_img = cv.imread(pic_name)
b,g,r = cv.split(raw_img)

#Improve contrast by equalizing the picture
eq_b = cv.equalizeHist(b)
eq_r = cv.equalizeHist(r)
diffed_pic = cv.subtract(eq_b,eq_r)
cv.imwrite('minus.jpg',diffed_pic) #For debugging

#Set threshold binarilize the grey scale picture.
_,thresh = cv.threshold(diffed_pic,98,255,cv.THRESH_BINARY)
kernel = np.ones((5,5),np.uint8)
thresh = cv.dilate(thresh,kernel,iterations = 2)
# Find all contours avaliable.
_,cnts,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

cv.imwrite('thresh.jpg',thresh) #For debugging
cpy_img = copy.deepcopy(raw_img)
cpy_img = cv.drawContours(cpy_img,cnts,-1,(0,0,255),2)
cv.imwrite('allcnts.jpg',cpy_img)
for cnt in cnts:
	if cv.contourArea(cnt) > 5000 and cv.contourArea(cnt)<100000: 
		#Screen areas enclosed by contours that are too big or small
		rect = cv.minAreaRect(cnt)
		ratio1 = rect[1][0] / rect[1][1]
		ratio2 = rect[1][1] / rect[1][0]
		if (rect[2] <= -45 and ratio1 > 0.25 and ratio1 < 0.7) or (rect[2] >= -33 and ratio2 > 0.25 and ratio2 < 0.7):
			#Screen the shape according to it wid to height ratio
			box = cv.boxPoints(rect)
			box = np.int0(box)
			raw_img = cv.drawContours(raw_img,[box],0,(0,255,0),5)
cv.imwrite('result2.jpg',raw_img)

# To do: Correct the angle.


