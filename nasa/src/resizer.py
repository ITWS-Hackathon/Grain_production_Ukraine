"""
@author: Max Marshall
@desc: Resizes the massive TIFF files I'm dealing with,
I only have so much room on my drive.
"""
from PIL import Image
import os
import math
import numpy as np


def resize(original,new,x,y):
	if (os.path.exists(original)):
		print("BEGINNING: {}".format(original))
		o_image = Image.open(original)
		new_image = Image.new("RGB",size=(x,y))
		mx,my = o_image.size
		dx,dy = mx/float(x),my/float(y)
		for px in range(x):
			for py in range(y):
				psum = [0,0,0]
				cx,cy = math.floor(dx*px),math.floor(dy*py) # Top Corners of pixel groups
				# Now grab all of the pixels in range of subgroup,
				# check their relative value, and add them to the sum
				for sx in range(cx,math.ceil(cx+dx)+1):
					for sy in range(cy,math.ceil(cy+dy)+1):
						modifier = min((abs((dx*(px+.5))-sx),1))*min(((abs((dy*(py+.5))-sy)),1)) # How much of pixel to include
						if (sx<mx and sy<my): # Only access elements from in image
							psum = np.add(np.multiply(o_image.getpixel((sx,sy)),modifier),psum)
				p_avg = np.divide(psum,dx*dy)
				new_image.putpixel((px,py),(round(p_avg[0]),round(p_avg[1]),round(p_avg[2])))
		new_image.save(new)
		print("FINISHED: {}".format(original))
		o_image.close()
		new_image.close()


if __name__ == '__main__':
	year = 2020
	x,y = 1500,1500
	for day in range(241,250,8):
		resize("../improved_data/{0}-{1:03d}.tif".format(year,day),"../improved_data/{0}-{1:03d}_x{2}y{3}.tif".format(year,day,x,y),x,y)