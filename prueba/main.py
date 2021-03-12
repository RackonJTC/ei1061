from pprint import pprint


FIN="FIN"
#TIPOS DE INSTRUCCIONES
NOP="NOP"
MEM="MEM"
ALU="ALU"
BEQ="BEQ"
# FIN TIPO INSTRUCCIONES

#TIPOS OPERACIONES
ADD="ADD"
SUB="SUB"
LOAD="LOAD"
STORE="STORE"
#TIPOS OPERACIONES




# La instruccion codificada supongo que estan en formato string
# La instruccion decodificada la guardo en sus campos

# Registros inicializados a 10
#   reg[0] ... reg[15]
reg = [a for a in range(0,16)]

# Memoria de instrucciones
# memIns[0] ... memIns[31]
memDat = [a for a in range(0,32)]

# Memoria de datos
# memDat[0] ... memDat[31]
memDat = [a for a in range(0,32)]

# Salto
salto = 0

# Simula la etapa IF
def simulaEtapaIf(lista):
    instruccion,id_inst = lista
    print("\t\t-- ETAPA IF de I",id_inst)
    return lista

# Simula la etapa ID
def simulaEtapaId(lista):
        instruccion, id_inst=lista
        print("\t\t-- ETAPA ID de I",id_inst)
        if(instruccion=="NOP"):
            return [NOP,0,0,0,0,0,0,0,id_inst]

        instSplit = instruccion.split(" ")
        if(instSplit[0]=="add" or instSplit[0]=="sub"):
            rd=int(instSplit[1][1:-1])
            rs=int(instSplit[2][1:-1])
            op1=reg[rs]
            rt=int(instSplit[3][1:])
            op2=reg[rt]
            inm=-1
            tipo=ALU
            if(instSplit[0]=="add"):
                operacion=ADD
            else:
                operacion=SUB
            return [tipo,operacion,rs,op1,rt,op2,inm,rd,id_inst]

        elif(instSplit[0]=="lw" or instSplit[0]=="sw"):
            rd=-1
            rs=int(instSplit[2].split("(")[1][1:-1])
            op1=reg[rs]
            rt=int(instSplit[1][1:-1])
            op2=reg[rt]
            inm=int(instSplit[2].split("(")[0])
            tipo=MEM
            if(instSplit[0]=="lw"):
                operacion=LOAD
            else:
                operacion=STORE
            return [tipo,operacion,rs,op1,rt,op2,inm,rd,id_inst]
        elif(instSplit[0]=="beqz"):
            rs=int(instSplit[1][1:-1])
            op1=reg[rs]
            inm=int(instSplit[2])
            return [BEQ,-1,rs,op1,-1,-1,inm,-1,id_inst]


# Simula la etapa EX
def simulaEtapaEx(lista):
    tipo,operacion,rs,op1,rt,op2,inm,rd,id_inst = lista
    print("\t\t-- ETAPA EX de I",id_inst)
    res=0
    if (tipo==NOP):
        return [rd,0,rt,op2,NOP,0,id_inst]
    if(tipo==ALU):
        if(operacion==ADD):
            res=op1+op2
        else:
            res=op1-op2

    elif(tipo==MEM):
        res=inm+op1
    elif(tipo==BEQ):
        if(op1==0): res=0
        else: res=inm
        global salto
        salto=res
    return [rd,res,rt,op2,tipo,operacion,id_inst]


# Simula la etapa MEM
def simulaEtapaMem(lista):
    rd,res,rt,op2,tipo,operacion,id_inst=lista
    print("\t\t-- ETAPA MEM de I",id_inst)
    if(tipo==NOP):
        return [0,0,0,tipo,0,id_inst]
    if(tipo==ALU):
        return [res,rd,rt,tipo,operacion,id_inst]
    if(operacion==STORE):
        memDat[res]=op2
    else:
        res=memDat[res]
    return [res,rd,rt,tipo,operacion,id_inst]

# Simula la etapa WB
def simulaEtapaWB(lista):
    res,rd,rt,tipo,operacion,id_inst = lista
    print("\t\t-- ETAPA WB de I",id_inst)
    if(tipo==NOP):
        return
    if(tipo==MEM):
        if(operacion==LOAD):
            reg[rt]=res
    if(tipo==ALU):
       reg[rd]=res



class RS_IFID():
    InstruccionCodificada=""
    id_inst=-1

    def getInstruccion(self):
        return [self.InstruccionCodificada,self.id_inst];
    def setInstruccion(self,lista):
        self.InstruccionCodificada,self.id_inst=lista;
    def vaciaRegistro(self):
        self.InstruccionCodificada,self.id_inst = ["",-1]
    def __str__(self):
        return "\t\t\t"+str(self.__dict__)

