"""
@author: Max Marshall
@desc: Converting NASA images to data
"""
from PIL import Image
import os


def color_image_to_data(filename, year, day):
	if (os.path.exists(filename)):
		o_image = Image.open(filename)
		num_pixels = 0.0
		ndvi_sum = 0.0
		for px in range(o_image.size[0]):
			for py in range(o_image.size[1]):
				value = o_image.getpixel((px,py))
				#print(value)
				if value[2] == 0 and not (value[0]==0 and value[1]==0):
					ndvi_sum += (value[1]-127)/128.0 
					num_pixels += 1.0
					#print(ndvi_sum)
		ndvi_avg = ndvi_sum/num_pixels
		print("{0}-{1:03d} ==> {2:.03f} -- Data from {3} pixels".format(year,day,ndvi_avg,int(num_pixels)))
		o_image.close()
		return "{0}-{1:03d}".format(year,day), ndvi_avg, num_pixels
	return None, None, None


def gray_image_to_data(filename, year, day):
	if (os.path.exists(filename)):
		o_image = Image.open(filename)
		num_pixels = 0.0
		ndvi_sum = 0.0
		for px in range(o_image.size[0]):
			for py in range(o_image.size[1]):
				value = o_image.getpixel((px,py))
				#print(value)
				if value <= 250:
					ndvi_sum += (value)/250.0 
					num_pixels += 1.0
		ndvi_avg = ndvi_sum/num_pixels
		print("{0}-{1:03d} ==> {2:.03f} -- Data from {3} pixels".format(year,day,ndvi_avg,int(num_pixels)))
		o_image.close()
		return "{0}-{1:03d}".format(year,day), ndvi_avg, num_pixels
	return None, None, None


if __name__ == '__main__':
	year = 2018
	filename = "../temp/{}.csv".format(year)
	f = open(filename,"w+")
	f.write("Date,NDVI_avg,Num_Pixels\n")
	f.close()
	ndvi_total = 0.0
	for day in range(1,366,8):
		date,ndvi,pix = gray_image_to_data("../nasa_data/{0}-{1:03d}.tif".format(year,day),year,day)
		if date is not None:
			ndvi_total += ndvi
			f = open(filename,"a")
			f.write("{0},{1:.03f},{2}\n".format(date,ndvi,pix))
			f.close()
	print("NDVI Year Total: {:.03f}".format(ndvi_total))