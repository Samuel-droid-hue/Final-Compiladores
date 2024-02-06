import string
import re
from collections import OrderedDict

class AnalizadorLexico:
    def __init__(self):
        self.reservadas = {
            'printf', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'main', 'float', 'for', 'goto', 'if','bool',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            'auto','extern','scanf','pow','malloc','free','strlen','strcpy','fopen','fclose'
        }
        self.caracteres = {
            '\n': 'salto de línea', '\t': 'tabulación', '(': 'paréntesis abierto', '{': 'llave abierta',
            ',': 'coma', '<': 'menor que', '>': 'mayor que', '=': 'igual', '+': 'más', '-': 'menos',
            '*': 'asterisco', ';': 'punto y coma', ' ': 'espacio', '}': 'llave cerrada',')': 'paréntesis cerrado',
            '"': 'comillas dobles', '/': 'barra', '&': 'y', '%': 'porcentaje', '|':'barra',':':'doblep'
            
        }
    def caracter_separador(self,caracter):
        return caracter in self.caracteres

    lin_num = 1

    def tokenizar(self, codigo):
        reglas = [
            ('RESERVADO', '|'.join(re.escape(word) for word in self.reservadas)),
            ('PARENTA', r'\('),        # (
            ('PARENTC', r'\)'),        # )
            ('LLAVEA', r'\{'),          # {
            ('LLAVEC', r'\}'),          # }
            ('COMA', r','),            # ,
            ('PCOMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('AMPER', r'&'),             # &
            ('PORCENT', r'%'),             # %
            ('TWOP', r':'),             # :
            ('COMEN_START', r'/\*'),  # Inicio de comentario /* 
            ('COMEN_END', r'\*/'),    # Fin de comentario */
            ('COMENT',  r'\/\/.*'),             # &&
            ('literalCad', r'"([^"\\]*(\\.[^"\\]*)*)"'),
            ('literalCar', r"'([^'\\]*(\\.[^'\\]*)*)'"),
            #('ARRAY',r'[a-zA-Z1-9_]\w*\[\d+\]'),        #arreglos
            #('ARRAYAP',r'\*[a-zA-Z1-9]*.\[[1-9]*\]'),        #apuntadores arreglos
            #('APUNT',r'\*[a-zA-Z_]\w*'),        #apuntadores
            ('CORCHETEA', r'\['),           # [
            ('CORCHETEC', r'\]'),           # ]
            ('IGUAL', r'\='),            # =
            ('MAYOR', r'<'),               # <
            ('MENOR', r'>'),               # >
            ('iNCRE', r'\+\+'),            # ++
            ('DECRE', r'--'),            # -
            ('SUMA', r'\+'),            # +
            ('RESTA', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # / 
            ('id', r'[a-zA-Z]\w*'),     # IDENTIFICADORES
            ('nfloat', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('nint', r'\d(\d)*'),          # INT
            ('NEWLINE', r'\n'),         # NUEVA LINEA
            ('SKIP', r'[ \t]+'),        # SPACIO Y TABS
            ('MISMATCH', r'.'),         # OTRO CARACTER
        ]
        tokens_unidos = '|'.join('(?P<%s>%s)' % x for x in reglas)

        # Listas de salida del programa
        simbolos=[]
        token = []
        lexema = []
        fila = []
        total = []
        tira_token = ""
        in_comentario = False 
        lineas_validas= []
        with open(codigo, 'r') as file:
            codigo = file.read()
            
        
        # Analiza el código para encontrar los lexemas y sus respectivos Tokens
        for m in re.finditer(tokens_unidos, codigo):
            token_tipo = m.lastgroup
            token_lexema = m.group(token_tipo)

            
            if token_tipo == 'NEWLINE':
                self.lin_num += 1
            elif token_tipo == 'COMEN_START':
                in_comentario = True
                continue  # Salta al siguiente token sin imprimir nada
            elif token_tipo == 'COMEN_END':
                in_comentario = False
                continue  # Salta al siguiente token sin imprimir nada
            elif in_comentario:
                continue
            elif token_tipo == 'COMENT':
                continue
            elif token_tipo == 'SKIP':
                continue
            elif token_tipo == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexema, self.lin_num))
            else:

                    token.append(token_tipo)
                    lexema.append(token_lexema)
                    fila.append(self.lin_num)
                    
                    # Imprimir información sobre un Token
                    if token_tipo != 'id'and token_tipo != 'literalCad' and token_tipo != 'literalCar' and token_tipo != 'nint'and token_tipo != 'nfloat':
                        total += ["{2} , {1}  , {1} ".format("id", token_lexema, self.lin_num)]
                        tira_token += token_lexema + " "
                    else:
                        total += ["{2} , {1}  , {0} ".format(token_tipo, token_lexema, self.lin_num)]
                        tira_token += token_tipo + " "
                    if token_tipo == 'id':
                        simbolos.append((token_lexema,(0),(0)))
                        

        return tira_token, total, simbolos 

    def encontrar_error(self, archivo_path, caracteres_separadores, letra):
        lineas_validas = []
        errores = []
        num_linea = 1  # Número de línea inicial
        with open(archivo_path, 'r') as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                nueva_linea = ''.join(char if char in caracteres_separadores or char in letra else (errores.append((num_linea, char,char)), ' ')[1] for char in linea)
                lineas_validas.append(nueva_linea)
                num_linea += 1
        # Sobrescribe el archivo con las líneas válidas
        with open(archivo_path, 'w') as archivo:
            archivo.writelines(lineas_validas)

        return errores
    
def analizar(file):
    analizador= AnalizadorLexico()
    
    caracteres_separadores = analizador.caracteres
    letra= string.ascii_letters + string.digits + '.' + "'" + "_" +'['+']'+'!'+'\\'
    errores = analizador.encontrar_error(file, caracteres_separadores,letra)
    tira_tokens, total,palabras_id= analizador.tokenizar(file)
    conjunto_sin_duplicados = OrderedDict()
    # Iteración sobre la lista palabras_id_unicas para crear un conjunto sin duplicados:
    for elemento in palabras_id:
        conjunto_sin_duplicados[elemento] = None  # Usamos el objeto None como marcador
        
    analyzed = True
    with open("analizador.txt", 'w') as archivo:
    
        for elem in total:
            print(elem)
            archivo.writelines(elem + '\n')
        
        print("errores=============================================")
        for err in errores:
            print(err)
            archivo.writelines(err+ '\n')
        print("id=============================================")
        for con in conjunto_sin_duplicados:
            print(con)
    return tira_tokens