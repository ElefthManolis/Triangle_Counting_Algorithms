"""
Implementation of streaming algorithm for finding the number of triangles in a graph
"""


import os
import argparse
import random
import networkx as nx
from collections import defaultdict
from utils.utils import timeit



global_T = 0
local_T = defaultdict(lambda:0)
G = nx.Graph()


def parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--graph', type=str, required=True,
                    help='The name of the graph (facebook or roads)')
    parser.add_argument('--M', type=str, required=True,
                    help='parameter M of the triest algorithm')
    args = parser.parse_args() 
    return args

def coin_flip(prob: float) -> bool:
    random_number = random.random()
    if random_number < prob :
        return True
    else:
        return False


def sample_edge(graph: nx.Graph, edge: tuple, M: int, t: int):
    if t <= M:
        return True
    else:
        coin = coin_flip(M / t)
        if coin:
            edge_list = list(graph.edges())
            num_edges = len(edge_list)
            e_idx = random.randint(0, num_edges-1)
            node1, node2 = edge_list[e_idx]
            # print "edge to be removed (%s,%s)" % (u1, v1)
            graph.remove_edge(node1, node2)
            update_counters(graph, (node1,node2), "-")
            return (graph, True)
    return False


def update_counters(graph: nx.Graph, edge: tuple, operation: str):
    global global_T
    nodes = list(graph.nodes)
    node1, node2 = edge
    if node1 not in nodes or node2 not in nodes:
        return


    node1_neighbors = nx.all_neighbors(graph, node1)
    node2_neighbors = nx.all_neighbors(graph, node2)

    shared_neigbourhood = list(set(node1_neighbors) & set(node2_neighbors))
    shared_value = len(shared_neigbourhood)
    if shared_value == 0:
        return
    if operation == "+":
        global_T += shared_value
        local_T[node1] +=  shared_value
        local_T[node2] +=  shared_value

        for c in shared_neigbourhood:
            local_T[c] += 1
    if operation == "-":
        global_T -= shared_value

        local_T[node1] -= shared_value
        if local_T[node1] == 0:
            del local_T[node1]

        local_T[node2] -= shared_value
        if local_T[node2] == 0:
            del local_T[node2]

        for c in shared_neigbourhood:
            local_T[c]-= 1
        if local_T[c] == 0:
            del local_T[c]




def estimate_triangles(M, time):
    estimate = (time*(time-1)*(time-2)) / (M*(M-1)*(M-2))
    if estimate < 1:
        estimate =1
    return int(estimate) * global_T

@timeit
def run_triest_base(graphfile, M):
    time = 0 # variable for time simulation
    with open(graphfile, 'r') as file:
        for line in file:
            line = " ".join(line.split())
            node1, node2 = line.split(' ')
            if node1 == node2:
                continue
            if node1 > node2:
                tmp = node1
                node1 = node2
                node2 = tmp
            if G.has_edge(node1, node2):
                continue
            time += 1
            if sample_edge(G, (node1, node2), M, time):
                G.add_edge(node1, node2)
                update_counters(G, (node1, node2), "+")

    print('The M value is: ', M)
    print("Local_Ts: ", local_T)
    print("Global_T: ", global_T)
    global_triangles = int(estimate_triangles(M, time))
    print("Global Triangles (Estimate * Global_T) = ", global_triangles)
    print ("--------------------")
    return  global_triangles


def main():
    args = parse_args()
    cwd = os.getcwd()
    if args.graph == "facebook":
        graphfile = cwd + '/graph_data/facebook/facebook_combined.txt'
    if args.graph == "roads":
        graphfile = cwd + '/graph_data/california_road_network/roadNet-CA.txt'
    if args.graph == "journal":
        graphfile = cwd + '/graph_data/live_journal/soc-LiveJournal1.txt'


    triest_triangles = run_triest_base(graphfile, int(args.M))
    


if __name__ == '__main__':
    main()