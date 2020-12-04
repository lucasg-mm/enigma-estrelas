from __future__ import print_function
from collections import deque
from ortools.linear_solver import pywraplp
from math import sqrt, inf
from time import time
import igraph


def acha_subciclos(mat_adj):
    """Dada uma matriz mat_adj, a função abaixo retorna uma lista de sets, cada um contendo os índices
    que representam os vértices que formam um subciclo. Se não houver subciclos, retorna False. A
    matriz mat_adj deve ser uma matriz adjacências de um grafo não ponderado, ou seja, mat_adj[i][j] == 1,
    se existe uma aresta entre os vértices i e j.
    """

    # se marcados[i] == True, então o vértice 1 já foi atribuido a um comp. conexo
    marcados = [False for i in range(len(mat_adj))]
    comp_conexos = []  # lista de sets que contêm os índices que formam comp. conexo
    fila = deque()  # fila utilizada no busca em largura

    for i in range(len(marcados)):
        # para todo vértice ainda não atribuído a um comp. conexo, faz uma busca em largura (início = marcados[i])
        # para registrar os vértices que fazem parte do mesmo componente conexo que marcados[j]
        if not marcados[i]:
            # set que deverá armazenar os vértices que fazem parte do mesmo componente conexo que marcados[i]
            aux = set()
            fila.append(i)
            marcados[i] = True
            aux.add(i)

            while fila:  # enquanto a fila não estiver vazia, busca em largura...
                atual = fila.popleft()
                for j in range(len(mat_adj)):
                    if mat_adj[atual][j] and not marcados[j]:
                        marcados[j] = True
                        fila.append(j)
                        # o vértice j faz parte do mesmo componente conexo de marcados[i]
                        aux.add(j)
            # if 0 not in aux:
            #     comp_conexos.append(aux)  # adiciona mais um set para a lista
            if len(aux) >= 3 and len(aux) <= len(mat_adj) - 1:
                comp_conexos.append(aux)  # adiciona mais um set para a lista
    return comp_conexos


def elimina_subciclos(mat_adj, custos, num_vertices):
    """
    Dada uma configuração do grafo com subciclos representada por mat_adj, elimina os
    subciclos sem aumentar muito o custo. 
    """

    rota = []  # rota (sem subciclos) que deve ser retornada no final
    proximo = 0
    for _ in range(num_vertices+1):  # percorre todos os nós
        rota.append(proximo)
        atual = proximo
        # recupera os nós adjacentes no grafo representado por mat_adj (apenas os que ainda não fazem parte da rota)
        proximos_possiveis = [i for i in range(
            num_vertices) if mat_adj[atual][i] == 1 and i not in rota]
        if proximos_possiveis:  # se proximos_possiveis não for vazio...
            # preserva a aresta de menor peso e elimina a outra (se existir outra)
            if len(proximos_possiveis) == 1 or custos[atual][proximos_possiveis[0]] < custos[atual][proximos_possiveis[1]]:
                # obtém o índice do próximo nó a ser visitado
                proximo = proximos_possiveis[0]
            else:
                # obtém o índice do próximo nó a ser visitado
                proximo = proximos_possiveis[1]
        else:  # se proximos_possiveis estiver vazio...
            # conecta o nó com a aresta de menor peso que o liga com um dos que ainda não fazem parte da rota (como a heurística dos nearest neighboors)
            proximos_possiveis = [
                custo if custos[atual].index(custo) not in rota else inf for custo in custos[atual]]
            # obtém o índice do próximo nó a ser visitado
            proximo = proximos_possiveis.index(min(proximos_possiveis))
    return rota


def nearest_neighboors(custos, num_vertices):
    """
    Implementação da heurística dos vizinhos mais próximos para obter uma rota que é uma solução
    factível para o problema de otimização.
    """

    rota = []
    proximo = 0
    for _ in range(num_vertices+1):
        rota.append(proximo)  # adiciona mais um elemento à rota
        atual = proximo
        # obtém os custos dos próximos nodos possíveis (os ainda não visitados)
        proximos_possiveis = [
            custo if custos[atual].index(custo) not in rota else inf for custo in custos[atual]]
        # obtém o índice do próximo nó a ser visitado
        proximo = proximos_possiveis.index(min(proximos_possiveis))

    return rota


def troca_two_opt(rota, i, k):
    """
    Executa a troca durante a execução do 2-opt
    """
    nova_rota = rota[:i]
    nova_rota.extend(rota[i:k+1][::-1])
    nova_rota.extend(rota[k+1:])
    return nova_rota


