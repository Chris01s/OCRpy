import os
import cv2
from glob import glob
import pytesseract

from CorePackage.system_class import System
from CorePackage.clean_img import CleanImg


class OCRExtract(System, CleanImg):
	def read_image(self, filepath):
		return cv2.imread(filepath)
		
	def resize_image(self, img):
		return cv2.resize(img, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC)
		
	def ocr_extract_text(self, img):
		return pytesseract.image_to_string(img)
		
	def extract_text_from_img(self, img_filepath):
		 ##read the image in
		 img = self.read_image(img_filepath)
		 
		 ##resize it by a factor of 1.5
		 resized_img = self.resize_image(img)
		 
		 ##perform OCR...
		 OCR_text = self.ocr_extract_text(img)
		 
		 ## if no output, try resetting the DPI, resizing and try again
		 if not OCR_text:
		     resized_img_filepath = self.set_image_dpi(img_filepath)
		     img = self.remove_noise_and_smooth(resized_img_filepath)
		     OCR_text = self.ocr_extract_text(img)
		 return OCR_text


	def extract_text_from_all_imgs(self, dir_path, dest_path):
		 '''extracts from ALL pages in the document'''
		 pages = glob(dir_path+"/*.jpg")
		 self.create_folders_if_not_exist(dest_path)
		 for npage, page in enumerate(pages):
		     try:
		         OCR_text = self.ocr_extract_text(page)
		         OCR_text_file_name = os.path.basename(page)
		         OCR_text_file_name = OCR_text_file_name.replace(".jpg",".txt")
		         OCR_text_file_path = dest_path+"/"+OCR_text_file_name
		         with open(OCR_text_file_path,"w") as OCR_FILE:
		             OCR_FILE.write(OCR_text)
		         self.update_progress("OCR Extraction", npage, len(pages))
		     except:
		         print("Could not extract page:", page)
		 self.del_files_under_limit(
		 	dir_path=dest_path,
		 	file_ext="txt",
		 	limit=10
		 )



