"""
@author: Max Marshall
@desc: Converts .tif files provided by NASA's GIMMS Databse
into a format that is more visually helpful
"""
import os
from PIL import Image

def convert(original,new):
	if (os.path.exists(original)):
		print("BEGINNING: {}".format(original))
		o_image = Image.open(original)
		new_image = Image.new("RGB",size=o_image.size)
		for px in range(o_image.size[0]):
			for py in range(o_image.size[1]):
				value = o_image.getpixel((px,py))
				r,g,b=0,0,0
				if value > 250:
					if value == 254:
						b=255
					elif value == 255:
						r,g,b=255,255,255
				else:
					scalar = (value-125) * .008
					g = int(scalar*128+127)
					r = int(scalar*-128+127)
				new_image.putpixel((px,py),(r,g,b))
		#new_image.show()
		new_image.save(new)
		print("FINISHED: {}".format(original))
		o_image.close()
		new_image.close()



if __name__ == '__main__':
	year = 2020
	for day in range(1,365,8):
		convert("../nasa_data/{0}-{1:03d}.tif".format(year,day),"../improved_data/{0}-{1:03d}.tif".format(year,day))
