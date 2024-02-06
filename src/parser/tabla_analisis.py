import src.parser.primeros_siguientes as ps
import src.parser.coleccion_canonica as cn

def imprimirTabla(tabla):
    for fila in range(len(tabla)):
        print(str(fila)+str(tabla[fila]))

def tablaDeAnalisis(path):
    def obtenerIndex(simb, arreglo):
        for i in range(len(arreglo)):
            if arreglo[i] == simb:
                return i
        return -1
    
    #Obtiene las reglas, los terminales y no terminales
    no_terminales, terminales, reglas, reglas2 = ps.get_reglas(path)

    #Aqui debemos obtener los estados, ir_a_T y ir_a_NT
    estados, ir_a_T, ir_a_NT = cn.canonica(reglas2, no_terminales)

    #Obtiene Primeros y siguientes
    p_s = ps.primeros_siguientes(no_terminales, terminales, reglas)

    #Resguarda solo los siguientes
    siguientes = p_s['S']

    #Convierte terminales y no terminales a arreglos de cadenas.
    no_terminales = no_terminales.split(" ")
    terminales = terminales.split(" ")

    #Obtiene los tamaños
    tamTerminales = len(terminales)
    tamNoTerminales = len(no_terminales)
    tamEstados = len(estados)

    #Crea la tabla vacia
    columnas = tamTerminales + tamNoTerminales + 1
    TAS = [[' ' for _ in range(columnas)] for _ in range(tamEstados)]

    #Empieza con los desplaza
    for irA in ir_a_T:
        if irA[1] == '$':
            TAS[irA[0]][tamTerminales] = "ac"
        else:
            index = obtenerIndex(irA[1], terminales)
            TAS[irA[0]][index] = "d"+str(irA[2])

    #Empieza con ir a no terminales
    for irA_2 in ir_a_NT:
        index = obtenerIndex(irA_2[1], no_terminales)
        TAS[irA_2[0]][tamTerminales + 1 + index] = str(irA_2[2])
    
    #Empieza con remplaza
    estadoActual = 0
    for elementos in estados:
        for e in elementos:
            if e[len(e) - 1] == '.':
                subcadena = e[:-2]
                if len(subcadena) == 1:
                    subcadena = subcadena + " @"
                for j in range(len(reglas)):
                    if reglas[j] == subcadena:
                        noTerminal = subcadena[0]
                        indexNT = obtenerIndex(noTerminal, no_terminales)
                        sigNT = siguientes[indexNT]
                        sigNT = sigNT.split(" ")
                        for sim in sigNT:
                            if sim == '$':
                                TAS[estadoActual][tamTerminales] = "r" + str(j+1)
                            else:
                                ind = obtenerIndex(sim, terminales)
                                TAS[estadoActual][ind] = "r" + str(j+1)
        estadoActual += 1
    return TAS