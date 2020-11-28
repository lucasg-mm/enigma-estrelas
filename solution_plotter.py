# Adiciona dependencia de matplotlib e networkx

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx



def plot_dir_graph(nodes, edges, weigths=None):
    """
        nodes:   dicionario com os nodos do grafo com sua respectiva posicao x,y
        edges:   uma lista de tuplas cada uma contendo os nodos de origem e destino
        weights: o comprimento de cada aresta
    """

    # criando grafo orientado
    G = nx.DiGraph()
    # posicionando nodos no grafo 
    G.add_nodes_from(list(nodes.keys()))
    nx.set_node_attributes(G, 'pos', nodes)
    """G.add_edges_from(
        [('1', '2'), ('2', '3'), ('5', '1'), ('3', '4'), ("4", "5")])
    """
    if weigths == None:
        weigths = list(range(len(edges)))

    # ligando os nodos
    for i in range(len(edges)):
        G.add_edge(str(edges[i][0]), str(edges[i][1]), weigth=weigths[i])

    # definindo cores unicas pra cada nodo
    val_map = {}
    for i in range(len(nodes)):
        val_map[str(i)] = i/2
    
    values = [val_map.get(node, 0.25) for node in G.nodes()]

    
    pos = nx.layout.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                        node_color = values, node_size = 250)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle="->", arrowsize=20, arrows=True)

    plt.show()    



"""edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=node_sizes,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=plt.cm.Blues,
    width=2,
)"""