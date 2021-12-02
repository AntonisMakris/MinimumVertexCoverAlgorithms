import timeit
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from heap import build_heap, get_degrees, get_heap
import sys


# https://github.com/danielslz/minimum-vertex-cover

# def minimum_vertex_cover_greedy(graph):
#     mvc = set()
#
#     edges = set(graph.edges)
#     heap, degrees = build_heap(graph)
#
#     while len(edges) > 0:
#         # remove node with max degree
#         _, node_index = heap.pop()
#         adj = set(graph.edges([node_index]))
#         for u, v in adj:
#             # remove edge from list
#             edges.discard((u, v))
#             edges.discard((v, u))
#
#             # update neighbors
#             if heap.contains(v):
#                 new_degree = degrees[v] - 1
#                 # update index
#                 degrees[v] = new_degree
#                 # update heap
#                 heap.update(v, -1 * new_degree)
#
#         # add node in mvc
#         mvc.add(node_index)
#
#     return mvc




def remove_edges_and_update_degrees(edges_to_remove, edges, degrees, visited):
    for u, v in edges_to_remove:
        # remove edge from list
        edges.discard((u, v))
        edges.discard((v, u))
        # update degree
        degrees[v] -= 1
        if degrees[v] == 0:
            visited[v] = True


def minimum_vertex_cover_hybrid_greedy(graph):
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

    return mvc


def plot_graph(graph, name):
    g = nx.Graph()
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    nx.draw_networkx(g, pos=nx.circular_layout(g))
    plt.show()


graphBinomial = nx.generators.classic.binomial_tree(4)
#minimum_vertex_cover_hybrid_greedy(graphBinomial)


MVC_algorithm = nx.to_dict_of_dicts(graphBinomial)
graph_name_used_for_plot = graphBinomial


labels = ['Graph', 'Algorithm', 'Running Time (ms)', 'Approximation Ratio', 'Cover']
table_data = []
graphConnected_data_b = ['Hybrid_greedy']


coverConnected = []
time = timeit.timeit('minimum_vertex_cover_hybrid_greedy(graphBinomial)', number=1, globals=globals())
print (time)
graphConnected_data_b.append("{0:.3f}".format(time*1000))
#graphConnected_data_b.append(1.0)
#graphConnected_data_b.append(coverConnected[0])
print (graphConnected_data_b)


table_data.append(graphConnected_data_b)





#minimum_vertex_cover_hybrid_greedy(graphBinomial)
plot_graph(nx.to_dict_of_dicts(graph_name_used_for_plot), "plots/Graph")



