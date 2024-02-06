def get_reglas(path):
    with open(path, 'r') as file:
        content = file.readlines()
    content=' '.join(content)
    content=content.split("\n ")
    content2=content
    content ='-|-'.join(content)
    content=content.split("-> ")
    content =''.join(content)
    content=content.split("-|-")
    no_terminales = content[0].strip()
    terminales = content[1].strip()
    content.pop(0)
    content.pop(0)
    content.pop(0)
    content2.pop(0)
    content2.pop(0)


    return no_terminales, terminales, content,content2

def obtener_Primeros(S,regla,noTerminales,terminales,bandera=0):
    v=0
    a=0
    primeros=[]
    if S=="@" :
        if bandera==1:
            return bandera,""
        return bandera,S
    if S in terminales :
        return 0,S
    for i in regla:
        i=i.split(" ")
        b=1
        i = [conta for conta in i if conta != '']
        if i[0]==S :
                if len(i)>2:
                    bandera=1
                h=1
                while (bandera==1 or b==1) and i[h] !=S:
                    b=0
                    v,k=obtener_Primeros(i[h],regla,noTerminales,terminales,bandera)
                    if v==1:
                        a=1
                    primeros.append(k)
                    primeros[0]=' '.join(primeros)
                    if len(primeros)==2:
                        primeros.pop(1)
                    if len(i)==2:    
                        break
                    h=h+1
                    if a==1 and v==1:
                        b=1
                    else:
                        bandera=0  
    if a==0 and bandera==1:
        bandera=0
        
    return bandera,primeros[0]  

def obtener_siguientes(i,regla,noterminales,terminale,primeros,sig):
    siguiente=""
    for reg in regla:
        reg=reg.split(" ")
        B=reg[0]
        reg.pop(0)
        reg = [conta for conta in reg if conta != '']
        if i in reg:
                index=reg.index(i)
                if index+1<len(reg):
                    if  reg[index+1] in terminale:
                        siguiente=siguiente+" "+reg[index+1]
                    else:
                        siguiente=siguiente+" "+primeros[reg[index+1]]
                        if "@" in siguiente:
                            conta=1
                            while ("@" in siguiente) and (index+conta<len(reg)):
                                
                                if index+conta!=index+1:
                                    siguiente=siguiente.replace("@","")
                                    if reg[index+conta] in terminale:
                                        siguiente=siguiente+" "+reg[index+conta]
                                    else:
                                        siguiente=siguiente+" "+primeros[reg[index+conta]]
                                conta=conta+1
                            if "@" in siguiente: 
                                if i != B:   
                                    try:
                                        if ("@" in sig[B]) and ("@" in siguiente):
                                            siguiente=siguiente+" "+sig[B]
                                        else:
                                            siguiente=siguiente+" "+sig[B]
                                            siguiente=siguiente.replace("@","")
                                    except KeyError:
                                        if i != B:
                                            sig[B]=obtener_siguientes(B,regla,noterminales,terminale,primeros,sig)
                                            sig[B]=sig[B].split(" ")
                                            sig[B]=list(set(sig[B]))
                                            sig[B] = [conta for conta in sig[B] if conta != '']
                                            sig[B]=' '.join(sig[B])
                                            if ("@" in sig[B]) and ("@" in siguiente):
                                                siguiente=siguiente+" "+sig[B]
                                            else:
                                                siguiente=siguiente+" "+sig[B]
                                                siguiente=siguiente.replace("@","")
                else:
                    if i != B:   
                        try:
                                siguiente=siguiente+" "+sig[B]
                        except KeyError:
                            if i != B:
                                sig[B]=obtener_siguientes(B,regla,noterminales,terminale,primeros,sig)
                                sig[B]=sig[B].split(" ")
                                sig[B]=list(set(sig[B]))
                                sig[B] = [conta for conta in sig[B] if conta != '']
                                sig[B]=' '.join(sig[B])
                                siguiente=siguiente+" "+sig[B]
                                if ("@" in sig[B]) and ("@" in siguiente):
                                    siguiente=siguiente+" "+sig[B]
                                else:
                                    siguiente=siguiente+" "+sig[B]
                                    siguiente=siguiente.replace("@","")
    
    return siguiente

def primeros_siguientes(noterminales,terminale,regla):
    noterminales=noterminales.split(" ")
    terminale=terminale.split(" ")
    bandera=0
    primeros={}
    for i in noterminales:
        bandera,primeros[i]=obtener_Primeros(i,regla,noterminales,terminale)
    for i in noterminales:
        primeros[i]=primeros[i].split(" ")
        primeros[i]=list(set(primeros[i]))
        primeros[i] = [i for i in primeros[i] if i != '']
        primeros[i]=' '.join(primeros[i])

    siguiente={}
    siguiente[noterminales[0]]="$"
    for i in noterminales:
        try:
            if len(siguiente[i])<2:
                siguiente[i]=siguiente[i]+obtener_siguientes(i,regla,noterminales,terminale,primeros,siguiente)
        except KeyError:
            
            siguiente[i]=obtener_siguientes(i,regla,noterminales,terminale,primeros,siguiente)
        
        siguiente[i]=siguiente[i].split(" ")
        siguiente[i]=list(set(siguiente[i]))
        siguiente[i] = [i for i in siguiente[i] if i != '']
        siguiente[i]=' '.join(siguiente[i])

    p=[]
    S=[]
    for i in noterminales:
        p.append(primeros[i])
        S.append(siguiente[i])
    PS={}
    PS["S"]=S
    PS["P"]=p

    return PS