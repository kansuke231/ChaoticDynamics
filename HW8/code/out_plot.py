from __future__ import division
import sys
import matplotlib.pyplot as plt



def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			columns = e.split()
			temp = map(lambda s:float(s), columns[:2])
			data.append(tuple(temp))
	return data

def plot(data):
	plt.scatter(*zip(*data))
	#plt.ylim(-5,5)
	plt.axhline(0.1)
	plt.xlabel("embedding demension m")
	plt.ylabel("the ratio false neighbors")
	plt.show()

def main(filepath):
	data = data_read(filepath)
	plot(data)

if __name__ == '__main__':
	args = sys.argv
	filepath = args[1]
	main(filepath)