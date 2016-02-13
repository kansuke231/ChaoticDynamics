import sys
import matplotlib.pyplot as plt
import os


def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			temp = map(lambda s:float(s), e.split(",")[1:])
			data.append((temp[0],temp[2]))
	return data

def all_plot(dirpath):

	files = os.listdir(dirpath)

	for f in files:
		if f.startswith("."):continue
		data = data_read(dirpath+"/"+f)
		plt.scatter(*zip(*data),s=1.0)

	plt.axhline(y=0)
	plt.axvline(x=0)
	plt.xlabel("theta")
	plt.ylabel("omega")
	#plt.xlim(-4,4)
	#plt.ylim(-25,25)
	plt.show()


def main():
    params = sys.argv
    dirpath = params[1]
    all_plot(dirpath)

if __name__ == "__main__":
	main()
