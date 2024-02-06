import src.lexer.analizador_lexico as al
import src.parser.tabla_analisis as ta

def get_grammar(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    NT = content[0].replace("\n", "")
    NT = NT.split(" ")
    TE = content[1].replace("\n", "")
    TE = TE.split(" ")
    grammar = []
    content = content[2:]
    
    for line in content:
        grammar.append(line.strip().split(" -> "))

    return NT, TE, grammar

# Obtiene una posicion en la tabla
# ------------------------------
# ADVERTENCIA!: DEMASIADOS PARAMETROS
# ------------------------------
# s: Numero de estado
# a: Simbolo
def get_action(TA, NT, TE, s, a):
    # Obtiene el indice i
    i = int(s)
    # Obtiene el indice j
    if a in TE:
        j = TE.index(a)
    else:
        j = len(TE) + NT.index(a)
    
    return TA[i][j]

def find_error(row, TE):
    indexs = []
    symbols = []
    n = len(TE)-1

    for i in range(0, n):
        if row[i] != '  ':
            indexs.append(i)

    for j in indexs:
        symbols.append(TE[j])
    
    return symbols

# Otorga formato a las filas
def get_rowda(stack, input, action):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(input)

    return [column1,  column2, action]

def get_rowr(stack, input, action, production):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(input)
    column3 = '->'.join(production)
    column3 = action + ' ' + column3

    return [column1, column2, column3]

def get_rowe(stack, input, symbols):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(input)
    column3 = 'Error se esperaba ' + ' o '.join(symbols)

    return [column1, column2, column3]

# ------------- ANALIZADOR ------------- #
def to_analyze(grammar_path, file_path):
    # Variables
    NT, TE, augmentedGrammar = get_grammar(grammar_path)
    stack = []
    input = []
    accept = False
    error = False
    production = []
    analysis = []

    # Obtiene la tabla y demas valores
    # NT, TE, TA = ta.to_create(grammar_path)
    # TE.append('$')
    #input = get_tokens(tokens_path)
    input= al.analizar(file_path).strip().split(' ')
    input.append('$')
    TA = ta.tablaDeAnalisis(grammar_path)
    
    # Algoritmo
    stack.append(0)

    while not (accept or error):
        case_action = get_action(TA, NT, TE, stack[-1], input[0])
        if case_action[0] in {'d', 'r'}:
            # Calcula el indice de r o d
            index = case_action[1:]
            index = int(index)
            if case_action[0] == 'd':
                # print(stack, "\t\t", input, "\t\t", case_action)
                analysis.append(get_rowda(stack, input, case_action))
                stack.append(input[0])
                stack.append(index)
                input.pop(0)
            elif case_action[0] == 'r':
                production = augmentedGrammar[index]
                # print(stack, "\t\t", input, "\t\t", case_action, " ", production)
                analysis.append(get_rowr(stack, input, case_action, production))
                if production[-1] != '@':
                    for j in range(0, 2*(production[-1].count(' ')+1)):
                        stack.pop()
                j = stack[-1]
                stack.append(production[0])
                ir_a = get_action(TA, NT, TE, j, production[0])
                stack.append(ir_a)
        else:
            if case_action == 'AC':
                # print(stack, "\t\t", input, "\t\t", case_action)
                analysis.append(get_rowda(stack, input, case_action))
                accept = True
            else:
                symbols = find_error(TA[stack[-1]], TE)
                # print(stack, "\t\t", input, "\t\tError se esperaba: ", symbols)
                analysis.append(get_rowe(stack, input, symbols))
                error = True
    
    return analysis