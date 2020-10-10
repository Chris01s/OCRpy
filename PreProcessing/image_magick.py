import re
from glob import glob
import subprocess
import shutil
import os
from PDFpy import PDFExtract



class ImageMagick(PDFExtract):	
	def __init__(self, filepath):
		PDFExtract.__init__(self)
		self.filepath = filepath
		
	def check_if_imagemagick_installed(self):
		return "ImageMagick" in os.popen("convert --version").read()
		
	def convert_to_png(self):
		cmd = f'convert -density 600 "{self.filepath}" output.jpg'
		print(f"[+] Converting {self.filepath} to jpg")
		self.run_subprocess(cmd)
	
	def move_separate_images_to_temp_folder(self):
		self.temp_folder = self.filepath.replace(".pdf","_imgs")
		self.create_folders_if_not_exist(self.temp_folder)
		self.move_file(src="output*.jpg", dst=self.temp_folder)
	
	def convert_pdf_to_png(self):
		self.convert_to_png()
		self.move_separate_images_to_temp_folder()

			
