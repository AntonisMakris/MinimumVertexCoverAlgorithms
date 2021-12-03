import timeit
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

# Graphs: https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.erdos_renyi_graph.html

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

def vertex_cover_degrees(graph, res):
    edges = generate_edges(graph)
    degrees = count_degrees(edges, list(dict(graph).keys()))
    degrees_sorted = sorted(degrees.items(), key=itemgetter(1), reverse=True)
    cover_ = []
    for v in degrees_sorted:
        cover_.append(v[0])
        if verify_vertex_cover(cover_, edges):
            res.append(cover_)
            return

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

# verifies that cover is indeed a vertex cover
# does not check if cover only has vertices from graph
def verify_vertex_cover(cover, edges):
    # check that atleast one vertice from each edge appears in cover
    for edge in edges:
        in_cover = False;
        for vertex in cover:
            if edge[0] == vertex or edge[1] == vertex:
                    in_cover = True;
        # stop processing as soon as one edge found not in cover
        if in_cover == False:
            return False
    # return true if all edges have atleast one endpoint in cover
    return True

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            if (node,neighbour) and (neighbour, node) not in edges:
                edges.append((node,neighbour))
    return edges

def count_degrees(edges, vertices):
    degrees = {}
    for v in vertices:
        degrees[v] = 0
    for edge in edges:
        degrees[edge[0]] = degrees[edge[0]] + 1
        degrees[edge[1]] = degrees[edge[1]] + 1
    return degrees

def plot_graph(graph, name):
    g = nx.Graph()
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    nx.draw_networkx(g, pos=nx.circular_layout(g))
    plt.show()

graphConnected_data_DegreeH= ['Degree Heuristic']

cover_degree = []
time = timeit.timeit('vertex_cover_degrees(MVC_algorithm, cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/6
graphConnected_data_DegreeH.append("{0:.3f}".format(time*1000))
graphConnected_data_DegreeH.append("{0:.3f}".format(ratio))
graphConnected_data_DegreeH.append(cover_degree[0])
print(graphConnected_data_DegreeH)

plot_graph(nx.to_dict_of_dicts(graph_name_used_for_plot), "plots/Graph")
