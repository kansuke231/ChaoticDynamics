import sys
import matplotlib.pyplot as plt


def main(R,x0,m):
	ys = [0 for i in range(m)]
	ys[0] = x0

	for i in range(1,m):
		ys[i] = R*ys[i-1]*(1-ys[i-1]) 

	plt.plot(ys)
	plt.show()	

if __name__ == "__main__":
	params = sys.argv
	R = float(params[1])
	x0 = float(params[2])
	m = int(params[3])
	main(R,x0,m)
