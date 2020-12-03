from __future__ import print_function
from collections import deque
from ortools.linear_solver import pywraplp
from math import sqrt, inf
from time import time
from copy import deepcopy
# import igraph


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
    melhor_distancia = dist_rota(melhor_rota, distancias)
    print(f"Melhor distância antes: {melhor_distancia}")
    while melhorou:
        melhorou = False
        for i in range(1, num_vertices - 1):
            for k in range(i+1, num_vertices):
                nova_rota = troca_two_opt(melhor_rota, i, k)
                nova_distancia = dist_rota(nova_rota, distancias)

                if nova_distancia < melhor_distancia:
                    melhorou = True
                    melhor_rota = nova_rota
                    melhor_distancia = nova_distancia
                    break
                else:
                    melhorou = False
            if melhorou:
                break
    print(f"Melhor distância depois: {melhor_distancia}")            
    return melhor_rota


def dist_rota(rota, distancias):
    """
    Dada uma rota, calcula e retorna a sua distância.
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


def resolve_tsp(coords):
    """
    Resolve o Problema do Caixeiro-Viajante.
    """

    # para plotar o grafo final:
    # g = igraph.Graph()
    # g.add_vertices(len(coords))

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
    timeout = t_inicio + 60*60  # define timeout de 30 minutos (em segundos)
    solver.set_time_limit(max(int((timeout - time())*1000), 0))
    print("Resolvendo...")
    solver.Solve()
    print("Resolveu...")
    solver.set_time_limit(max(int((timeout - time())*1000), 0))

    # obtém a solução parcial na forma de matriz
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
        # solver.SetHint(variables, values)
        print("Resolvendo...")
        solver.Solve()  # resolve novamente
        print("Resolveu...")
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
        # se a sol_parcial não tem nenhum subciclo, ela é a correta!
        subciclos = acha_subciclos(sol_parcial)

    t_final = time()
    custo_total = 0
    print("-->SOLUÇÃO FINAL")
    print("Solução encontrada:")
    for i in range(num_galaxias):
        for j in range(i + 1, num_galaxias):
            if y[i][j].solution_value():
                print(f"{i} -- {j} -> custo: {distancias[i][j]}")
                custo_total += distancias[i][j]
                # g.add_edge(i, j)
    print(f"Custo total: {round(solver.Objective().Value())}")
    print(f"Tempo decorrido: {t_final - t_inicio} segundos")
    # igraph.plot(g, vertex_label=list(range(num_galaxias)), layout=coords)


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
    resolve_tsp(coords)


if __name__ == '__main__':
    main()
