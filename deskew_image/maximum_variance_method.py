#!/bin/python
import numpy as np
import pylab as plt
import cv2
import imutils
import pytesseract
import sys
import string

from clean_img import CleanImg


class MaxVariance(CleanImg):
	def __init__(self, image):
		CleanImg.__init__(self, image)
	
	def detect_english(self, text):
		char_freq = []
		for char in string.ascii_lowercase:
			char_freq.append(text.lower().count(char))
		max_char_count = max(char_freq)
		return char_freq.index(max_char_count) == 'e'

	def find_max_variance(self, start_angle, end_angle, step, thresh):
		maxes = []
		variances = []
		angles = np.arange(start_angle, end_angle, step)
		print_line = "[+] Rotating image by "
		for i in angles:
			image_rotated = imutils.rotate_bound(thresh, i)
			print(print_line+str(i),end='')
			print('\b' * len(print_line+str(i)), end='', flush=True)
			
			##integrate across the x-axis
			x_sum = np.sum(image_rotated, axis=1)
			
			##find maximum value in the sum across x-axis
			maxes.append(np.max(x_sum))
			
			##find the maximum variance in the x-axis spectrum
			variances.append(np.var(x_sum))
			
		variances = np.array(variances)
		return angles[np.where(variances==max(variances))[0][0]]


	def adaptive_method(self):
		threshold = 0.01
		old_angle = -160
		new_angle = 160
		dtheta = abs(old_angle - new_angle)
		alpha = 0.05
		step = alpha * dtheta
		boundaries = 10
		while True:
			new_angle = self.find_max_variance(
				old_angle - boundaries, 
				new_angle + boundaries,  
				step,
				self.thresh
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
		self.angle = new_angle

	def rotate_image(self):
		try:
			self.new_image = imutils.rotate_bound(self.image, self.angle)
			osd = pytesseract.image_to_osd(self.new_image) 
			for line in osd.splitlines():
				if "Orientation in degrees" in line: 
					orientation = int(line.split(":")[1])
					break
			if orientation != 0:
				self.new_image = imutils.rotate_bound(self.new_image, orientation)
		except Exception as ex:
			# otherwise, just take the inverse of the angle to make
			# it positive
			if self.angle < -135:
				self.angle += 180
			elif self.angle < -90:
				self.angle += 90
			elif self.angle < -45:
				self.angle += 90
			elif self.angle > 45:
				self.angle -= 45
			elif self.angle > 90:
				self.angle -= 90
			elif self.angle > 135:
				self.angle -= 180
			self.new_image = imutils.rotate_bound(self.image, self.angle)
		print("\n[+] Angle is {}".format(self.angle))
		
	def resize_image(self):
		scale_percent = 200# percent of original size
		width = int(self.new_image.shape[1] * scale_percent / 100)
		height = int(self.new_image.shape[0] * scale_percent / 100)
		dim = (width, height) 
		self.new_image = cv2.resize(self.new_image, dim, interpolation= cv2.INTER_AREA)
		


if __name__=="__main__":
	if len(sys.argv) < 2:
		print("Usage: python deskew_image.py <image.png>")
		sys.exit()
	
	image = cv2.imread(sys.argv[1])

	max_var_obj = MaxVariance(image)
	
	max_var_obj.grayscale()
	max_var_obj.bitwise()
	max_var_obj.applyThreshold()
	
	max_var_obj.adaptive_method()
	max_var_obj.rotate_image()
	max_var_obj.resize_image()
	
	try:
		text = pytesseract.image_to_string(max_var_obj.new_image)
	except:
		print("[!] Could not perform OCR on the image")
		sys.exit()

	print("[+] Saving the deskewed image...")
	cv2.imwrite("deskewed_"+sys.argv[1],max_var_obj.new_image)
		

