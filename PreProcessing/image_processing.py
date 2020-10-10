
from CorePackage.system_class import System
import os
from PIL import Image
import numpy as np
import cv2


class ImageProcessing(System):	
	def resize_image(self, image):
		 ##get the dimensions of image
		 length_x, width_y = image.size
		 
		 #resize the image with anti-aliasing
		 factor = min(1, float(1024.0 / length_x))
		 size = int(factor * length_x), int(factor * width_y)
		 
		 return image.resize(size, Image.ANTIALIAS)
		 
			
	def set_image_dpi(self, filepath):
		 ##read in image
		 image = self.read_image_PIL(filepath)
		 
		 ##resize image
		 image_resized = self.resize_image(image)
		 filepath = filepath.replace(".jpg","_resized.jpg")
		 
		 #save new image
		 image_resized.save(filepath, dpi=(1000, 1000))
		 print(f"[+] Saved file as {filepath}")
		 return filepath


	def image_smoothening(self, image):
		 '''
		 	this smooths images with a gaussian blur: https://en.wikipedia.org/wiki/Gaussian_blur
		 '''
		 blur = cv2.GaussianBlur(image, (5, 5), 0)
		 ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		 ret2, th2 = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		 return th2


	def remove_noise_and_smooth(self, filepath):
		 '''
		 	this takes the above functions and performs all kinds of image smoothing 
		 	and noise removal...again, only a small difference, I havent had much luck with it
		 '''
		 img = self.read_image_cv2(filepath)
		 
		 filtered = cv2.adaptiveThreshold(
		     img.astype(np.uint8), 255,
		     cv2.ADAPTIVE_THRESH_MEAN_C,
		     cv2.THRESH_BINARY, 9, 20
		 )
		 kernel = np.ones((1, 1), np.uint8)
		 opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
		 closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
		 img = self.image_smoothening(img)
		 or_image = cv2.bitwise_or(img, closing)
		 return or_image
