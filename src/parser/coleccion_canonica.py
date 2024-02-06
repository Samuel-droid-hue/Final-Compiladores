def canonica(gramaticaA,noterminal):
    n=[]
    n=gramaticaA[0].replace("->", ".")
    C = {0 : cerradura([n],gramaticaA)}
    
    conta=1
    Cerr=[[]]
    for s in C.values():
        Cerr.append(s)
    Cerr.pop(0)
    ir=[]
    for L in Cerr:
        
        for elemento in L:
            elemento=elemento.split(" ")
            index=elemento.index(".")
            
            try:
                X=elemento[index+1]
                if X!='$':
                    nuevoE=ir_a(L,X,gramaticaA)
                    if nuevoE != [] and nuevoE not in Cerr:
                        Cerr.append(nuevoE)
                        C[conta]=nuevoE
                        indexC=Cerr.index(L)
                        
                        ir.append(str(indexC)+" "+str(X)+" "+str(conta))
                        conta+=1
                    else:
                        
                            ir.append(str(Cerr.index(L))+" "+str(X)+" "+str(Cerr.index(nuevoE)))
                else:
                    ir.append(str(Cerr.index(L))+" "+str(X)+" "+str(-1))
                    continue
                        
            except IndexError:
                continue
    ir=set(ir)
    ir=list(ir)
    ir.sort()
    ir_T=[]
    ir_NT=[]
    
    for k in ir:
        k=k.split(" ")
        k[0]=int(k[0])
        k[2]=int(k[2])
        if k[1] in noterminal:
            ir_NT.append(k)
            
        else:
            ir_T.append(k)
            
    Estados=[]
    for V in C.values():
        Estados.append(V)  
    return Estados,ir_T,ir_NT
                
        
        
        
def ir_a(L,X,gramatica):
    j=[]
    for l in L:
        l=l.split(" ")
        index=l.index(".")
        try:    
            y=l[index+1]
            if y==X :
                l[index+1]='.'
                l[index]=y
                l=" ".join(l)
                j.append(l)
        except IndexError:
            continue
            
    return cerradura(j,gramatica)   
    
    
def cerradura(I,gramatica):
    nuevoI = []
    nuevoI = I
    for elemento in nuevoI:
        elemento = elemento.split(" ")
        index=elemento.index(".")
        try:    
            B=elemento[index+1]
            for regla in gramatica:
                regla=regla.replace(" @", "")
                regla=regla.replace("->", ".")
                regla = regla.split(" ")
                if regla[0] == B:
                    regla=' '.join(regla)
                    if regla not in nuevoI:
                        nuevoI.append(regla)  
        except IndexError:
            continue                    
    return nuevoI