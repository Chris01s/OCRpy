import os
import sys
from glob import glob
import time
import shutil
import subprocess
import cv2
from PIL import Image


class System:
	def read_image_PIL(self, filepath):
		try:
			print("[+] Reading image...")
			return Image.open(filepath)
		except FileNotFoundError as fnfe:
			raise FileNotFoundError(fnfe.__str__)
			return None

	def read_image_cv2(self, filepath):
		try:
			print("[+] Reading image...")
			return cv2.imread(filepath, 0)
		except FileNotFoundError as fnfe:
			raise FileNotFoundError(fnfe.__str__)
			return None
			
			
	def read_text(self, filepath):
		try:
			with open(filepath, "r") as FILE_OBJ:
				text = FILE_OBJ.read()
			return text
		except FileNotFoundError as fnfe:
			raise FileNotFoundError(fnfe.__str__)
			return None
		
		
	def update_progress(self, job_title, progress, length):
		if (progress+1)/length == 1:
			print("[+] "+job_title+": "+"#"*length+"Done!", end='\n')
		else:
			msg = "[+] "+job_title+": "
			msg += '#'*progress
			msg += " "*(length-progress)
			msg += str(int((progress+1)/length *100))+"%"
			print(msg, end='')
			print('\b'*len(msg), end='', flush=True)
		 
	
	def clean_filename(self, filepath):
		print(f"[*] Cleaning filepath {filepath}...")
		filename = os.path.basename(filepath)
		directory = filepath.replace(filename, "")
		filename = filename.replace(" ","_")
		for punct in string.punctuation:
			if punct in ".":
				filename = filename.replace(punct, "_")
		new_filepath = os.path.join(directory, filename)
		self.move_file(filepath, new_filepath)
		print(f"[*] filename Changed...")
		return new_filepath
		     
		     
	def create_folders_if_not_exist(self, dir_name):
		if not os.path.isdir(dir_name):
			print("[*] creating '"+dir_name+"' folder...")
			os.makedirs(dir_name)
		else:
			print(f"[!] {dir_name} already exists...")
			
			
	def move_file(self, src, dst):
		try:
			if os.system(f'mv {src} {dst}'):
				raise Exception(f"Couldn't move {src} to {dst}")
		except Exception as ex:
			print(f"[!!] {ex.__str__()}")
			
	
	def delete_file(self, src):
		try:
			os.remove(src)
		except Exception as ex:
			try:
				os.system(f"rm {src}")
			except Exception as ex:
				print(f"[!] {ex.__str__()}")
			
			
	def delete_folder(self, src):
		try:
			shutil.rmtree(src)
		except Exception as ex:
			try:
				os.system("rm -rf {src}")
			except Exception as ex:	
				print(f"[!] {ex.__str__()}")
			


	def del_files_under_limit(self, dir_path, file_ext, limit):
		 '''
		 deletes all the images in a folder (dir_path)
		 under file size limit (limit). Used for deleting scrap cropped images
		 '''
		 files = glob(dir_path+f"/*.{file_ext}")
		 for nFile, File in enumerate(files):
		     self.update_progress(
		     		"Deleting scrap cropped images",
		     		nFile,
		     		len(files)
		     )
		     file_size = os.path.getsize(File)
		     if file_size < limit:
		         os.remove(File)

	

	def del_files_over_limit(self, dir_path, file_ext, limit):
		 '''
		 deletes all the images in a folder (dir_path)
		 under file size limit (limit). Used for deleting scrap cropped images
		 '''
		 files = glob(dir_path+f"/*.{file_ext}")
		 for nFile, File in enumerate(files):
		     self.update_progress(
		     		"Deleting scrap cropped images",
		     		nFile,
		     		len(files)
		     )
		     file_size = os.path.getsize(File)
		     if file_size > limit:
		         os.remove(File)
		         
		         
	def run_subprocess(self, cmd):
		try:
		 	subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)
		except Exception as ex:
	 		raise Exception("Could not scrape PDF: " + ex.__str__())
