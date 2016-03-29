import sys
import random
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import numpy as np

def data_read(filepath):
    data = []
    with open(filepath,"r") as f:
        for e in f.readlines():
            columns = e.split(",")
            temp = map(lambda s:float(s), columns[1:])
            data.append(tuple(temp))
    return data

def edge_generator(n1_nodes, n2_nodes, p_in, p_out):
    """
    input -> a list of vertices, n1_nodes and n2_nodes and probabilities p_in and p_out
    output -> a list of edges between vertices in two groups conditioned on p_in and p_out
    """

    e_gen = lambda n1,n2,p: [e for e in [x for x in itertools.product(n1,n2) if x[0]!=x[1]] if random.random()<p]

    between_es = e_gen(n1_nodes, n2_nodes, p_out)
    in_n1 = e_gen(n1_nodes, n1_nodes, p_in)
    in_n2 = e_gen(n2_nodes, n2_nodes, p_in)

    return between_es + in_n1 + in_n2


def SBM_generator(n1,n2,p_in,p_out):
    n1_nodes = [x for x in range(1,n1+1)]
    n2_nodes = [x for x in range(n1+1,n1+n2+1)]

    all_edges = edge_generator(n1_nodes, n2_nodes, p_in, p_out)

    G = nx.Graph()
    G.add_edges_from(all_edges)

    return G

def interval_convert(old_interval, old_min, old_val, new_interval, new_min):
    return (old_val - old_min)*new_interval/old_interval + new_min

def graph_draw(G):

    label = {}
    for e in range(1,len(G.nodes())):
        label[e] = e

    pos = nx.spring_layout(G)

    nx.draw(G,pos,node_size = 100, width=0.4)
    plt.show()

def main(filepath):

    # number of nodes
    N = 40

    trajectory = data_read(filepath)

    for point in trajectory[::20]:
        
        x = point[0]
        y = point[1]
        z = point[2]

        c1 = interval_convert(62, -30, x, 1, 0)
        c2 = interval_convert(86, -42, y, 2, -1)
        c3 = interval_convert(82, 5, z, 1, 0)

        a = np.array([[1,1], [1,-1]])
        b = np.array([c1, c2])

        ans = np.linalg.solve(a, b)
        p_in, p_out = ans
        n1 = int(N*c3)
        print n1
        n2 = N - n1

        G = SBM_generator(n1, n2, p_in, p_out)
        graph_draw(G)

if __name__ == '__main__':
    params = sys.argv
    filepath = params[1]
    main(filepath)


