import sys
import matplotlib.pyplot as plt
import numpy as np


def HenonMap(m,interval):
	a = 1.4
	b = 0.3
	x0 = 0.1
	y0 = 0

	xs = [x0]

	xk = x0
	yk = y0
	for i in np.arange(1,m):
		yk_1 = b*xk
		xk_1 = yk + 1 - a*(xk**2) 

		xs.append(xk_1)

		xk = xk_1
		yk = yk_1

	#plt.scatter([i for i in range(m)], xs)

	# for x_n+1 vs. x_n plot
	plt.xlabel("x_n")
	plt.ylabel("x_n+1")
	plt.scatter(xs[:m-1],xs[1:]) 
	plt.show()

def HenonMapBifurcation(m,L,interval):

	b = 0.3
	result = []
	
	for a in np.arange(0, 1.4, interval):

		x0 = 0.1
		y0 = 0
		xs = [x0]
	
		xk = x0
		yk = y0

		for i in np.arange(1,m):
			yk_1 = b*xk
			xk_1 = yk + 1 - a*(xk**2) 
			
			xs.append(xk_1)
	
			xk = xk_1
			yk = yk_1

		xs = xs[L:]
		result.append(xs)

	print "Done calculation!"

	for a, xs in zip(np.arange(0, 1.4, interval), result):
		print a
		for p in xs:
			plt.scatter(a,p,s=1.0)
	
	plt.xlabel("alpha")
	plt.ylabel("x_n")
	plt.ylim(-2,2)
	plt.xlim(-0.01, 1.41)
	plt.show()



def main(m,L,interval):

	x0 = 0.2

	R_start = 3.4
	R_end = 3.6

	result = []
	for R in np.arange(R_start, R_end, interval):

		xs = [0 for i in range(m)]
		xs[0] = x0
	
		for i in np.arange(1,m):
			xs[i] = R*xs[i-1]*(1-xs[i-1]) 
	
		xs = xs[L:]
		result.append(xs)
	
	for R, xs in zip(np.arange(R_start, R_end, interval), result):
		for p in xs:
			plt.scatter(R,p,s=1.0)
	
	plt.xlabel("R")
	plt.ylabel("x_n")
	plt.ylim(0.3, 0.9)
	plt.xlim(R_start, R_end)
	plt.show()

	

if __name__ == "__main__":
	params = sys.argv
	
	m = int(params[1])
	L = int(params[2])
	interval = float(params[3])

	#main(m,L,interval)
	#HenonMapBifurcation(m, L, interval)
	HenonMap(m, interval)

