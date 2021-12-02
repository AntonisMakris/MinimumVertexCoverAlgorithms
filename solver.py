import timeit
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import pickle



graphConnected_Binomial = nx.generators.classic.binomial_tree(4)
#graphConnected_Star = nx.star_graph(10)

#graphConnected_Star = nx.barabasi_albert_graph(10, 5)
# G2 = nx.generators.classic.balanced_tree(8, 2)

#print (nx.to_dict_of_dicts(graphConnected_Binomial))

# Functions #################################################

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

# vertex_cover_brute checks all possible sets of vertices of size k for a valid cover
def vertex_cover_brute(graph, res):
    vertices = list(dict(graph).keys())
    k = len(vertices)
    # generate all edges present in graph
    edges = generate_edges(graph)
    for i in range(1, k):
        # generate all subset of size i from set vertices
        subsets_ = gen_subsets(vertices, i)
        for s in subsets_:
            # check if subset s is a cover for graph
            if verify_vertex_cover(s, edges) == True:
                # since subsets are generated in  increasing size, the first
                # subset that is cover can be returned as the minimal one
                res.append(s)
                return
    # no cover was found so return set of all edges as minimal cover
    #res.append(vertices)

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


# gen_subsets(set,k)
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


# Experiments ####################################################


col_labels = ['Graph', 'Algorithm', 'Running Time (ms)', 'Approximation Ratio', 'Cover']
table_data = []


graphConnected_data_b = ['GraphConnected', 'Brute Force']
graphConnected_data_a = ['GraphConnected', 'Approximation']
graphConnected_data_d = ['GraphConnected', 'Degree Heuristic']

# graph351_data_b = ['Graph351', 'Brute Force']
# graph351_data_a = ['Graph351', 'Approximation']
# graph351_data_d = ['Graph351', 'Degree Heuristic']


coverConnected = []
time = timeit.timeit('vertex_cover_brute(nx.to_dict_of_dicts(graphConnected_Binomial), coverConnected)', number=1, globals=globals())
print (time)
graphConnected_data_b.append("{0:.3f}".format(time*1000))
graphConnected_data_b.append(1.0)
graphConnected_data_b.append(coverConnected[0])
print (graphConnected_data_b)

time = 0.0
size = []
cover_approx = []
time = timeit.timeit('vertex_cover_approx(nx.to_dict_of_dicts(graphConnected_Binomial), size, cover_approx)', number=1, globals=globals())
ratio = size[0]/6
graphConnected_data_a.append("{0:.3f}".format(time*1000))
graphConnected_data_a.append("{0:.3f}".format(ratio))
graphConnected_data_a.append(cover_approx[0])
print (graphConnected_data_a)



cover_degree = []
time = timeit.timeit('vertex_cover_degrees(nx.to_dict_of_dicts(graphConnected_Binomial), cover_degree)', number=1, globals=globals())
ratio = len(cover_degree[0])/6
graphConnected_data_d.append("{0:.3f}".format(time*1000))
graphConnected_data_d.append("{0:.3f}".format(ratio))
graphConnected_data_d.append(cover_degree[0])
print(graphConnected_data_d)




##################################
# coverConnected = []
# time = timeit.timeit('vertex_cover_brute(nx.to_dict_of_dicts(graphConnected_Star), coverConnected)', number=1, globals=globals())
# print (time)
# graph351_data_b.append("{0:.3f}".format(time*1000))
# graph351_data_b.append(1.0)
# graph351_data_b.append(coverConnected[0])
# print (graph351_data_b)
#
# time = 0.0
# size = []
# cover_approx = []
# time = timeit.timeit('vertex_cover_approx(nx.to_dict_of_dicts(graphConnected_Star), size, cover_approx)', number=1, globals=globals())
# ratio = size[0]/6
# graph351_data_a.append("{0:.3f}".format(time*1000))
# graph351_data_a.append("{0:.3f}".format(ratio))
# graph351_data_a.append(cover_approx[0])
# print (graph351_data_a)
#
#
#
# cover_degree = []
# time = timeit.timeit('vertex_cover_degrees(nx.to_dict_of_dicts(graphConnected_Star), cover_degree)', number=1, globals=globals())
# ratio = len(cover_degree[0])/6
# graph351_data_d.append("{0:.3f}".format(time*1000))
# graph351_data_d.append("{0:.3f}".format(ratio))
# graph351_data_d.append(cover_degree[0])
# print(graph351_data_d)


##################################












table_data.append(graphConnected_data_b)
table_data.append(graphConnected_data_a)
table_data.append(graphConnected_data_d)

# table_data.append(graph351_data_b)
# table_data.append(graph351_data_a)
# table_data.append(graph351_data_d)


fig = plt.figure(dpi=160)
ax = fig.add_subplot(111)
ax.set_title("Results")

table = ax.table(cellText=table_data,
                  colLabels=col_labels,
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.auto_set_column_width([0,1,2,3,4])
ax.axis('off')
plt.show()


#plot_graph(nx.to_dict_of_dicts(graphConnected_Star), "plots/Graph351")
plot_graph(nx.to_dict_of_dicts(graphConnected_Binomial), "plots/GraphConnected")
# plot_graph(graphBipartite, "plots/GraphBipartite")
# plot_graph(graphBig, "plots/GraphBig")