class RS_IDEX():
    id_inst=-1
    tipo=""
    operacion=""
    rs=""
    op1=-1
    rt=""
    op2=-1
    inm=-1
    rd=""

    def getInstruccion(self):
        return [self.tipo,self.operacion,self.rs,self.op1,self.rt,self.op2,self.inm,self.rd,self.id_inst]
    def setInstruccion(self,lista):
        self.tipo,self.operacion,self.rs,self.op1,self.rt,self.op2,self.inm,self.rd,self.id_inst = lista
    def vaciaRegistro(self):
        self.tipo,self.operacion,self.rs,self.op1,self.rt,self.op2,self.inm,self.rd,self.id_inst = ["","","",-1,"",-1,-1,"",-1]
    def __str__(self):
         return "\t\t\t"+str(self.__dict__)
class RS_EXMEM():
    id_inst=-1
    rd=""
    res=-1
    rt=""
    op2=""
    tipo=""
    operacion=""

    def getInstruccion(self):
        return [self.rd,self.res,self.rt,self.op2,self.tipo,self.operacion,self.id_inst]
    def setIstruccion(self,lista):
        self.rd,self.res,self.rt,self.op2,self.tipo,self.operacion,self.id_inst=lista
    def vaciaRegistro(self):
        self.rd,self.res,self.rt,self.op2,self.tipo,self.operacion,self.id_inst = ["",-1,"","","","",-1]

    def __str__(self):
         return "\t\t\t"+str(self.__dict__)
class RS_MEMWB():
    id_inst=-1
    res=-1
    rd=""
    rt=""
    tipo=""
    operacion=""
    def getInstruccion(self):
        return [self.res,self.rd,self.rt,self.tipo,self.operacion,self.id_inst]
    def setInstruccion(self,lista):
        self.res,self.rd,self.rt,self.tipo,self.operacion,self.id_inst= lista
    def vaciaRegistro(self):
        self.res,self.rd,self.rt,self.tipo,self.operacion,self.id_inst = [-1,"","","","",-1]
    def __str__(self):
         return "\t\t\t"+str(self.__dict__)



# Carga de memoria de instrucciones
def cargaMemoria(fichero):
    f = open(fichero)
    global memIns
    memIns=[]
    i=0
    for linea in f:
        if(i==32): return
        memIns.append(linea.rstrip())
        i+=1
    memIns.append(FIN)
    print(memIns)

