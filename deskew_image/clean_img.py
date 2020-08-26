
import numpy as np
import cv2
import sys
import imutils
import pytesseract
import string


class CleanImg:
	def __init__(self, image):
		self.image = image
		
	def grayscale(self):
		print("[+] Grayscale image...")
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
	
	def bitwise(self):
		print("[+] Bitwise operation...")
		self.bitwise = cv2.bitwise_not(self.gray)
	
	def applyThreshold(self):
		print("[+] Applying threshold...")
		self.thresh = cv2.threshold(self.bitwise, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		
		
