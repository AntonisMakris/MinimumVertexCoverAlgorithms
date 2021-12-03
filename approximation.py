import timeit
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

# Approximation: https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf

# Graphs
graphBinomial = nx.generators.classic.binomial_tree(4)
graphbalanced = nx.generators.classic.balanced_tree(4, 2)
graphStar = nx.star_graph(10)
graph_barabasi_albert = nx.barabasi_albert_graph(20, 10)
graph_erdos_renyi = nx.erdos_renyi_graph(20, 0.7, seed=None, directed=False)
graph_newman_watts_strogatz = nx.newman_watts_strogatz_graph(10, 7, 0.7, seed=None)

print("Vertices:", len(graph_newman_watts_strogatz.nodes), "Edges:", len(graph_newman_watts_strogatz.edges))
MVC_algorithm = nx.to_dict_of_dicts(graph_newman_watts_strogatz)
graph_name_used_for_plot = graph_newman_watts_strogatz


# vertex_cover_approx
# Generates an approximately optimal vertex cover for a given graph using the APPROX-VERTEX-COVER algorithm
# found in (Cormen)
def vertex_cover_approx(graph, size_, res):
    # generate all edges present in graph
    edges = generate_edges(graph)
    s = 0
    cover_ = []
    for edge in edges:
        if edge[0] not in cover_ and edge[1] not in cover_:
            cover_.append(edge[0])
            cover_.append(edge[1])
            s += 2
    size_.append(s)
    res.append(cover_)

# Generates all subsets of size k for the set given
# The subsets are generated in increasing size
def gen_subsets(set_, k):
    curr_subset = []
    res = []
    generate_subsets(set_, curr_subset, res, k, 0)
    return res

def generate_subsets(set_, curr_subset, subsets_, k, next_index):
    if len(curr_subset) == int(k):
        subsets_.append(curr_subset)
        return
    if next_index + 1 <= len(set_):
        curr_subset_exclude = curr_subset.copy()
        curr_subset.append(set_[next_index])
        generate_subsets(set_, curr_subset, subsets_, k, next_index+1)
        generate_subsets(set_, curr_subset_exclude, subsets_, k, next_index+1)

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            if (node,neighbour) and (neighbour, node) not in edges:
                edges.append((node,neighbour))
    return edges

def plot_graph(graph, name):
    g = nx.Graph()
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    nx.draw_networkx(g, pos=nx.circular_layout(g))
    plt.show()


graphConnected_data_Approx = ['Approximation']

size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(MVC_algorithm, size, cover_approx)', number=1, globals=globals())
ratio = size[0]/6
graphConnected_data_Approx.append("{0:.3f}".format(time*1000))
graphConnected_data_Approx.append("{0:.3f}".format(ratio))
graphConnected_data_Approx.append(cover_approx[0])
print (graphConnected_data_Approx)


plot_graph(nx.to_dict_of_dicts(graph_name_used_for_plot), "plots/Graph")
