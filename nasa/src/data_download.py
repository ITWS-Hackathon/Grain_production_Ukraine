"""
@author: Max Marshall
@desc: This utility downloads agriculture maps of Ukraine
"""
import gzip
import requests
import shutil
import os
import time


def download_tif(base,year,day,x_coord,y_coord):
	file_request = "GMOD09Q1.A{0}{1:03d}.08d.latlon.x{2:02d}y{3:02d}.6v1.NDVI.tif.gz".format(year,day,x_coord,y_coord)
	print(file_request)
	this_req = base+"{0}/{1:03d}/".format(year,day)+file_request
	print(this_req)
	r = requests.get(this_req, allow_redirects=True)
	if(r.status_code) != 200:
		return None
	f = open("../temp/{}".format(file_request),"w+b")
	f.write(r.content)
	f.close()
	return file_request

def unzip(file, new_file):
	try:
		f = gzip.open(file,"rb")
		g = open(new_file, "w+b")
		shutil.copyfileobj(f,g)
		f.close()
		g.close()
		os.remove(file)
	except FileNotFoundError:
		print("Something fucked up")

if __name__ == '__main__':
	nasa_web_dir = "https://gimms.gsfc.nasa.gov/MODIS/std/GMOD09Q1/tif/NDVI/"
	x_coord = 23
	y_coord = 4
	for year in range(2020, 2023):
		day = 1
		while (day < 366):
			file = download_tif(nasa_web_dir,year,day,x_coord,y_coord)
			if file is not None:
				unzip("../temp/"+file,"../nasa_data/{0}-{1:03d}.tif".format(year,day))
			day += 8
			time.sleep(.1)
	
