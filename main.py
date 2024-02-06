import src.parser.primeros_siguientes as ps
import src.semantic.analizador_semantico as asm

path = "gramatica.txt"
program = "program.txt"
never = asm.to_analyze(path, program)
print(never)