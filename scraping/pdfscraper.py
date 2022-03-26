import tabula as tb
import pandas as pd
import numpy as np


if __name__ == '__main__':
	filename = "UkraineMarch2021.pdf"
	data = tb.read_pdf(filename, pages = '8',lattice=True)
	#print(data)
	#print(type(data))
	data.pop(0)
	df = pd.DataFrame(np.concatenate(data))
	df.dropna(inplace=True)
	df.to_csv("annual_costs.csv")