import cv2
import imutils
import sys
from CorePackage.system_class import System
from CorePackage.clean_img import CleanImg
import numpy as np
import os



class BoxExtraction(System, CleanImg):
	def __init__(self):
		System.__init__(self)
		CleanImg.__init__(self)


	def build_kernels(self, kernel_length_horizontal = 30, kernel_length_verticle = 15):
		 hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_horizontal, 1))
		 vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_verticle))
		 print("[+] Vertical and Horizontal kernels calculated...")
		 return hori_kernel, vert_kernel
	
	
	def line_image(self, image_inverted, kernel, filename):
		temp_image = cv2.erode(image_inverted, kernel, iterations=3)
		line_image = cv2.dilate(temp_image, kernel, iterations=5)
		cv2.imwrite(filename+".jpg", line_image)
		print(f'[+] {filename+".jpg"} created...')
		return line_image


	def final_lines_image(self, vertical_lines_img, horizontal_lines_img):
		alpha = 0.5
		beta = 1.0 - alpha
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

		img_final_bin = cv2.addWeighted(vertical_lines_img, alpha, horizontal_lines_img, beta, 0.0)
		img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)

		thresh, img_final_bin = cv2.threshold(img_final_bin, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
 
		cv2.imwrite("img_final_bin.jpg",img_final_bin)
		print("[+] Combined Line image created...")
		return img_final_bin
	

	def build_final_lines_image(self, filepath):
		self.image = cv2.imread(filepath)
		image_inverted = self.invert_image(self.image)
		
		hori_kernel, vert_kernel = self.build_kernels(
			kernel_length_horizontal = 50,
			kernel_length_verticle = 40
		)
		horizontal_lines_img = self.line_image(image_inverted, hori_kernel, "horizontal_line_image")
		vertical_lines_img = self.line_image(image_inverted, vert_kernel, "vertical_line_image")
		return self.final_lines_image(vertical_lines_img, horizontal_lines_img)
	
	
	def integrate_image_over_x_axis(self, image):
		return np.sum(image, axis=1)
		
	
	def get_local_maxima(self, x_sum):
		x_sum_maxima_mask = [0] ##start with zero as this makes the maths easier for slicing later
		for idx in range(len(x_sum)):
			if x_sum[idx-1] < x_sum[idx] and x_sum[idx+1] < x_sum[idx]:
				x_sum_maxima_mask.append(idx)
		return x_sum_maxima_mask
		
		
	def take_img_slice(self, mask, image, idx):
		try:
			img_slice = image[mask[idx]:mask[idx+1]]
		except:
			img_slice = image[mask[idx]:]
		return img_slice
		
		
	def slice_image_by_horizontal_lines(self, filepath):
		img_final_bin = self.build_final_lines_image(filepath)
		try:
			horizontal_image = cv2.imread("horizontal_line_image.jpg", 0)
		except Exception as ex: 
			print(f"[!!] Problem reading horizontal line image...: {ex.__str__()}")
		else:
			self.cropped_dir_path = ''.join(filepath.split(".")[:-1]) + "_horizontal_slice_imgs"
			self.create_folders_if_not_exist(self.cropped_dir_path)

			x_sum = self.integrate_image_over_x_axis(horizontal_image)
			x_sum_maxima_mask = self.get_local_maxima(x_sum)

			#slice image up
			print(f"[*] Cropping {filepath} image on horizontal lines...")
			for n, i in enumerate(x_sum_maxima_mask):
				self.update_progress("Slicing image", n, len(x_sum_maxima_mask))
				img_slice = self.take_img_slice(x_sum_maxima_mask, self.image, n)
				##save image slice
				crop_img_filename = os.path.join(self.cropped_dir_path, "slice_{}.jpg".format(n))
				cv2.imwrite(crop_img_filename, img_slice)
	
	def crop_img_with_box_extraction(self, filepath):
		print("[*] Performing collision detection...")
		img_final_bin = self.build_final_lines_image(filepath)
		cnts = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		
		self.cropped_dir_path = ''.join(filepath.split(".")[:-1]) + "_box_cropped_imgs"
		self.create_folders_if_not_exist(self.cropped_dir_path)
		
		for ncnt, cnt in enumerate(cnts):
			self.update_progress("Cropping table", ncnt, len(cnts))
			# Returns the location and width,height for every contour
			x, y, w, h = cv2.boundingRect(cnt)
			new_img = self.image[y:y+h, x:x+w]
			crop_img_filename = os.path.join(self.cropped_dir_path, "crop_{}.jpg".format(ncnt))
			cv2.imwrite(crop_img_filename, new_img)
				 
