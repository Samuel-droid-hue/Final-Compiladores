import src.semantic.analizador_semantico as asm

path = "gramatica2.txt"
program = "program.txt"
never = asm.to_analyze(path, program)

for elem in never:
    print(elem)