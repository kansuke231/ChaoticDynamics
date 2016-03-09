from __future__ import division
import sys
import matplotlib.pyplot as plt



def data_read(filepath):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			columns = e.split()
			temp = map(lambda s:float(s), columns)
			data.append(tuple(temp))
	return data

def divided_diff(x_t, x_t_1, delta_t):
	return (x_t - x_t_1)/delta_t

def plot(data):
	plt.scatter(*zip(*data))
	#plt.ylim(-5,5)
	plt.xlabel("Theta")
	plt.ylabel("Omega")
	plt.show()

def q1(data):
	result = []
	dt = data[1][1] - data[0][1]
	x_t_1 = data[0][0]

	for d in data[1::50]:
		x_t = d[0]
		omega = divided_diff(x_t, x_t_1, dt)
		result.append((x_t,omega))
		x_t_1 = x_t
	
	plot(result)

def reconstruction(data,tau,m,j,k):
	result = []
	for i in xrange(len(data)):
		if (i + m*tau) >= len(data):
			break
		else:
			temp = []
			for offset in range(m):
				temp.append(data[i + offset*tau][0])
			result.append(tuple(temp))

	selected = []
	for r in result:
		temp = []
		for i,e in enumerate(r):
			if i == j or i == k:
				temp.append(e)
		selected.append(tuple(temp[::-1]))

	plt.xlabel("k")
	plt.ylabel("j")
	plt.scatter(*zip(*selected),s=0.01)
	plt.show()



def main(filepath):
	data = data_read(filepath)
	#q1(data)
	reconstruction(data, 1, 7, 0, 6)

if __name__ == '__main__':
	args = sys.argv
	filepath = args[1]
	main(filepath)