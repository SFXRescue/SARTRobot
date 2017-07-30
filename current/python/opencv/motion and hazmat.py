import cv2
import numpy as np
from matplotlib import pyplot as plt
from operator import itemgetter 

 
# Get the stream from the NUC
#cap = cv2.VideoCapture('http://10.0.2.3:8081/')

# Hazmat classes and functions
class Sign(object): 
	
	def __init__(self, image, name, short, minHue, minSat, minBr, maxHue, maxSat, maxBr):
		self.name = name
		self.short = short
		self.image = image
		self.minHue = minHue
		self.minSat = minSat
		self.minBr = minBr
		self.maxHue = maxHue
		self.maxSat = maxSat
		self.maxBr = maxBr

def rotate(sign):
	closest_distance = 100
	for i in range(9):
		dist = match(sign, rotate=45*i)
		if (dist < closest_distance):
			closest_distance = dist
	return closest_distance
		
def match(sign, rotate=-1, debug=False):
	
		
	check_image = cv2.imread('new_s.jpg')	
		
	sign_image = cv2.imread(sign.image)
	sign_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2GRAY)
	
	#mask = cv2.inRange(hsv, np.array([sign.minHue, sign.minSat, sign.minBr]), np.array([sign.maxHue, sign.maxSat, sign.maxBr]))
	#res = cv2.bitwise_and(check_image,check_image, mask= mask)
	# Uncomment the below line to disable HSV
	res = check_image 
	
	if not (rotate == -1):
		num_rows, num_cols = sign_image.shape[:2]
		rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), rotate, 1)
		sign_image = cv2.warpAffine(sign_image, rotation_matrix, (num_cols, num_rows))

	orb = cv2.ORB_create()
	kp1, des1 = orb.detectAndCompute(res,None)
	kp2, des2 = orb.detectAndCompute(sign_image,None)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)

	

	img1_kp1 = matches[0].queryIdx
	(x1, y1) = kp1[img1_kp1].pt
	
	if(matches[0].distance < 36):
		cv2.imshow("matches", cv2.imread(sign.image))

	font = cv2.FONT_HERSHEY_SIMPLEX
	img3 = cv2.putText(check_image,sign.short,(int(x1),int(y1)), font, 1, (200,255,155), 2, cv2.LINE_AA)	
	
	cv2.imshow("match", img3)
	
	if (debug):
		img_matches = cv2.drawMatches(res,kp1,img2,kp2,matches[:1],None, flags=2)
		img_matches = cv2.circle(img_matches,(int(x1), int(y1)), 15, (255,0,0), 2)
		print(sign.name)
		print((int(x1), int(y1)))
		print (matches[0].distance)
		cv2.imshow("matches", img_matches)
		cv2.imshow("res", res)
		cv2.imshow("template", cv2.imread(sign.image))
	
	
	
	return matches[0].distance

def init_sign_list():
	global sign_list
	sign_list = []
	sign_list.append(Sign("templates/template1.jpg", "Oxidizer", "Ox", 0, 100, 200, 255, 255, 255))#1
	sign_list.append(Sign("templates/template2.jpg", "Organic Peroxide", "OP", 0, 100, 200, 255, 255, 255))#2
	sign_list.append(Sign("templates/template3.png", "Flammable Gas", "FG", 0, 100, 200, 255, 255, 255))#3
	sign_list.append(Sign("templates/template4.png", "Inhalation Hazard", "IN", 0, 0, 0, 255, 10, 255))	 #4
	sign_list.append(Sign("templates/template5.jpg", "Dangerous When Wet", "DWW", 80, 0, 0, 155, 255, 255))#5
	sign_list.append(Sign("templates/template6.jpg", "Flammable Solid", "FS", 0, 0, 0, 255, 255, 255))#6
	sign_list.append(Sign("templates/template7.jpg", "Spontaneously Combustible", "SP", 0, 0, 200, 255, 255, 255))#7
	sign_list.append(Sign("templates/template8.png", "Explosives", "Ex", 0, 100, 200, 255, 255, 255))#8
	sign_list.append(Sign("templates/template9.png", "Radioactive II", "Rad", 0, 100, 200, 255, 255, 255))#9
	sign_list.append(Sign("templates/template10.png", "Corrosive", "Cor", 0, 0, 0, 255, 255, 255))#10
	sign_list.append(Sign("templates/template11.jpg", "Non-flammable Gas", "NFG", 0, 0, 0, 255, 255, 255))#11
	sign_list.append(Sign("templates/template12.png", "Infectious Substance", "IS", 0, 0, 0, 255, 10, 255))#12



# Main Loop
while(1):
	#_, frame = cap.read()
	im = cv2.imread("new_s.jpg")
	 
	im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	 
	# Read image
	#im = cv2.imread("blob_detection.jpg", cv2.IMREAD_GRAYSCALE)
	 
	# Set up the detector with default parameters.
	
	sign_distances = {}

	init_sign_list()
	for sign in sign_list:
		distance = match(sign)
		rotated_distance = rotate(sign)
		if (distance > rotated_distance):
			distance = rotated_distance
		sign_distances[sign] = distance
		

	list_keys = []

	for sign, distance in sorted(sign_distances.items(), key=itemgetter(1), reverse=False):
		list_keys.append(sign)
		print(sign.name + ": " + str(distance)) 


	cv2.imshow("Found {}:".format(list_keys[0].name), cv2.imread(list_keys[0].image))
	cv2.imshow("Found {}:".format(list_keys[1].name), cv2.imread(list_keys[1].image))	
	cv2.imshow("Found {}:".format(list_keys[2].name), cv2.imread(list_keys[2].image))
	cv2.imshow("Found {}:".format(list_keys[3].name), cv2.imread(list_keys[3].image))
		
	
	
	
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
	elif k == ord('s'):
		
		break
