
import math
import matplotlib.pyplot as plt


def plot(data,marker):
	data_log = map(lambda e: (math.log(1.0/e[0]), math.log(e[1])), data)
	print data_log
	plt.plot(*zip(*data_log),marker=marker)
	plt.ylabel(r"$\log N(\epsilon)$", fontsize=20)
	plt.xlabel(r'$\log (\frac{1}{\epsilon})$', fontsize=20)


	

if __name__ == '__main__':
	data_1 = [#(5, 380), (4, 554), (3, 907), (2, 1645),\
			(0.9, 4615), (0.8, 5242), (0.7, 5947), (0.6, 6872),\
			(0.5, 8090), (0.4, 9731)]
	data_2 = [(0.9, 7403), (0.8, 8760), (0.7,10358), (0.6,12651),\
			  (0.5, 15829), (0.4, 20237)]
	#data_3 for q2c. m = 3
	data_3 = [(0.9, 3198), (0.8,3692), (0.7, 4333), (0.6, 5194),\
			  (0.5, 6342), (0.4, 7865)]

	plot(data_1,"o")
	plot(data_2,"v")
	plot(data_3,"^")
	plt.show()