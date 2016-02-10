import sys
import matplotlib.pyplot as plt
import os
import math

def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			temp = map(lambda s:float(s), e.split(",")[1:])
			data.append(tuple(temp))
	return data

def all_plot(dirpath):

	files = os.listdir(dirpath)

	for f in files:
		if f.startswith("."):continue
		data = data_read(dirpath+"/"+f)
		modulo = map(lambda (x,y): (x%(2*math.pi) if (x%(2*math.pi) < math.pi) else x%(2*math.pi)-2*math.pi ,y),data)
		#modulo = map(lambda (x,y): (x%(2*math.pi),y),data)
		plt.scatter(*zip(*modulo),s=1.0)

	plt.axhline(y=0)
	plt.axvline(x=0)
	plt.xlabel("theta")
	plt.ylabel("omega")
	plt.xlim(-4,4)
	plt.ylim(-25,25)
	plt.show()


def main():
    params = sys.argv
    dirpath = params[1]
    all_plot(dirpath)

if __name__ == "__main__":
	main()
