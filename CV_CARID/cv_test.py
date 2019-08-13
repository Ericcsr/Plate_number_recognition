import cv2 as cv
import numpy as np
import copy
from math import sin,cos,sinh,cosh,tan,tanh
#Read the pic, split them into bgr grey scale
pic_name = raw_input("Picture Name: ")
raw_img = cv.imread(pic_name)
b,g,r = cv.split(raw_img)

#Improve contrast by equalizing the picture
eq_b = cv.equalizeHist(b)
eq_r = cv.equalizeHist(r)
diffed_pic = cv.subtract(eq_b,eq_r)
cv.imwrite('minus.jpg',diffed_pic) #For debugging

# Set threshold binarilize the grey scale picture.
_,thresh = cv.threshold(diffed_pic,98,255,cv.THRESH_BINARY)
# Avoid text content caused sticky.
kernel = np.ones((5,5),np.uint8)
thresh = cv.dilate(thresh,kernel,iterations = 2)
# Find all contours avaliable.
_,cnts,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

cv.imwrite('thresh.jpg',thresh) #For debugging
cpy_img = copy.deepcopy(raw_img)
cpy_img = cv.drawContours(cpy_img,cnts,-1,(0,0,255),2)
cv.imwrite('allcnts.jpg',cpy_img)
rects = list() #create a list that can be used to save rectangles.
demo_img = copy.deepcopy(raw_img) 
for cnt in cnts:
	if cv.contourArea(cnt) > 5000 and cv.contourArea(cnt)<100000: 
		#Screen areas enclosed by contours that are too big or small
		rect = cv.minAreaRect(cnt)
		ratio1 = rect[1][0] / rect[1][1]
		ratio2 = rect[1][1] / rect[1][0]
		if (rect[2] <= -45 and ratio1 > 0.25 and ratio1 < 0.7) or (rect[2] >= -33 and ratio2 > 0.25 and ratio2 < 0.7):
			#Screen the shape according to it wid to height ratio
			rects.append(rect)
			box = cv.boxPoints(rect)
			box = np.int0(box)
			demo_img = cv.drawContours(demo_img,[box],0,(0,255,0),5)
cv.imwrite('result2.jpg',demo_img)
# Sort the list based on the area of rect
rects.sort(key = lambda rect:rect[1][0]*rect[1][1])
# To do: Grasp the ROI bounded by 'box'
car_candidates = list() # A list that used to contains 
car_index = 0
	# Rotate the colored picture using box till box's edge is parallel.
	#     * p2
	#    *    * p1
	#p4 *    * theta
	#    p3 *__________
for rect in rects:
	box = cv.boxPoints(rect)
	process_img = copy.deepcopy(raw_img)
	rows,cols,ch = process_img.shape
	print('rows:',rows,' columns:',cols)
	x,y = rect[0] # Center of the rectangle
	theta = abs(rect[2]) # This is the absolute rotation angle
	print(theta)
	width = rect[1][0]
	height = rect[1][1]
	#point1 = (x+ (width * cos(theta)/2 + height*sin(theta)/2) , rows - ((rows-y)+(width * sin(theta)/2 - height*cos(theta)/2)))
	point1 = box[3]
	#point2 = (x+ (width * cos(theta)/2 - height*sin(theta)/2) , rows - ((rows-y)+(width * sin(theta)/2 + height*cos(theta)/2)))
	point2 = box[2]
	#point3 = (x+ (-width * cos(theta)/2 - height*sin(theta)/2) , rows - ((rows-y)+(-width * sin(theta)/2 + height*cos(theta)/2)))
	point3 = box[1]
	#point4 = (x+ (-width * cos(theta)/2 + height*sin(theta)/2) , rows - ((rows-y)+(-width * sin(theta)/2 - height*cos(theta)/2)))
	point4 = box[0]
	#cv.drawContours(process_img,np.array([[point1,point2,point3,point4]]),0,(255,0,0),3)
	if (theta <= 33):
		pts = np.float32([point1,point2,point3])
	else:
		pts = np.float32([point4,point1,point2])
	target_pts = np.float32([[440,140],[440,0],[0,0]])
	M = cv.getAffineTransform(pts,target_pts)
	process_imghat = cv.warpAffine(process_img,M,(cols,rows))
	# select the region using indexing.
	cv.imwrite('rotated.jpg',process_imghat)
	car_candidate = process_imghat[0:140,0:440]
	car_candidates.append(car_candidate)
	# save as new image	
	cv.imwrite('isolated_car%d.jpg'%car_index,car_candidate)	
	car_index +=1
#cv.imwrite('origin.jpg',process_img)
# To do: Process the ROI to highlight text.
	# Map to grey scale.
	# Equalization.
	# Thresholding.		
# To do: correct the right angle.
	# dilate and egde detection. 
	# Mapped to rectangle.
# To do: fix the width, height ratio.
# To do: Seperate the text


