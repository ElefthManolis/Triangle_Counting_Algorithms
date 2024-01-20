import time
from functools import wraps
import networkx as nx



def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


@timeit
def create_graph(graph_path: str, sampling_factor: int = None):
    G = nx.Graph() # create an empty graph with networkx library
    # Read the file and add edges to the graph
    
    with open(graph_path, 'r') as file:
        row = 0
        for line in file:
            if (sampling_factor is not None) and (row % sampling_factor == 0):
                row += 1
                continue
            # Remove unnecessary spaces between the numbers
            line = " ".join(line.split())
            # Split the line into two numbers
            node1, node2 = line.split(' ')
            if node1 == node2:
                continue
            if node1 > node2:
                tmp = node1
                node1 = node2
                node2 = tmp
            if G.has_edge(node1, node2):
                continue
            # Add an edge between the two nodes
            G.add_edge(node1, node2)
            row += 1
    return G