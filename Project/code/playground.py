import sys


def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			columns = e.split(",")
			temp = map(lambda s:float(s), columns[1:])
			data.append(tuple(temp))
	return data

def max_min(*column):
	for i,e in enumerate(column):
		print "----------- %d -----------"%i
		print "min:%f  max:%f" %(min(e),max(e))


def main(filepath):
	data = data_read(filepath)
	max_min(*zip(*data))


if __name__ == '__main__':
	params = sys.argv
	filepath = params[1]
	main(filepath)
