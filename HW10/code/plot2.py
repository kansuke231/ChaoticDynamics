import matplotlib.pyplot as plt
import sys

def data_read(filepath):
	data = []

	with open(filepath,"r") as f:
		for e in f.readlines():
			
			if "#dim" in e:
				print e
				data.append("token")
			else:
				columns = e.split(" ")
				temp = map(lambda s:float(s), columns)
				data.append(tuple(temp))
	return data

def plot(data):
	plt.plot(*zip(*data),marker="o")
	#plt.yscale("log")
	plt.xscale("log")
	plt.xlabel(r"$\epsilon$", fontsize=20)
	plt.ylabel(r'$D(m,\epsilon)$', fontsize=20)

def main(filepath):
	data = data_read(filepath)
	temp = []
	for e in data[1:]:
		if e == "token":
			plot(temp)
			temp = []
		else:
			temp.append(e)
	plt.show()

if __name__ == "__main__":
	args = sys.argv
	filepath = args[1]
	main(filepath)
