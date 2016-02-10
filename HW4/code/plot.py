import sys
import matplotlib.pyplot as plt

def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			temp = map(lambda s:float(s), e.split(",")[1:])
			data.append(tuple(temp))
	return data

def plot(data):
	plt.scatter(*zip(*data),s=0.5)
	plt.plot(data[0][0], data[0][1], "ro")
	plt.axhline(y=0)
	plt.axvline(x=0)
	plt.xlabel("theta")
	plt.ylabel("omega")
	#plt.xlim(-22,22)
	#plt.ylim(-22,22)
	plt.show()


def main():
    params = sys.argv
    filepath = params[1]
    data = data_read(filepath)
    plot(data)

if __name__ == "__main__":
	main()
