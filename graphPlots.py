import networkx as nx
import matplotlib.pyplot as plt


def barabasi():
    n = 50
    m = 5
    G_barabasi = nx.barabasi_albert_graph(n,m)
    plt.figure(figsize=(12,8))
    nx.draw(G_barabasi, node_size=4)
    plt.show()

def binomial_tree_custom(n):
    G = nx.empty_graph(1)

    N = 1
    for i in range(n):
        # Use G.edges() to ensure 2-tuples. G.edges is 3-tuple for MultiGraph
        edges = [(u + N, v + N) for (u, v) in G.edges()]
        G.add_edges_from(edges)
        G.add_edge(0, N)
        N *= 2
    return G

def binomial():
    binomial_tree = binomial_tree_custom(6)
    plt.figure(figsize=(12, 8))

    nx.draw(binomial_tree, node_size=4)
    plt.show()


def erdos_renyi():
    graph_erdos_renyi = nx.erdos_renyi_graph(50, 0.2, seed=None, directed=False)
    plt.figure(figsize=(12, 8))

    nx.draw(graph_erdos_renyi, node_size=8)
    plt.show()

def watts_strogatz():
    watts_strogatz = nx.newman_watts_strogatz_graph(20, 4, 1, seed=None)
    plt.figure(figsize=(12, 8))

    nx.draw(watts_strogatz, node_size=8)
    plt.show()

def star():
    graphStar = nx.star_graph(10)
    plt.figure(figsize=(12, 8))

    nx.draw(graphStar, node_size=19)
    plt.show()

def balanced():
    balanced_tree = nx.balanced_tree(4, 3, create_using=None)
    plt.figure(figsize=(12, 8))

    nx.draw(balanced_tree, node_size=4)
    plt.show()

def plot_graph(graph, name):
    g = nx.Graph()
    color_map =[]
    for k, vs in dict(graph).items():
        for v in vs:
            g.add_edge(k, v)
    color_map.append('black')
    plt.axis('off')
    nx.draw_networkx(g, node_size=12, node_color=color_map, with_labels=False)
    plt.show()


#plot_graph(nx.to_dict_of_dicts(nx.star_graph(20)), "plots/Graph")

binomial()
#balanced()
#watts_strogatz()
#star()
#barabasi()
#binomial()
#erdos_renyi()