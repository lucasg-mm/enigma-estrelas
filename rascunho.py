def elimina_subciclos(mat_adj, custos, num_vertices):
    rota = []
    proximo = 0 
    for _ in range(num_vertices+1):
        rota.append(proximo)
        atual = proximo
        proximos_possiveis = [i for i in range(num_vertices) if mat_adj[atual][i] == 1 and i not in rota]
        if proximos_possiveis:
            if custos[atual][proximos_possiveis[0]] < custos[atual][proximos_possiveis[1]]:
                proximo = proximos_possiveis[0]
            else:
                proximo = proximos_possiveis[1]    
        else:
            proximos_possiveis = [
                custo if custos[atual].index(custo) not in rota else inf for custo in custos[atual]]
            # obtém o índice do próximo nó a ser visitado
            proximo = proximos_possiveis.index(min(proximos_possiveis))
