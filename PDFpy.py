import re
from glob import glob
import subprocess
from system_class import System



class PDFExtract(System):
	def get_full_text(self, filepath, form="-raw", output="full_text.txt"):
		 print("[*] Extracting full document raw...")
		 extract_text_cmd = r"""{} "{}" "{}" "{}" -enc UTF-8""".format('pdftotext', form, filepath, output)
		 self.run_subprocess(extract_text_cmd)
		 full_text = self.read_text(output)
		 full_text = full_text.replace("\x0c","")
		 return full_text


	def seperate_pages(self, filepath):
		##split pdf into separate pages
		print("[*] Separating pdf pages...")
		page_name = "output-%d.pdf"
		separate_pages = r"""{} "{}" "{}" """.format('pdfseparate', filepath, page_name)
		self.run_subprocess(separate_pages)
		
		 
	def is_scanned(self, text):
		 print("[*] Checking if the pdf file is scanned...")
		 return not text.strip()
		

	def extract_each_page(self, filename):
		##create new temp folder
		print("[*] Creating new folder for text extraction...")
		self.temp_folder = filename.replace(".pdf","_pdf_pages")
		self.create_folders_if_not_exist(self.temp_folder)
		
		print("[*] Performing extraction based on tabular layout of the document...")
		##loop through all pages extract text
		seperate_pages = glob("output*.pdf")
		for npage, page in enumerate(seperate_pages):
			output = ''.join(page.split(".")[:-1])+".txt"
			self.get_full_text(page, form="-layout", output=output)
			self.update_progress("PDF text extraction", npage, len(seperate_pages))
		##move all pages to temp folder
		self.move_file("output*.*", self.temp_folder)
		print("[+] Extracted text sitting in {}".format(self.temp_folder))
		
	
