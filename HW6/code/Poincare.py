import sys
import matplotlib.pyplot as plt
import os
import math
import numpy as np

L = 0.1
g = 9.8
alpha = math.sqrt(g/L)*(3.0/4.0)
t_drive = (2*math.pi)/alpha

def data_read(filepath,t_flag=True):
	data = []
	with open(filepath,"r") as f:
		for e in f.readlines():
			columns = e.split(",")
			temp = map(lambda s:float(s), columns[1:])
			if t_flag:
				time = [float(columns[0][2:])]
				data.append(tuple(time+temp))
			else:
				data.append(tuple(temp))
	return data



def interpolation(p1,p2,nT):
	t = [p1[0], p2[0]]
	theta = [p1[1], p2[1]]
	omega = [p1[2], p2[2]]
	new_p_theta = np.interp(nT,t,theta)
	new_p_omega = np.interp(nT,t,omega)
	return (new_p_theta,new_p_omega)

def interpolation_spatial(p1,p2,plane):
	x = [p1[0], p2[0]]
	y = [p1[1], p2[1]]
	z = [p1[2], p2[2]]
	new_x = np.interp(plane,y,x)
	new_z = np.interp(plane,y,z)
	return (new_x,new_z)

def Poincare_map_time_overlap(data,T):
	"""
	data = [(t_0,theta_0,omega_0),...]
	"""
	points = []
	interpolated = []
	prev = tuple(data[0])
	post = None
	n = 1
	for e in data:
		post = tuple(e)
		if e[0] > n*T:
		#if e[0] % (T) < 0.01:
			#print "Modulo:",e[0]
			points.append((e[1],e[2]))
			interpolated.append(interpolation(prev, post, n*T))
			n += 1
		prev = tuple(e)
	print n

	#modulo = map(lambda (x,y): (x%(2*math.pi) if (x%(2*math.pi) < math.pi) else x%(2*math.pi)-2*math.pi ,y),points)
	#plt.scatter(*zip(*modulo),c="r",s=25.0)

	modulo_interpolated = map(lambda (x,y): (x%(2*math.pi) if (x%(2*math.pi) < math.pi) else x%(2*math.pi)-2*math.pi ,y),interpolated)
	plt.scatter(*zip(*modulo_interpolated),c="b",s=25.0)

	plt.axhline(y=0)
	plt.axvline(x=0)
	plt.xlabel("theta")
	plt.ylabel("omega")
	plt.show()

def Poincare_map_time(data,T):
	"""
	data = [(t_0,theta_0,omega_0),...]
	"""
	points = []
	n = 1
	for e in data:
		#if e[0] > n*T:
			#print "Non-modulo:",e[0],n*T
		if e[0] % (T) < 0.05:
			#print "Modulo:",e[0]
			points.append((e[1],e[2]))
			
			n += 1
	print n

	modulo = map(lambda (x,y): (x%(2*math.pi) if (x%(2*math.pi) < math.pi) else x%(2*math.pi)-2*math.pi ,y),points)
	plt.scatter(*zip(*modulo),c="r",s=0.1)

	plt.axhline(y=0)
	plt.axvline(x=0)
	#plt.xlim(-4,4)
	plt.xlabel("theta")
	plt.ylabel("omega")
	plt.show()

def Poincare_interpolation(data,T):

	points = []
	n = 1
	prev = tuple(data[0])
	post = None

	for e in data[1:]:
		post = tuple(e)
		
		#if e[0] > n*T:
		if e[0] % T < 0.05:
			points.append(interpolation(prev, post, n*T))
			n += 1

		prev = tuple(e)
	print n

	return points

def Poincare_q3a(data):

	points = []
	prev = data[0]
	post = None

	for e in data[1:]:
		post = e
		if ((e[1] - 20) <= 0.1) and ((e[1] - 20) > 0):
			points.append(interpolation_spatial(prev, post, 20))
		prev = e

	return points

def Poincare_q3b(data):

	points = []
	prev = data[0]
	post = None

	for e in data[1:]:
		post = e
		x = e[0]
		y = 2*x
		if ((e[1] - y) <= 0.1) and ((e[1] - y) > 0):
			interpolated = interpolation_spatial(prev, post, y)
			points.append((interpolated[0]*math.sqrt(5),interpolated[1]))
		prev = e

	return points




def just_plot(data):
	#data_converted = [(theta,omega) for t,theta,omega in data]
	modulo = map(lambda (x,y): (x%(2*math.pi) if (x%(2*math.pi) < math.pi) else x%(2*math.pi)-2*math.pi ,y),data)
	plt.scatter(*zip(*modulo),c="r",s=3)
	plt.axhline(y=0)
	plt.axvline(x=0)
	plt.xlim(-4,4)
	plt.xlabel("theta")
	plt.ylabel("omega")
	plt.show()



def main():
    params = sys.argv
    filepath = params[1]
    data = data_read(filepath,t_flag=True)
    Poincare_map_time(data, t_drive/math.pi)
    #just_plot(data)
    #section = Poincare_interpolation(data, t_drive)
    #just_plot(section)
    #spatial_section1 = Poincare_q3b(data)
    #just_plot(spatial_section1)


if __name__ == "__main__":
	main()