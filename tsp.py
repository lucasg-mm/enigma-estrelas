# LUCAS G. M. MIRANDA - 10265892 - lucasgmm@usp.br
# MARCELA TIEMI SHINZATO - 10276953 - marcelats@usp.br
# SÉRGIO RICARDO G. B. FILHO - 10408386 - sergiobarbosa@usp.br
# TIAGO LASCALA AUDE - 8936742 - tiago.aude@usp.br


# Resolve uma instância do problema do caixeiro viajante,
# usando o CP-SAT solver do Google OR-Tools.

from collections import deque
from ortools.sat.python import cp_model
from math import sqrt


# Dada uma matriz mat_adj, a função abaixo retorna uma lista de sets, cada um contendo os índices
# que representam os vértices que formam um subciclo. Se não houver subciclos, retorna False. A
# matriz mat_adj deve ser uma matriz adjacências de um grafo não ponderado, ou seja, mat_adj[i][j] == True,
# se existe uma aresta entre os vértices i e j.


def acha_subciclos(mat_adj):
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

# Resolve o Problema do Caixeiro-Viajante


def resolve_tsp(distancias):
    # -- declara o modelo CP-SAT
    model = cp_model.CpModel()

    # -- cria as variáveis binárias inteiras x[i][j]
    num_galaxias = len(distancias)
    x = [[model.NewBoolVar(f"x[{i},{j}]") for j in range(
        num_galaxias)] for i in range(num_galaxias)]

    # -- cria as restrições
    # garante que apenas uma aresta saia de um vértice
    for i in range(num_galaxias):
        model.Add(sum(x[i][j] for j in range(num_galaxias)) == 1)

    # garante que apenas uma aresta chegue em um vértice
    for j in range(num_galaxias):
        model.Add(sum(x[i][j] for i in range(num_galaxias)) == 1)

    # -- cria a função objetivo
    # termos da função objetivo
    obj_termos = []
    for i in range(num_galaxias):
        for j in range(num_galaxias):
            obj_termos.append(int(distancias[i][j])*x[i][j])
    model.Minimize(sum(obj_termos))

    # -- resolve
    solver = cp_model.CpSolver()  # obtém o solver
    solver.Solve(model)  # resolve

    # obtém a solução parcial na forma de matriz (sol_parcial[i][j] == True se x[i][j] == True)
    sol_parcial = [[solver.BooleanValue(x[i][j]) for i in range(
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
                    aux_list.append(x[i][j])
            model.Add(sum(aux_list) <= len(subciclo) - 1)

        solver.Solve(model)  # resolve novamente
        sol_parcial = [[solver.BooleanValue(x[i][j]) for i in range(  # obtém outra solução parcial
            num_galaxias)] for j in range(num_galaxias)]
        # se a sol_parcial não tem nenhum subciclo, ela é a correta!
        subciclos = acha_subciclos(sol_parcial)

    print("-->SOLUÇÃO FINAL")
    print("Solução encontrada:")
    for i in range(num_galaxias):
        for j in range(num_galaxias):
            if solver.BooleanValue(x[i][j]):
                print(f"De {i} para {j} -> custo: {distancias[i][j]}")
    print(f"Custo total: {solver.ObjectiveValue()}")

# calcula a distância euclidiana 2d entre dois pontos representados por tuplas


def dist_euclid(a, b):
    return sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))

# constrói a matriz de distâncias


def constroi_matriz(coords):
    num_vertices = len(coords)
    distancias = []
    for i in range(num_vertices):
        distancias.append([])
        for j in range(num_vertices):
            distancias[i].append(round(dist_euclid(coords[i], coords[j])))
    return distancias

# pega input e retorna numa lista de tuplas


def get_input():
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
    distancias = constroi_matriz(coords)
    resolve_tsp(distancias)


if __name__ == '__main__':
    main()
