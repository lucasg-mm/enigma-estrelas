from __future__ import print_function
from collections import deque
from ortools.linear_solver import pywraplp
from math import sqrt

import solution_plotter


def acha_subciclos(mat_adj):
    """
    Dada uma matriz mat_adj, a função abaixo retorna uma lista de sets, cada um contendo os índices
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
            if 0 not in aux:
                comp_conexos.append(aux)  # adiciona mais um set para a lista
    return comp_conexos


def resolve_tsp(coords):
    """
    Resolve o Problema do Caixeiro-Viajante.
    """

    solver = pywraplp.Solver.CreateSolver('SCIP')  # define o solver
    num_galaxias = len(coords)  # armazena o número de galáxias

    # -> definindo as variáveis da função objetivo
    y = []  # variáveis da função objetivo (em forma de matriz)
    for i in range(num_galaxias):
        y.append([])
        for j in range(num_galaxias):
            y[i].append(solver.IntVar(0, 1, f"y[{i}][{j}]"))
    print(f"Número de variáveis = {solver.NumVariables()}")

    # -> definindo as restrições
    # garante que apenas uma aresta saia de um vértice
    for i in range(num_galaxias):
        solver.Add(sum(y[i][j] for j in range(num_galaxias)) == 1)

    # garante que apenas uma aresta chegue em um vértice
    for j in range(num_galaxias):
        solver.Add(sum(y[i][j] for i in range(num_galaxias)) == 1)

    print(f"Número de restrições (inicialmente) = {solver.NumConstraints()}")

    # -> definindo a função objetivo
    distancias = []
    parcelas_obj = []
    for i in range(num_galaxias):
        distancias.append([])
        for j in range(num_galaxias):
            distancias[i].append(int(round(dist_euclid(coords[i], coords[j]))))
            parcelas_obj.append(y[i][j] * distancias[i][j])
    solver.Minimize(sum(parcelas_obj))

    # -> resolve
    solver.Solve()

    # obtém a solução parcial na forma de matriz
    sol_parcial = [[y[i][j].solution_value() for i in range(
        num_galaxias)] for j in range(num_galaxias)]

    # se a sol_parcial não tem nenhum subciclo, ela é a correta!
    subciclos = acha_subciclos(sol_parcial)

    while subciclos:
        # se a solução parcial possui subciclos, adiciona restrições para detectar
        # os subciclos achados, e resolve o problema novamente, achando outra solução parcial
        for subciclo in subciclos:
            aux_list = []
            for i in subciclo:
                for j in subciclo:
                    aux_list.append(y[i][j])
            solver.Add(sum(aux_list) <= len(subciclo) - 1)

        solver.Solve()  # resolve novamente
        sol_parcial = [[y[i][j].solution_value() for i in range(  # obtém outra solução parcial
            num_galaxias)] for j in range(num_galaxias)]
        # se a sol_parcial não tem nenhum subciclo, ela é a correta!
        subciclos = acha_subciclos(sol_parcial)

    solucao = {}
    custo_total = 0
    print("-->SOLUÇÃO FINAL")
    print("Solução encontrada:")
    for i in range(num_galaxias):
        for j in range(num_galaxias):
            if y[i][j].solution_value():
                print(f"De {i} para {j} -> custo: {distancias[i][j]}")
                custo_total += distancias[i][j]
                solucao[(i, j)] = distancias[i][j]
                
    print(f"Custo total: {round(solver.Objective().Value())}")
    
    return solucao


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


def main(plotar_solucao=False):
    coords = get_input()
    solucao = resolve_tsp(coords)

    if plotar_solucao and len(coords) < 100:
        solution_plotter.plot_dir_graph(coords, list(solucao.keys()))



if __name__ == '__main__':
    main(plotar_solucao = True)
