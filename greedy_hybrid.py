import timeit
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from networkx.algorithms import approximation
from heapq import heapify, heappop
import sys

class Heap():
    # data format: [node_degree, node_index]
    heap = []
    hash = dict()

    def init(self, initial):
        self.heap = initial
        for value, index in initial:
            self.hash[index] = value
        self.rebuild()

    def rebuild(self):
        heapify(self.heap)

    def pop(self):
        return heappop(self.heap)

    def contains(self, index):
        return index in self.hash

    def update(self, index, value):
        self.hash[index] = value
        for i, e in enumerate(self.heap):
            if e[1] == index:
                self.heap[i] = [value, index]
                break
        self.rebuild()

    def get(self, index):
        return self.hash.get(index)

    def size(self):
        return len(self.heap)


def build_heap(graph):
    heap = Heap()
    degree_index = {}

    data = []  # data format: [node_degree, node_index]
    for node in graph.nodes:
        node_index = node
        degree = graph.degree[node_index]
        degree_index[node_index] = degree
        # multiply to -1 for desc order
        data.append([-1 * degree, node_index])
    heap.init(data)

    return heap, degree_index


def get_degrees(graph):
    degrees = {}

    for node in graph.nodes:
        node_index = node
        degree = graph.degree[node_index]
        degrees[node_index] = degree

    return degrees


def get_heap(nodes, degrees, visited):
    heap = Heap()
    heap_data = []  # data format: [node_degree, node_index]
    for node in nodes:
        if not visited[node]:
            degree = degrees[node]
            # multiply to -1 for desc order
            heap_data.append([-1 * degree, node])
    heap.init(heap_data)

    return heap



def minimum_vertex_cover_greedy(graph, coverset):
    mvc = set()

    edges = set(graph.edges)
    heap, degrees = build_heap(graph)

    while len(edges) > 0:
        # remove node with max degree
        _, node_index = heap.pop()
        adj = set(graph.edges([node_index]))
        for u, v in adj:
            # remove edge from list
            edges.discard((u, v))
            edges.discard((v, u))

            # update neighbors
            if heap.contains(v):
                new_degree = degrees[v] - 1
                # update index
                degrees[v] = new_degree
                # update heap
                heap.update(v, -1 * new_degree)
        # add node in mvc
        mvc.add(node_index)
        coverset.append(mvc)
    return

def remove_edges_and_update_degrees(edges_to_remove, edges, degrees, visited):
    for u, v in edges_to_remove:
        # remove edge from list
        edges.discard((u, v))
        edges.discard((v, u))
        # update degree
        degrees[v] -= 1
        if degrees[v] == 0:
            visited[v] = True

def minimum_vertex_cover_hybrid_greedy(graph, coverset):
    mvc = set()
    visited = {}

    degrees = get_degrees(graph)
    edges = set(graph.edges)
    nodes = set(graph.nodes)

    # mark node with degree 1 as visited, otherwise not visited
    for node in nodes:
        # init status
        visited[node] = False
        if degrees[node] == 1:
            # mark node as visited
            visited[node] = True
            # remove edges and update node degrees
            for u, v in graph.edges([node]):
                if degrees[v] > 1:
                    # remove edge from list
                    edges.discard((u, v))
                    edges.discard((v, u))
                    # update degree
                    degrees[v] -= 1
                    if degrees[v] == 0:
                        visited[v] = True

    # build heap with nodes not visited
    heap = get_heap(nodes, degrees, visited)

    # heap update factor
    heap_update_factor = sys.maxsize
    total_nodes = heap.size()
    ratio = total_nodes / len(edges)
    if len(nodes) > 100:
        heap_update_factor = int(total_nodes * ratio)

    # greedy
    count = 0
    while(len(edges) > 0):
        count += 1
        # verify if must update heap
        if count > heap_update_factor:
            count = 0
            # build heap with nodes not visited
            heap = get_heap(nodes, degrees, visited)

        try:
            _, node_index = heap.pop()
            if not visited[node_index]:
                visited[node_index] = True
                mvc.add(node_index)
                # remove edges
                remove_edges_and_update_degrees(graph.edges([node_index]), edges, degrees, visited)
        except IndexError:
            # no more nodes
            break
    coverset.append(mvc)
    return mvc


def plot_graph(graph, name):
    g = nx.Graph()
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    nx.draw_networkx(g, pos=nx.circular_layout(g))
    plt.show()


graphBinomial = nx.generators.classic.binomial_tree(4)
graphbalanced = nx.generators.classic.balanced_tree(4, 2)
graphStar = nx.star_graph(10)
graph_barabasi_albert = nx.barabasi_albert_graph(50, 3)
graph_erdos_renyi = nx.erdos_renyi_graph(10, 0.9, seed=None, directed=False)
graph_newman_watts_strogatz = nx.newman_watts_strogatz_graph(10, 7, 0.7, seed=None)

print("Vertices:", len(graph_barabasi_albert.nodes), "Edges:", len(graph_barabasi_albert.edges))

graph_name_used_for_plot = graph_barabasi_albert
G = graph_barabasi_albert


labels = ['Graph', 'Algorithm', 'Running Time (ms)', 'Approximation Ratio', 'Cover']
table_data = []
graphConnected_data_b = ['Hybrid_greedy']

coverConnected = []
time = timeit.timeit('minimum_vertex_cover_hybrid_greedy(G, coverConnected)', number=1, globals=globals())
print (time)
graphConnected_data_b.append("{0:.3f}".format(time*1000))
print ("approximation ratio", len(coverConnected[0])/len(approximation.min_weighted_vertex_cover(G)))
graphConnected_data_b.append(coverConnected[0])
print (graphConnected_data_b)

#minimum_vertex_cover_hybrid_greedy(graphBinomial)
plot_graph(nx.to_dict_of_dicts(graph_name_used_for_plot), "plots/Graph")



