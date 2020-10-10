from PDFpy import PDFExtract
from PreProcessing.image_processing import ImageProcessing
from PreProcessing.box_extraction import BoxExtraction
from ocr_extract import OCRExtract
import sys
import cv2
import os
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

		

if __name__=="__main__":
	get_banner()
	argparser = ArgumentParser(description="OCR and pdf extract tool\n\nCommandline argument -h for help.\n")
	argparser.add_argument(
		"-p", "--pdf",
		help = "PDF filepath to extract",
	)
	
	argparser.add_argument(
		"-i", "--image",
		help = "filepath to image to perform OCR extraction. Must be '.jpg'"
	)
	
		
	args = argparser.parse_args()
	if args.pdf:
		pdf = args.pdf
		print(f"[*] Extracting pdf {pdf}...")
		##code for pdf extraction
		pdf_extract = PDFExtract()
		full_text = pdf_extract.get_full_text(pdf, form="-raw", output="full_text.txt")
		if not pdf_extract.is_scanned(full_text):
			pdf_extract.seperate_pages(pdf)
			pdf_extract.extract_each_page(pdf)
		else:
			print("[-] The pdf is empty, possibly scanned...")
			print("[*] Performing OCR extraction...")
			##TODO: add OCR pipeline
		

	

	
	
