#!/bin/python
import numpy as np
import pylab as plt
import cv2
import imutils
import pytesseract
import sys
import string



def ocr_core(image): 
	text = pytesseract.image_to_string(image) 
	osd = pytesseract.image_to_osd(image) 
	return text, osd 


def detect_english(text):
	char_freq = []
	for char in string.ascii_lowercase:
		char_freq.append(text.lower().count(char))
	max_char_count = max(char_freq)
	if not char_freq.index(max_char_count) == 'e':
		print(string.ascii_lowercase[char_freq.index(max_char_count)])
		return "Not English"


def find_max_variance(start_angle, end_angle, thresh, step):
	maxes = []
	variances = []
	angles = np.arange(start_angle, end_angle, step)
	for i in angles:
		image_rotated = imutils.rotate_bound(thresh, i)
		x_sum = np.sum(image_rotated, axis=1)
		print("angle: {}, Max:{}, Var: {}".format(i, max(x_sum), np.var(x_sum)))
		maxes.append(np.max(x_sum))
		variances.append(np.var(x_sum))

	plt.plot(angles, variances)
	variances = np.array(variances)
	angle_to_rotate = angles[np.where(variances==max(variances))[0][0]]
	return angle_to_rotate

def adaptive_method():
	threshold = 0.01
	old_angle = -160
	new_angle = 160
	dtheta = abs(old_angle - new_angle)
	alpha = 0.05
	step = alpha * dtheta
	boundaries = 10
	while True:
		new_angle = find_max_variance(
			old_angle - boundaries, 
			new_angle + boundaries, 
			thresh, 
			step
		)
		dtheta = abs(old_angle - new_angle)
		if dtheta <= threshold:
			break
		else:
			old_angle = new_angle
			step = alpha * dtheta
			boundaries = dtheta
			if step < threshold:
				step = threshold
			if boundaries > 50:
				boundaries = 50
	return new_angle


if __name__=="__main__":
	if len(sys.argv) < 2:
		print("Usage: python deskew_image.py <image.png>")
		sys.exit()
	
	image = cv2.imread(sys.argv[1])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)
	thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	
	angle_to_rotate = adaptive_method()
	new_image = imutils.rotate_bound(image, angle_to_rotate)
	try:
		text, osd = ocr_core(new_image)
		print("Text: ", text)
		for line in osd.splitlines():
			if "Orientation in degrees" in line: 
				orientation = int(line.split(":")[1])
				break
	except:
		pass
			
	while True:
		if orientation == 0:
			break
		else:
			new_image = imutils.rotate_bound(new_image, -orientation)
			text, osd = ocr_core(new_image)
			print("Text:",text)
	
	cv2.imwrite("deskewd_"+sys.argv[1],new_image)
		

