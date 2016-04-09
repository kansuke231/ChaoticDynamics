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


def e_rr(G,g):
    m = len(G.edges())
    sigma =  sum([1 for x in G.edges() if (x[0] in g) and (x[1] in g)])
    return sigma/float(m)

def a_r(G,group):
    m = len(G.edges())
    sigma = sum([G.degree(x) for x in G.nodes() if x in group])
    return sigma/float(2*m)


def Q(G,groups):
    return sum([e_rr(G,groups[g])-(a_r(G,groups[g]))**2 for g in groups.keys()])


def graph_draw(G):

    label = {}
    for e in range(1,len(G.nodes())):
        label[e] = e

    pos = nx.spring_layout(G)

    nx.draw(G,pos,node_size = 100, width=0.4)
    plt.show()

def graph_draw_colored(G,group):
    print group

    label = {}
    for e in range(1,len(G.nodes())):
        label[e] = e

    pos = nx.spring_layout(G)
    print pos

    key = group.keys()
    nx.draw_networkx_nodes(G,pos,
                       nodelist=group[key[0]],
                       node_color='r',
                       node_size=100,)
    nx.draw_networkx_nodes(G,pos,
                       nodelist=group[key[1]],
                       node_color='b',
                       node_size=100,)

    nx.draw_networkx_labels(G,pos=pos,label=label,fontsize = 15)
    nx.draw(G,pos=pos, node_size = 0, width=0.4)

    plt.show()

def DynamicSBM_Q(filepath):

    # number of nodes
    N = 40
    Qs = []
    trajectory = data_read(filepath)

    for point in trajectory[::1]:
        
        x = point[0]
        y = point[1]
        z = point[2]

        c1 = interval_convert(9.0, -3.5, x, 1, 0)
        c2 = interval_convert(8.1, -5.7, y, 0.3, 0)
        c3 = interval_convert(7.0, 0.2, z, 0.3, 0)

        p_in, p_out = c2,c3
        n1 = int(N*c1)
        n2 = N - n1
        #print "n1: %d, n2: %d, p_in: %f, p_out: %f"%(n1,n2,p_in,p_out)
        q_temp = []
        for i in range(2):
            G = SBM_generator(n1, n2, p_in, p_out)
            g = {"g1": range(1,n1+1), "g2":range(n1+1,n1+n2+1)}
            q = Q(G, g)
            q_temp.append(q)
        #graph_draw(G)
        Qs.append(np.average(q_temp))
    return Qs

if __name__ == '__main__':
    params = sys.argv
    filepath1 = params[1]
    filepath2 = params[2]
    Qs_1 = DynamicSBM_Q(filepath1)
    Qs_2 = DynamicSBM_Q(filepath2)
    plt.plot(Qs_1)
    plt.plot(Qs_2)
    plt.show()


