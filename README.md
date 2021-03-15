## Integrantes do grupo:
- Lucas G. M. Miranda 
- Marcela Tiemi Shinnzato
- Sérgio Ricardo G. B. Filho
- Tiago Lascala Aude

## Arquivos mais relevantes

- Especificações do projeto: `descrição.pdf`
- Relatório final: `relatorio.pdf`
- Código: `tsp.py`

## Solver utilizado
SCIP, através do Google OR-Tools

## Instalação do PyCairo e iGraph

Antes de rodar o programa, é preciso instalar dois módulos
que são utilizados para plotar gráficos. Para instalá-los no Linux, basta executar
no terminal o seguinte comando: 

`pip3 install python-igraph pycairo`

## Rodando o Programa

Para rodar o programa no Linux e resolver o toy problem, abra o terminal
no diretório em que tsp.py está localizado e execute:

`python3 tsp.py < toy_problem.txt`

Similarmente, para rodar as quatro instâncias exigidas na especificação:

`python3 tsp.py < western_sahara.txt`  
`python3 tsp.py < djibouti.txt`  
`python3 tsp.py < qatar.txt`  
`python3 tsp.py < uruguay.txt`  

**Os arquivos das instâncias de waterloo (2020) foram reformatados
para combinar com a entrada esperada do programa. se quiser rodar outras instâncias
que não as quatro contidas aqui (western_sahara, djibouti, qatar e uruguay), baixe
o arquivo e o formate apropriadamente.** 

Se não quiser rodar o toy problem, nem nenhuma instância, apenas execute:

`python3 tsp.py`

Nesse caso, o usuário precisa fornecer a entrada, que é composta de

- Um inteiro N, que representa o número de vértices
- N coordenadas, x e y, separadas por um espaço

Exemplo de entrada válida:  
5  
-310 121  
-80 170  
101 391  
217 97  
107 40  

OBS.: na pasta instancias_results existem as saídas das instâncias que foram rodadas, se isso for útil
de alguma forma.
