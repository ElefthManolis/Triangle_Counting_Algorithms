"""
Implementation of exacts algorithms for finding the number of triangles in a graph
"""

import os
import argparse
import networkx as nx
from tqdm import tqdm
from utils.utils import create_graph, timeit
from itertools import combinations




def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--graph', type=str, required=True,
                    help='The name of the graph (facebook or roads)')
    args = parser.parse_args() 
    return args


@timeit
def all_triplets(graph: nx.Graph) -> int:
    cnt_triangles = 0
    for i,j,k in tqdm(combinations(graph.nodes, 3)):
        if graph.has_edge(i,j) and graph.has_edge(j,k) and graph.has_edge(i,k):
            cnt_triangles += 1
    return cnt_triangles


@timeit
def node_iterator(graph: nx.Graph) -> int:
    cnt_triangles = 0
    for i in tqdm(graph.nodes):
        for j,k in combinations(graph.neighbors(i),2):
            if graph.has_edge(j,k):
                cnt_triangles += 1
    return cnt_triangles/3

@timeit
def compact_forward() -> int:



def main():
    args = parse_args()
    cwd = os.getcwd()
    if args.graph == "facebook":
        graph = create_graph(cwd + '/graph_data/facebook/facebook_combined.txt')
    if args.graph == "roads":
        graph = create_graph(cwd + '/graph_data/california_road_network/roadNet-CA.txt')

    print(graph)

    # Brute Force exact algorithm
    at_triangles = all_triplets(graph)
    print('The number of triangles is: ', at_triangles)

    # Node Iterator exact algorithm
    ni_triangles = node_iterator(graph)
    print('The number of triangles is: ', ni_triangles)



if __name__ == '__main__':
    main()