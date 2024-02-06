import src.parser.primeros_siguientes as ps
import src.lexer.analizador_lexico as al

# ANALIZADOR LEXICO
path_uno = "C:/Users/Ismael/Downloads/programa.txt"
al.analizar(path_uno)

# PRIMEROS Y SIGUIENTES
# Se sabe que van los primeros y siguientes van en el orden establecido por simbolos no terminales
path = "C:/Users/Ismael/Downloads/gramatica.txt"
no_terminales, terminales, reglas = ps.get_reglas(path)
p_s = ps.primeros_siguientes(no_terminales, terminales, reglas)
print(p_s)
