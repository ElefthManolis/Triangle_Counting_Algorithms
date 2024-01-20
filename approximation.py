"""
Implementation of approximate algorithms for finding the number of triangles in a graph
"""
import os
import argparse
from utils.utils import create_graph, timeit
import numpy as np
import networkx as nx


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--graph', type=str, required=True,
                    help='The name of the graph (facebook or roads)')
    parser.add_argument('--p', type=float, required=True,
                    help='Sampling rate for edges')
    args = parser.parse_args() 
    return args


def sparsify_graph(graph: nx.Graph, p: float) -> nx.Graph:
    G_sparse = nx.Graph()
    for u,v in graph.edges():
        if np.random.random() <= p:
            G_sparse.add_edge(u,v)
    return G_sparse

@timeit
def doulion(graph: nx.Graph, p: float) -> int:
    assert 0 < p <= 1
    A = nx.to_scipy_sparse_array(graph)
    A2 = A.dot(A)
    A3 = A2.dot(A)
    nr_triangles = (1/p**3)*(A3.diagonal().sum()/6)
    return nr_triangles




def main():
    args = parse_args()
    cwd = os.getcwd()
    if args.graph == "facebook":
        graph = create_graph(cwd + '/graph_data/facebook/facebook_combined.txt')
    if args.graph == "roads":
        graph = create_graph(cwd + '/graph_data/california_road_network/roadNet-CA.txt')

    sparsed_graph = sparsify_graph(graph, args.p)
    doulion_triangles = doulion(sparsed_graph, args.p)
    print('The number of triangles is: ', doulion_triangles)

if __name__ == '__main__':
    main()