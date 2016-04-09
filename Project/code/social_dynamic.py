"""
Algorithms are based on a paper "Structure of growing social networks" by E. Jin et al. 
"""
from __future__ import division
import igraph
import networkx as nx
import random
from itertools import combinations
import collections
import numpy as np
import matplotlib.pyplot as plt


def connect_pair(G, u, v, z):
	# below returns -1 if the edge doesn't exist.
	edge_exist = G.get_eid(u, v, directed=False, error=False)
	if (edge_exist == -1) and (G.vs[u].degree() < z) and (G.vs[v].degree() < z):
		G.add_edge(u,v)	


def make_prob_dist(vs,L):
	n = len(L)
	counter = collections.Counter(L)
	return [counter[v]/n for v in vs]


def all_node_z(G, z):

	under_counts = 0

	for v in list(G.vs["name"]):
		d = G.vs[v].degree()
		print "v: %d, d: %d"%(v,d)
		if d < z:
			under_counts += 1

	print "under_counts: %d"%under_counts

	if under_counts < len(list(G.vs["name"]))*0.2:

		return True
	else:
		return False

def ne(G):
	return len(G.es)

def nm(G):
	return sum([(G.vs[v].degree())*(G.vs[v].degree() - 1) for v in list(G.vs["name"])])/2

def step1(G, np, r0, z):
	vs = list(G.vs["name"])
	pairs = combinations(vs, 2)
	for pair in random.sample(list(pairs), int(round(np*r0))):
		connect_pair(G, pair[0], pair[1], z)
	return G


def step2(G, nm, r1, z):
	vs = list(G.vs["name"])
	pool = []
	for v in vs:
		d = G.vs[v].degree()
		pool += [v for i in range(d*(d-1))]

	for v in np.random.choice(vs, int(round(nm*r1)), p=make_prob_dist(vs,pool)):
		pairs = combinations(G.neighbors(v), 2)
		selected = random.choice(list(pairs))
		connect_pair(G, selected[0], selected[1], z)

	return G

def step3(G, ne, gamma):
	vs = list(G.vs["name"])
	pool = []
	for v in vs:
		d = G.vs[v].degree()
		pool += [v for i in range(d)]

	for v in np.random.choice(vs, int(round(ne*gamma)), p=make_prob_dist(vs,pool)):
		u = random.choice(G.neighbors(v))
		print "delte %d and %d"%(v,u)
		G.delete_edges([v,u])

	return G


def init(G, np, r0, r1, z):

	while not all_node_z(G, z):
		step1(G, np, r0, z)
		step2(G, nm(G), r1, z)

	return G

def loop(G, np, r0, r1, gamma, z, n = 100):

	for i in range(n):
		print i
		step1(G, np, r0, z)
		step2(G, nm(G), r1, z)
		step3(G, ne(G), gamma)

	return G

def graph_draw(G):

    label = {}
    for e in range(1,len(G.nodes())):
        label[e] = e

    pos = nx.spring_layout(G)

    nx.draw(G,pos,node_size = 100, width=0.4)
    plt.show()

def main():
	N = 250
	z = 5
	np = N*(N-1)/2
	r0 = 0.0005
	r1 = 2
	gamma = 0.005

	G = igraph.Graph(directed=False)
	G.add_vertices(range(N))

	init(G, np, r0, r1, z)
	loop(G, np, r0, r1, gamma, z)
	
	edge_list = [e.tuple for e in G.es]
	G_nx = nx.Graph()
	G_nx.add_edges_from(edge_list)
	#graph_draw(G_nx)
	#nx.write_gml(G_nx,"output.gml")
	#G_after_init = init(G, z)
	

if __name__ == '__main__':
	main()