def two_opt(melhor_rota, distancias, num_vertices):
    """
    Implementação da heurística 2-opt.
    """

    melhorou = True
    melhor_distancia_rota = dist_rota(melhor_rota, distancias)
    # imprime a distância do caminho todo para ter uma ideia
    print(
        f"Custo da solução inicial antes da heurística 2-opt: {melhor_distancia_rota}")
    while melhorou:  # enquanto o custo estiver melhorando...
        melhorou = False
        for i in range(1, num_vertices - 1):
            for k in range(i+1, num_vertices):
                melhor_custo_par_aresta = custo_par_aresta(
                    distancias, [melhor_rota[i-1], melhor_rota[i]], [melhor_rota[k], melhor_rota[k+1]])
                novo_custo_par_aresta = custo_par_aresta(
                    distancias, [melhor_rota[i-1], melhor_rota[k]], [melhor_rota[i], melhor_rota[k+1]])

                # se o custo da troca do par de arestas for menor que o da configuração original do par...
                if novo_custo_par_aresta < melhor_custo_par_aresta:
                    melhorou = True
                    # define a melhor rota como a que possui as arestas trocadas
                    melhor_rota = troca_two_opt(melhor_rota, i, k)
                    break
                else:
                    melhorou = False
            if melhorou:
                break
    melhor_distancia_rota = dist_rota(melhor_rota, distancias)
    # imprime a distância do caminho todo para ter uma ideia da melhora
    print(
        f"Custo da solução inicial depois da heurística 2-opt: {melhor_distancia_rota}")
    return melhor_rota


def custo_par_aresta(distancias, aresta1, aresta2):
    """
    Retorna o custo de um par de arestas.
    """
    return distancias[aresta1[0]][aresta1[1]] + distancias[aresta2[0]][aresta2[1]]


def dist_rota(rota, distancias):
    """
    Dada uma rota, retorna a sua distância.
    """
    dist = 0
    for i in range(len(rota) - 1):
        dist += distancias[rota[i]][rota[i+1]]
    return dist


def define_solucao_inicial(solver, rota_inicial, num_vertices, y):
    """
    Define uma solução inicial para o modelo a partir de uma dada rota 
    na forma [0, k, ..., 0].
    """
    variaveis = []
    valores = []
    rota_inicial = [(rota_inicial[i], rota_inicial[i+1])
                    for i in range(len(rota_inicial) - 1)]
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if (i, j) in rota_inicial or (j, i) in rota_inicial:
                valores.append(1.0)
            else:
                valores.append(0.0)
            variaveis.append(y[i][j])

    solver.SetHint(variaveis, valores)


def get_mat_adj(y, num_galaxias):
    """
    A partir de uma solução y, retorna a matriz de adjacências correspondente.
    """
    sol_parcial = []
    for i in range(num_galaxias):
        sol_parcial.append([])
        for j in range(num_galaxias):
            if j >= i + 1:
                sol_parcial[i].append(y[i][j].solution_value())
            elif j == i:
                sol_parcial[i].append(0.0)
            else:
                sol_parcial[i].append(y[j][i].solution_value())
    return sol_parcial


