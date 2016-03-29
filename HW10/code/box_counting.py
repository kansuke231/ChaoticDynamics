import numpy as np
import sys

OFFSET = 100

def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			columns = e.split(",")
			temp = map(lambda s:float(s)+OFFSET, columns[1:])
			data.append(tuple(temp))
	return data

def data_read_delay(filepath,t,m):
	data = []
	with open(filepath,"r") as f:
		lines = list(f.readlines())
		for i,e in enumerate(lines):
			try:
				temp = []
				for j in range(m):
					temp.append(float(lines[i+(t*j)]))
				data.append(tuple(temp))

			except:
				return data

		
	return data

def box_counting(data,e,d):
	
	L = round(d/e)
	M = np.zeros((L, L, L))

	for p in data:
		i = round(p[0]/e)
		j = round(p[1]/e)
		k = round(p[2]/e)
		M[i][j][k] = 1

	unique, counts = np.unique(M, return_counts=True)

	return counts[1]

def main(data):
	print box_counting(data, 0.4, 500)

if __name__ == "__main__":
	args = sys.argv
	filepath = args[1]
	data = data_read_delay(filepath, 105, 3)
	main(data)
