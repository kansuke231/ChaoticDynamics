import sys
import matplotlib.pyplot as plt


def double_trajectory(R,x0,m):
	
	xs1 = [0 for i in range(m)]
	xs1[0] = x0
	
	xs2 = [0 for i in range(m)]
	xs2[0] = x0 + 0.000001
	
	# for x_n versus n
	for i in range(1,m):
		xs1[i] = R*xs1[i-1]*(1-xs1[i-1]) 
		xs2[i] = R*xs2[i-1]*(1-xs2[i-1])

	plt.plot(xs1, label="x_0 = 0.2", linestyle="-")
	plt.plot(xs2, label="x_0 = 0.200001",linestyle="--")
	plt.xlabel("n")
	plt.ylabel("x_n")
	plt.legend()
	plt.show()

def main(R,x0,m,k):
	xs = [0 for i in range(m)]
	xs[0] = x0
	
	# for x_n versus n
	for i in range(1,m):
		xs[i] = R*xs[i-1]*(1-xs[i-1]) 
	
	xs = xs[k:]
	plt.xlabel("n")
	plt.ylabel("x_n")
	plt.ylim(0,1)
	plt.scatter([i+k for i in range(len(xs))],xs)
	plt.show()

	# for x_n+1 versus x_n
	ys = xs[1:]
	plt.xlabel("x_n")
	plt.ylabel("x_n+1")
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.scatter(xs[:-1],ys)
	plt.show()
	
	# for x_n+2 versus x_n
	ys = xs[2:]
	plt.xlabel("x_n")
	plt.ylabel("x_n+2")
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.scatter(xs[:-2],ys)
	plt.show()
	

if __name__ == "__main__":
	params = sys.argv
	R = float(params[1])
	x0 = float(params[2])
	m = int(params[3])
	k = int(params[4])
	main(R,x0,m,k)
	#double_trajectory(R,x0,m)	
