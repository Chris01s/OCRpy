
import numpy as np
import cv2
import sys
import imutils
import pytesseract
import string
from matplotlib.pyplot import plot, show, imshow


class CleanImg:
	def grayscale(self, image):
		print("[+] Grayscale image...")
		self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	def applyBitwise(self):
		print("[+] Bitwise operation...")
		self.bitwise = cv2.bitwise_not(self.gray)
	
	def applyThreshold(self):
		print("[+] Applying threshold...")
		self.thresh, self.img_bin = cv2.threshold(self.bitwise, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	def invert_image(self, image):
		self.grayscale(image)
		self.applyBitwise()
		self.applyThreshold()

		img_inverted = self.img_bin  # Invert the image

		cv2.imwrite("Image_bin.jpg", self.img_bin)
		print("[+] Image bin created...")
		return img_inverted

	
		
