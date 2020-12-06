--> Integrantes do grupo:
-> LUCAS G. M. MIRANDA - 10265892 - lucasgmm@usp.br 
-> MARCELA TIEMI SHINZATO - 10276953 - marcelats@usp.br
-> SÉRGIO RICARDO G. B. FILHO - 10408386 - sergiobarbosa@usp.br
-> TIAGO LASCALA AUDE - 8936742 - tiago.aude@usp.br
--> Solver utilizado: SCIP, através do Google OR-Tools
 
------------------------------------------------------------------------------------------

--> ATENÇÃO: ANTES DE RODAR O PROGRAMA, É PRECISO INSTALAR DOIS MÓDULOS
QUE SÃO UTILIZADOS PARA PLOTAR GRAFOS. Para instalá-los no Linux, basta executar
no terminal o seguinte comando:

pip3 install python-igraph pycairo

------------------------------------------------------------------------------------------

--> Para rodar o programa no Linux e resolver o toy problem, abra o terminal
no diretório em que tsp.py está localizado e execute:

python3 tsp.py < toy_problem.txt

--> Similarmente, para rodar as quatro instâncias exigidas na especificação:

python3 tsp.py < western_sahara.txt
python3 tsp.py < djibouti.txt
python3 tsp.py < qatar.txt
python3 tsp.py < uruguay.txt

-->AVISO: OS ARQUIVOS DAS INSTÂNCIAS DE WATERLOO (2020) FORAM REFORMATADOS
PARA COMBINAR COM A ENTRADA ESPERADA DO PROGRAMA. SE QUISER RODAR OUTRAS INSTÂNCIAS
QUE NÃO AS QUATRO CONTIDAS AQUI (western_sahara, djibouti, qatar e uruguay), BAIXE
O ARQUIVO E O FORMATE APROPRIADAMENTE. 

------------------------------------------------------------------------------------------

--> Se não quiser rodar o toy problem, nem nenhuma instância, apenas execute:

python3 tsp.py

--> Nesse caso, o usuário precisa fornecer a entrada, que é composta de

Um inteiro N, que representa o número de vértices
N coordenadas, x e y, separadas por um espaço

Exemplo de entrada válida:
5
-310 121
-80 170
101 391
217 97
107 40

------------------------------------------------------------------------------------------

OBS.: na pasta instancias_results existem as saídas das instâncias que rodamos, se isso for útil
de alguma forma.
