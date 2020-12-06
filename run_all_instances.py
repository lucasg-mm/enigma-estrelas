import os
import tsp

def get_filenames(directory):

    file_names = os.listdir(directory)

    names = [ ]

    for file_name in file_names:
        name_size = file_name.split("_")
        names.append([name_size[0], int(name_size[1][:-4]) ])

    names.sort(key=lambda x:x[1])

    return names


def parse_file(file_name):

    tuplas = []
    with open(file_name, "r") as f:

        data = f.read().strip("\n").split("\n")[7:]
        
        for line in data:
            try:
                values = line.split(" ")[1:]
                tuplas.append( (float(values[0]), float(values[1])) )
            except IndexError:
                # eof
                pass

    return tuplas

def save_result(directory, instancia, result):
    
    filename = instancia+"_result"
    
    with open(os.path.join(directory, filename), "w") as f:
        f.write("Custo: " + str(result[0]) + "\n")
        f.write("Solucao: " + "\n")
        for value in result[1]:
            f.write(str(value) + "\n")

if __name__ == "__main__":

    directory = "instancias_todas"
    names_size = get_filenames(directory)

    for name_size in names_size[:2]:
        name_size[1] = str(name_size[1])
        f_name = "_".join(name_size)
        coords = parse_file(os.path.join(directory, f_name + ".tsp"))    
        result = tsp.resolve_tsp(coords, desenhar=True, lim_minutos=30, heuristica="2-opt")
        save_result("instancias_results", name_size[0], result)