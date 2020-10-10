import cv2
import sys
import numpy as np
import pytesseract
import imutils
from CorePackage.clean_img import CleanImg

class BoundingBox(CleanImg):
	def __init__(self, image):
		CleanImg.__init__(self, image)
	
	def get_box_coords(self):
		print("[+] Gettting coordinates...")
		self.coords = np.column_stack(np.where(self.thresh > 0))
	
	def calculate_angle(self):
		print("[+] Calculating angle of bounding box...")
		self.angle = cv2.minAreaRect(self.coords)[-1]
	
	def rotate_image(self):
		print("[+] Rotating image...")
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
		else:
			self.angle = self.angle
		self.new_image = imutils.rotate_bound(self.image, self.angle)
		print("[+] Angle: {}".format(self.angle))
		
		
if __name__=="__main__":
	if len(sys.argv) < 2:
		print("Usage: python deskew_image.py <image.png>")
		sys.exit()
		
	img_filepath = sys.argv[1]

	print("[+] Reading {}...".format(img_filepath))
	image = cv2.imread(img_filepath)

	bounding_box = BoundingBox(image)
	bounding_box.grayscale()
	bounding_box.bitwise()
	bounding_box.applyThreshold()

	bounding_box.get_box_coords()
	bounding_box.calculate_angle()
	bounding_box.rotate_image()
	

	print("[+] Saving deskewd image...")
	cv2.imwrite("deskewed_"+sys.argv[1], bounding_box.new_image)


