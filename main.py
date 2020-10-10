from PDFpy import PDFExtract
from PreProcessing.image_processing import ImageProcessing
from PreProcessing.image_magick import ImageMagick
from PreProcessing.box_extraction import BoxExtraction
from CorePackage.system_class import System
from ocr_extract import OCRExtract
import sys
import cv2
import time
import os
from glob import glob
import platform
from argparse import ArgumentParser
from matplotlib.pyplot import imshow, show, plot


def get_banner():
	try:
		os.system("figlet OCRpy")
	except:
		print("Error: requirements missing: figlet")
		if platform.system() == "Linux":
			print("Linux users: sudo apt install figlet\n\n") 
		print("="*20+"\n")
		print("\t"+"OCRpy"+"\n")
		print("="*20)


def get_file_extension(filepath):
	return filepath.strip().split(".")[-1]


def file_is_pdf(file_ext):
	return file_ext == "pdf"


def file_is_jpg(file_ext):
	return file_ext == "jpg"



class OCRpy(OCRExtract, BoxExtraction, System):
	def __init__(self, FILE, dir_path):
		self.FILE = FILE
		self.dir_path = dir_path
		self.file_ext = get_file_extension(self.FILE)
		OCRExtract.__init__(self)
		BoxExtraction.__init__(self)


	def horizontal_slice_extraction(self, page):
		dest_path = page.replace("."+self.img_ext,"_horizontal_slice_text")
		self.slice_image_by_horizontal_lines(page)
		self.extract_text_from_all_imgs(self.cropped_dir_path, dest_path)
	
	
	def box_detection_extraction(self, page):
		dest_path = page.replace("."+self.img_ext,"_box_cropped_text")
		self.crop_img_with_box_extraction(page)
		self.extract_text_from_all_imgs(self.cropped_dir_path, dest_path)
		
		
	def box_ocr(self):
		print("[*] Attempting crop table extraction...")
		pages = glob(self.dir_path+"/*.jpg")
		for page in pages:
			try:
				print(f"\n\n[*] OCR Extraction on {page}")
				self.img_ext = get_file_extension(page)
				##horizontal line img
				self.horizontal_slice_extraction(page)
									
				##box detection img
				self.box_detection_extraction(page)
			except Exception as ex:
				print("\n[!!] Somthing went wrong: {}".format(ex.__str__()))
			
		print("\n[+] Box and Slice OCR extraction complete...")
		print("[*] Cleaning up...")
	
		##cleaning up
		self.delete_file("horizontal_line_image.jpg")
		self.delete_file("vertical_line_image.jpg")
		self.delete_file("img_final_bin.jpg")	
		self.delete_file("Image_bin.jpg")


	def extract_text(self):
		print("\n[+]\t OCR ...")
		dest_path = self.FILE.replace("."+self.file_ext,"_ocr_text")
		self.extract_text_from_all_imgs(self.dir_path, dest_path)
		print("[+] OCR Extraction complete: see {} for extraction results".format(dest_path))
		time.sleep(1)
		self.box_ocr()
	
	
	
	
	
if __name__=="__main__":
	get_banner()
	argparser = ArgumentParser(description="OCR and pdf extract tool\n\nCommandline argument -h for help.\n")
	argparser.add_argument(
		"-f", "--filepath",
		help = "PDF or JPG filepath to extract",
	)
	
	system = System()
	args = argparser.parse_args()
	FILE = args.filepath
	FILE = system.clean_filename(FILE)
	file_ext = get_file_extension(FILE)
	
	
	if file_is_pdf(file_ext):
		print(f"[*] Extracting {FILE}...")
		##code for pdf extraction
		pdf_extract = PDFExtract()
		full_text = pdf_extract.get_full_text(FILE, form="-raw", output="full_text.txt")
		if not pdf_extract.is_scanned(full_text):
			pdf_extract.seperate_pages(FILE)
			pdf_extract.extract_each_page(FILE)
		else:
			print("[-] The pdf is empty, possibly scanned...")
			print("[*] Performing OCR extraction...")
			image_magick = ImageMagick(FILE)
			if not image_magick.check_if_imagemagick_installed():
				print("[!!] Image magick is not installed on this system")
				sys.exit(1)
			else:
				image_magick.convert_pdf_to_png()
				dir_path = image_magick.temp_folder
				ocr = OCRpy(FILE, dir_path)
				ocr.extract_text()
	elif file_is_jpg(file_ext):
			dir_path = os.path.join(os.getcwd(), FILE.replace("."+file_ext, "_imgs"))
			system.create_folders_if_not_exist(dir_path)
			system.copy_file(FILE, dir_path)
			ocr = OCRpy(FILE, dir_path)
			ocr.extract_text()
			

							
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
			
	

	
	
