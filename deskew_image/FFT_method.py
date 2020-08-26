import numpy as np
import cv2
import sys
import imutils
import pytesseract
import string

from clean_img import CleanImg


class FFT(CleanImg):
	def __init__(self, image):
		CleanImg.__init__(self, image)
		
	def apply_FFT_threshold(self):
		print("[+] Applying FFT to image...")
		fft_image = np.fft.fft2(self.thresh)
		self.fft_image = np.fft.fftshift(fft_image)
	
	def get_magnitude_spectrum(self):
		print("[+] Calculating mag spectrum of FFT image")
		self.magnitude_spectrum = 20*np.log(abs(self.fft_image))
	
	def calculate_angle_of_FFT(self):
		print("[+] Calculating arc angle of FFT image")
		x, y = np.where(np.flipud(self.magnitude_spectrum)>=255)
		self.angle = np.arctan2(max(y)-min(y), max(x)-min(x))*180/np.pi 
		print("[+] Angle: {}".format(self.angle))
				
	def rotate_image(self):
		self.new_image = imutils.rotate_bound(self.image, self.angle)
	
	def resize_image(self):
		scale_percent = 200# percent of original size
		width = int(self.new_image.shape[1] * scale_percent / 100)
		height = int(self.new_image.shape[0] * scale_percent / 100)
		dim = (width, height) 
		new_image = cv2.resize(self.new_image, dim, interpolation= cv2.INTER_AREA)
	

if __name__=="__main__":
	if len(sys.argv) < 2:
		print("Usage: python {} <image.png>".format(sys.argv[0]))
		sys.exit()
		
	img_filepath = sys.argv[1]

	print("[+] Reading {}...".format(img_filepath))
	image = cv2.imread(img_filepath)

	fft_obj = FFT(image)
	
	fft_obj.grayscale()
	fft_obj.bitwise()
	fft_obj.applyThreshold()

	fft_obj.apply_FFT_threshold()
	fft_obj.get_magnitude_spectrum()	
	fft_obj.calculate_angle_of_FFT()
	fft_obj.rotate_image()
	fft_obj.resize_image()

	print("[+] Saving deskewd image...")
	cv2.imwrite("deskewed_"+sys.argv[1], fft_obj.new_image)


