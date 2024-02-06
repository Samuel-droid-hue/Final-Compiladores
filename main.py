import src.parser.primeros_siguientes as ps

# Se sabe que van los primeros y siguientes van en el orden establecido por simbolos no terminales
path = "C:/Users/Ismael/Downloads/gramatica.txt"
no_terminales, terminales, reglas = ps.get_reglas(path)
p_s = ps.primeros_siguientes(no_terminales, terminales, reglas)