def resolve_tsp(coords, desenhar=False, lim_minutos=30):
    """
    Resolve o Problema do Caixeiro-Viajante.
    """

    # para plotar o grafo final:
    g = igraph.Graph()
    g.add_vertices(len(coords))

    solver = pywraplp.Solver.CreateSolver('SCIP')  # define o solver
    num_galaxias = len(coords)  # armazena o número de galáxias

    # -> definindo as variáveis da função objetivo
    y = []  # variáveis da função objetivo (em forma de matriz)
    for i in range(num_galaxias):
        y.append([])
        for j in range(num_galaxias):
            if j >= i + 1:
                y[i].append(solver.IntVar(0, 1, f"y[{i}][{j}]"))
            else:
                y[i].append(0.0)
    print(f"Número de variáveis = {solver.NumVariables()}")

    # -> definindo as restrições
    # garante que apenas uma aresta saia de um vértice
    for vertice in range(num_galaxias):
        arestas = [y[vertice][j] for j in range(vertice + 1, num_galaxias)]
        arestas.extend((y[i][vertice] for i in range(0, vertice)))
        solver.Add(sum(arestas) == 2)

    print(f"Número de restrições (inicialmente) = {solver.NumConstraints()}")

    # -> definindo a função objetivo
    distancias = []
    parcelas_obj = []
    for i in range(num_galaxias):
        distancias.append([])
        for j in range(num_galaxias):
            if j >= i + 1:
                distancias[i].append(
                    int(round(dist_euclid(coords[i], coords[j]))))
                parcelas_obj.append(y[i][j] * distancias[i][j])
            elif j < i:
                distancias[i].append(
                    int(round(dist_euclid(coords[i], coords[j]))))
            else:
                distancias[i].append(0.0)

    # obtém uma rota inicial usando a heurística dos vizinhos mais próximos
    rota_inicial = nearest_neighboors(distancias, num_galaxias)
    # melhora a rota inicial usando a heurística 2-opt
    rota_inicial = two_opt(rota_inicial, distancias, num_galaxias)
    # da rota obtida, definimos uma solução inicial
    define_solucao_inicial(solver, rota_inicial, num_galaxias, y)

    solver.Minimize(sum(parcelas_obj))  # obtém a primeira solução

    # -> resolve
    t_inicio = time()
    timeout = t_inicio + 60 * lim_minutos  # define timeout
    solver.set_time_limit(max(int((timeout - time())*1000), 0))
    print("Resolvendo problema relaxado (sem restrições de subciclos ilegais)...")
    solver.Solve()

    if time() < timeout:  # só tenta continuar se o tempo ainda não acabou
        print("Problema resolvido!")
        custo_parcial = round(solver.Objective().Value())
        print(f"Custo total: {custo_parcial}")
        solver.set_time_limit(max(int((timeout - time())*1000), 0))

        # obtém a solução parcial na forma de matriz de adjacências (necessária para achar subciclos)
        sol_parcial = get_mat_adj(y, num_galaxias)
        # se a sol_parcial não tem nenhum subciclo, ela é a correta!
        subciclos = acha_subciclos(sol_parcial)

    while subciclos and time() < timeout:
        # se a solução parcial possui subciclos, adiciona restrições para detectar
        # os subciclos achados, e resolve o problema novamente, achando outra solução parcial
        for subciclo in subciclos:
            aux_list = []
            for i in subciclo:
                for j in subciclo:
                    if j >= i + 1:
                        aux_list.append(y[i][j])
            solver.Add(sum(aux_list) <= len(subciclo) - 1)

        solver.set_time_limit(max(int((timeout - time())*1000), 0))
        print("Resolvendo problema com mais algumas restrições de subciclos ilegais")
        solver.Solve()  # resolve novamente

        if time() < timeout:  # só tenta continuar se o tempo ainda não acabou
            print("Problema resolvido!")
            custo_parcial = round(solver.Objective().Value())
            print(f"Custo total: {custo_parcial}")
            # obtém a solução parcial na forma de matriz de adjacências (necessária para achar subciclos)
            sol_parcial = get_mat_adj(y, num_galaxias)
            # se a sol_parcial não tem nenhum subciclo, ela é a correta!
            subciclos = acha_subciclos(sol_parcial)

    if time() >= timeout:
        print("-----------------")
        print(f"TIMEOUT! Não foi possível gerar uma solução ótima em {lim_minutos} minutos.")
        print("Eliminando os subciclos da última solução encontrada...")
        rota = elimina_subciclos(sol_parcial, distancias, num_galaxias)
        print("Melhorando a solução com a heurística 2-opt...")
        rota = two_opt(rota, distancias, num_galaxias)

        t_final = time()
        custo_total = 0        
        print("-----------------")
        print("-->SOLUÇÃO FINAL (A MELHOR ENCONTRADA)")
        rota = [(rota[i], rota[i+1])
                        for i in range(len(rota) - 1)]
        for i in range(num_galaxias):
            for j in range(i + 1, num_galaxias):
                if (i, j) in rota or (j, i) in rota:
                    print(f"{i} -- {j} -> custo: {distancias[i][j]}")
                    g.add_edge(i, j)
                    custo_total += distancias[i][j]
        print(f"Custo total: {custo_total}")
        print(f"GAP:")
        print(f"Número de nós explorados:")
        print(f"Tempo decorrido: {round(t_final - t_inicio, 5)} segundos")             
    else:
        t_final = time()
        print("-----------------")
        print("-->SOLUÇÃO FINAL (ÓTIMA)")
        print("Solução encontrada:")
        for i in range(num_galaxias):
            for j in range(i + 1, num_galaxias):
                if y[i][j].solution_value():
                    print(f"{i} -- {j} -> custo: {distancias[i][j]}")
                    g.add_edge(i, j)
        print(f"Custo total: {round(solver.Objective().Value())}")
        print(f"Tempo decorrido: {round(t_final - t_inicio, 5)} segundos")
    if desenhar:    
        igraph.plot(g, layout=coords, vertex_size=5)


def dist_euclid(a, b):
    """
    Calcula a distância euclidiana 2d entre dois pontos representados por tuplas.
    """
    return sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))


def get_input():
    """
    Pega input e retorna numa lista de tuplas.
    """
    num_vertices = int(input())
    coords = []  # lista que contém cada coordenada em uma tupla

    for _ in range(num_vertices):
        coord = input()  # pega input como string em uma linha só
        coord = coord.split()  # separa as duas componentes
        # converte cada componenente para float
        coord = [float(comp) for comp in coord]
        coord = tuple(coord)  # transforma a tupla
        coords.append(coord)  # coloca na lista maior

    return coords


def main():
    coords = get_input()
    resolve_tsp(coords, desenhar=True, lim_minutos=30)


if __name__ == '__main__':
    main()
