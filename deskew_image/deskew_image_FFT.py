#!/bin/python

import numpy as np
import pylab as plt
from sklearn.decomposition import PCA
import cv2
import sys


def linear_fit(x, y):
	n = len(x)
	denom = n * sum(x**2) - sum(x)**2
	slope = (n*sum(x*y) - sum(x)*sum(y))/denom
	intercept = (sum(y) - slope*sum(x))/n
	return slope, intercept
    
    
def scale_data(x, y, hi, lo):
    x_scaled = (hi - lo)*(x - min(x))/(max(x) - min(x))
    y_scaled = (hi - lo)*(y - min(y))/(max(y) - min(y))
    return x_scaled, y_scaled


def correct_angle(angle):
	if angle < -45:
		angle = -(90 + angle)
	# otherwise, just take the inverse of the angle to make
	# it positive
	elif angle > 135:
		angle = -(angle - 180)
	else:
		angle = -angle
	return angle
	
	
img_filepath = sys.argv[1]

print("deskewing {}".format(img_filepath))
image = cv2.imread(img_filepath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

print("applying fft to image...")
fft_image = np.fft.fft2(thresh)
fft_image = np.fft.fftshift(fft_image)
magnitude_spectrum = 20*np.log(abs(fft_image))
cv2.imwrite("magnitude_spectrum.jpg",magnitude_spectrum)

##for fft method
x, y = np.where(np.flipud(magnitude_spectrum)>=255)
angle1 = np.arctan2(max(y)-min(y), max(x)-min(x))*180/np.pi 
print("Angle 1:{}".format(angle1))

x_scaled, y_scaled = scale_data(x, y, 1, 0)
slope, intercept = linear_fit(x, y)
y_fit = slope*x + intercept
angle2 = np.arctan2(max(y_fit)-min(y_fit), max(x) - min(x))*180/np.pi
print("Angle 2: {}".format(angle2))

print("Applying pca...")
pca = PCA(n_components=1)
data = np.column_stack([x,y])
pca.fit(data)
first_comp = pca.transform(data)
first_comp_inv = pca.inverse_transform(first_comp)
x_pca, y_pca = first_comp_inv.T
angle3 = np.arctan2(max(y_pca)-min(y_pca),max(x_pca)-min(x_pca))*180/np.pi
print("Angle 3: {}".format(angle3))

##for pca and linear fit mnethod
print("Applying linear fit method...")
y, x = np.where(np.flipud(thresh==255))
#linear
x_scaled, y_scaled = scale_data(x, y, 1, 0)
slope, intercept = linear_fit(x, y)
y_fit = slope*x + intercept
angle4 = np.arctan2(max(y_fit)-min(y_fit),max(x)-min(x))*180/np.pi
print("Angle 4: {}".format(angle4))

#pca
pca = PCA(n_components=1)
data = np.column_stack([x,y])
pca.fit(data)
first_comp = pca.transform(data)
first_comp_inv = pca.inverse_transform(first_comp)
x_pca, y_pca = first_comp_inv.T
angle5 = np.arctan2(max(y_pca)-min(y_pca),max(x_pca)-min(x_pca))*180/np.pi
print("Angle 5: {}".format(angle5))


print("Applying box detection method...")
##for bounding box method
coords = np.column_stack(np.where(thresh > 0))
angle6 = cv2.minAreaRect(coords)[-1]
print("Angle 6: {}".format(angle6))