def main(codigo):
    global salto


    #Carga en memoria de instrucciones las instrucciones
    cargaMemoria(codigo)

    #Cuenta los ciclos de procesador
    ciclo=1

    #Inicializa los registros de segmentacion
    registro_ifid= RS_IFID()
    registro_idex= RS_IDEX()
    registro_exmem= RS_EXMEM()
    registro_memwb= RS_MEMWB()

    print("-"*50)
    print("            R0,R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13,R14,R15")
    print("REGISTROS: ",end="")
    print(reg)
    print()
    print("          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31")
    print("MEMORIA: ",end="")
    print(memDat)
    print("-"*50)


    print(" -- INICIO -- ")


    #Direccion de instruccion
    PC=0

    #Cuenta intrucciones ejecutadas
    instruccionEjecutadas=0

    #Variable que comprueba si hay algo en lso reg de seg y por ende hay algo en el cauce
    quedenInstruccionesCauce=True

    #Indica si se debe añadir un ciclo de parada (dependencia LOAD-ALU)
    cicloParada=False

    #Cuenta las inntruciones NOPS añadidas
    stalls=0

    # Indica cuantas nops se deben incluir (beqz)
    nopsRetartado=0

    # -------------------------------- BUCLE PRINCIPAL--------------------------------
    while(quedenInstruccionesCauce):
        print("\t -- CICLO ",ciclo," --")

        # DETECCION DE RIESGOS #

        # Entre dos operaciones ALU seguidas--------------------
        if(registro_idex.rs!=""):
            if(registro_idex.rs == registro_exmem.rd):
                if(registro_exmem.tipo==ALU):
                    if(registro_idex.tipo==ALU):
                        registro_idex.op1=registro_exmem.res
        if(registro_idex.rt!=""):
            if(registro_idex.rt == registro_exmem.rd):
                if(registro_exmem.tipo==ALU):
                    if(registro_idex.tipo==ALU):
                        registro_idex.op2=registro_exmem.res
        # -----------------------------------------------------

        # Entre dos operaciones ALU separadas 1 instruccion ---
        if(registro_idex.rs!=""):
            if(registro_idex.rs == registro_memwb.rd):
                if(registro_memwb.tipo==ALU):
                    if(registro_idex.tipo==ALU):
                        registro_idex.op1=registro_memwb.res
        if(registro_idex.rt!=""):
            if(registro_idex.rt == registro_memwb.rd):
                if(registro_memwb.tipo==ALU):
                    if(registro_idex.tipo==ALU):
                        registro_idex.op2=registro_memwb.res
        # -----------------------------------------------------

        # Entre operacion LOAD y ALU seguidas -----------------
        if(registro_idex.rs!=""):
            if(registro_idex.rs==registro_exmem.rt):
                if(registro_idex.tipo==ALU):
                    if(registro_exmem.operacion==LOAD):
                        cicloParada=True
                        #print(" ***** SE AÑADE CICLO PARADA (",ciclo,")--> STALL  (load+alu)")
                        registro_idex.op1=registro_exmem.res

        if(registro_idex.rt!=""):
            if(registro_idex.rt==registro_exmem.rt):
                if(registro_idex.tipo==ALU):
                    if(registro_exmem.operacion==LOAD):
                        cicloParada=True
                        #print(" ***** SE AÑADE CICLO PARADA (",ciclo,")--> STALL  (load+alu)")
                        registro_idex.op2=registro_exmem.res
        # -----------------------------------------------------
        # Entre operacion ALU y STORE seguidas ----------------
        if(registro_exmem.rt!=""):
            if(registro_exmem.rt==registro_memwb.rd):
                if(registro_exmem.operacion==STORE):
                    if(registro_memwb.tipo==ALU):
                            registro_exmem.op2=registro_memwb.res
        # -----------------------------------------------------

        #  fin DETECCION DE RIESGOS #


        #  ------------------------------------- ESTO ES EL CAUCE -------------------------------------
        if(registro_memwb.tipo!=""):
            simulaEtapaWB(registro_memwb.getInstruccion())
            registro_memwb.vaciaRegistro()
        if(registro_exmem.tipo!=""):
            lista=simulaEtapaMem(registro_exmem.getInstruccion())
            registro_memwb.setInstruccion(lista)
            registro_exmem.vaciaRegistro()
            print("\t\t\tREGISTRO MEM/WB: ",end="")
            print(registro_memwb)
        if(cicloParada):
            ciclo+=1
            print("\t\t***** STALL")
            stalls+=1
            cicloParada=False
            continue
        if(registro_idex.tipo!=""):
            lista=simulaEtapaEx(registro_idex.getInstruccion())
            registro_exmem.setIstruccion(lista)
            registro_idex.vaciaRegistro()
            print("\t\t\tREGISTRO EX/MEM: ",end="")
            print(registro_exmem)
        if(registro_ifid.InstruccionCodificada!=""):
            lista=simulaEtapaId(registro_ifid.getInstruccion())
            registro_idex.setInstruccion(lista)
            registro_ifid.vaciaRegistro()
            print("\t\t\tREGISTRO ID/EX: ",end="")
            print(registro_idex)
        #  ------------------------------------- FIN ESTO ES EL CAUCE -------------------------------------

        #Se añaden las 2 nops despues del beqz
        if(nopsRetartado!=0):
            registro_ifid.setInstruccion([NOP,instruccionEjecutadas])
            instruccionEjecutadas+=1
            stalls+=1
            nopsRetartado-=1
            print("\t\t\tREGISTRO IF/ID: ",end="")
            print(registro_ifid)
        else:
            if(salto != 0): # Si se tiene que saltar se cambia pc por salto
                PC=PC+salto
                salto=0
            if(memIns[PC]!=FIN): # Introduce instruccion al cauce
                lista=simulaEtapaIf([memIns[PC],instruccionEjecutadas])
                registro_ifid.setInstruccion(lista)
                instruccionEjecutadas+=1
                print("\t\t\tREGISTRO IF/ID: ",end="")
                print(registro_ifid)
                if(memIns[PC].split(" ")[0] == "beqz"): # SI es de tipo beqz debe añadir dos nops
                    nopsRetartado=2
                PC+=1

        # Compureba si en los registros de segmentaicion hay intrucciones
        quedenInstruccionesCauce = registro_ifid.InstruccionCodificada!="" or registro_idex.tipo!="" or registro_exmem.tipo!="" or registro_memwb.tipo!=""
        ciclo+=1

    # -------------------------------- FIN BUCLNE PRINCIPAL --------------------------------


    print("-"*50)
    print("Instrucciones ejecutadas: ",instruccionEjecutadas-stalls)
    print("Ciclos totales de ejecuccion: ",ciclo-1)
    print("Se han añadido",stalls,"ciclo/s de parada")
    print("-"*50)
    print("-"*50)
    print("           R0,R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13,R14,R15")
    print("REGISTROS: ",end="")
    print(reg)
    print()
    print("          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31")
    print("MEMORIA: ",end="")
    print(memDat)
    print("-"*50)


if __name__ == "__main__":
    main("CodigoEnsamblador3")
