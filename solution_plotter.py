# Adiciona dependencia python-igraph
import igraph

def plot_dir_graph(coords, edges):
    """
        coords:  dicionario com os nodos do grafo com sua respectiva posicao x,y
        edges:   uma lista de tuplas cada uma contendo os nodos de origem e destino
    """

    # para plotar o grafo final:
    G = igraph.Graph(directed=True)
    G.add_vertices(len(coords))
    
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    G.vs["color"] = [(((i*5)%100)/100, (2*i**3.2 % 100)/100, ((0.5*i**1.5)%100)/100) for i in range(len(coords))]
 
    igraph.plot(G, vertex_label=list(range(len(coords))), layout=coords) 