import sys

# DATOS
# Simulador de un procesador segmentado de 5 etapas (IF,ID/OF, EX, MEM, WB).
# 16 registros para numeros de 32 bits de r0 a r15
# Memoria con capacidad para 32 instrucciones de 32 bits, desde 0 a 31
# Memoria de datos con capacidad para 31 numeros de 32 bits, desde 0 a 31

class Instruccion:  # add rd=r4 rs=r0 rt=r3
    operacion = None
    id_rd = None
    id_rs = None
    id_rt = None
    inm = None

    def __init__(self, operacion, id_rd, id_rs, id_rt, inm):
        self.operacion = operacion
        self.id_rd = id_rd
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.inm = inm

    def getOperacion(self):
        return self.operacion

    def getRd(self):
        return self.id_rd

    def getRs(self):
        return self.id_rs

    def getRt(self):
        return self.id_rt

    def getInm(self):
        return int(self.inm)

    def toSring(self):
        if self.operacion=="NOP":
            return "NOP"
        if self.operacion=="sw":
            return self.operacion + " " + self.id_rt + ", " + self.inm + "(" + self.id_rs + ")"
        if self.operacion=="lw":
            return self.operacion + " " + self.id_rt + ", " + self.inm + "(" + self.id_rs + ")"
        return self.operacion + " " + self.id_rd + ", " + self.id_rs + ", " + self.id_rt

class Reg_IF_ID:
    instruccion = None
    tipo = None
    operacion = None
    id_rs = None
    id_rt = None
    id_rd = None
    inmediato = None

    def getInstruccion(self):
        return self.instruccion

    def getTipo(self):
        return self.tipo

    def getOperacion(self):
        return self.operacion

    def getRs(self):
        return self.id_rs

    def getRt(self):
        return self.id_rt

    def getRd(self):
        return self.id_rd

    def getInm(self):
        return self.inm

    def setInstruccion(self, instruccion):
        self.instruccion = instruccion

    def setTipo(self, tipo):
        self.tipo = tipo

    def setOperacion(self, operacion):
        self.operacion = operacion

    def setRs(self, id_rs):
        self.id_rs = id_rs

    def setRt(self, id_rt):
        self.id_rt = id_rt

    def setRd(self, id_rd):
        self.id_rd = id_rd

    def setInm(self, inm):
        self.inm = inm

class Reg_ID_EX:
    instruccion = None
    tipo = None
    operacion = None
    id_rs = None
    id_rt = None
    id_rd = None
    inmediato = None
    op1 = None
    op2 = None

    def getInstruccion(self):
        return self.instruccion

    def getTipo(self):
        return self.tipo

    def getOperacion(self):
        return self.operacion

    def getRs(self):
        return self.id_rs

    def getRt(self):
        return self.id_rt

    def getRd(self):
        return self.id_rd

    def getInm(self):
        return self.inm

    def getOp1(self):
        return self.op1

    def getOp2(self):
        return self.op2

    def setInstruccion(self, instruccion):
        self.instruccion = instruccion

    def setTipo(self, tipo):
        self.tipo = tipo

    def setOperacion(self, operacion):
        self.operacion = operacion

    def setRs(self, id_rs):
        self.id_rs = id_rs

    def setRt(self, id_rt):
        self.id_rt = id_rt

    def setRd(self, id_rd):
        self.id_rd = id_rd

    def setInm(self, inm):
       self.inm = inm

    def setOp1(self, op1):
        self.op1 = op1

    def setOp2(self, op2):
        self.op2 = op2

class Reg_EX_MEM:
    instruccion = None
    tipo = None
    id_rt = None
    id_rd = None
    res = None
    op2 = None

    def getInstruccion(self):
        return self.instruccion

    def getTipo(self):
        return self.tipo

    def getRt(self):
        return self.id_rt

    def getRd(self):
        return self.id_rd

    def getRes(self):
        return self.res

    def getOp2(self):
        return self.op2

    def setInstruccion(self, instruccion):
        self.instruccion = instruccion

    def setTipo(self, tipo):
        self.tipo = tipo

    def setRt(self, id_rt):
        self.id_rt = id_rt

    def setRd(self, id_rd):
        self.id_rd = id_rd

    def setRes(self, res):
        self.res = res

    def setOp2(self, op2):
        self.op2 = op2

class Reg_MEM_WB:
    instruccion = None
    tipo = None
    id_rt = None
    id_rd = None
    res = None

    def getInstruccion(self):
        return self.instruccion

    def getTipo(self):
        return self.tipo

    def getRt(self):
        return self.id_rt

    def getRd(self):
        return self.id_rd

    def getRes(self):
        return self.res

    def setInstruccion(self, instruccion):
        self.instruccion = instruccion

    def setTipo(self, tipo):
        self.tipo = tipo

    def setRt(self, id_rt):
        self.id_rt = id_rt

    def setRd(self, id_rd):
        self.id_rd = id_rd

    def setRes(self, res):
        self.res = res

# ******************************************************************************************************
#    SIMULADOR
# ******************************************************************************************************
def ejecutaInstruccion(instruccion, registros):
    registrosNuevos = registros
    if instruccion.getOperacion() == "lw" or instruccion.getOperacion() == "sw":
        registrosNuevos[instruccion.getRt()]=registros.get(instruccion.getRs())+instruccion.getInm()
    if instruccion.getOperacion() == "add":
        registrosNuevos[instruccion.getRd()]=registros.get(instruccion.getRs())+registros.get(instruccion.getRt())
    if instruccion.getOperacion() == "sub":
        registrosNuevos[instruccion.getRd()]=registros.get(instruccion.getRs())-registros.get(instruccion.getRt())

    return registrosNuevos

def ejecutaEtapa(etapa, instruccion, registros, PC, registro ):

    if instruccion.getOperacion() == "NOP":
        return registros, registro
    if etapa == "IF":
        registro = Reg_IF_ID()
        registro.setInstruccion(instruccion)
        registro.setRs(instruccion.getRs())
        registro.setRt(instruccion.getRt())
        registro.setRd(instruccion.getRd())
        registro.setInm(instruccion.getInm())
        registro.setOperacion(instruccion.getOperacion())
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            registro.setTipo("MEM")
        else:
            registro.setTipo("ALU")
        print("  Etapa IF de I" + PC +": Mostrando contenido del registro RS_IF_ID")
        print("    Instrucción: " + registro.getInstruccion().toSring())
        print("    Tipo: " + registro.getTipo())
        print("    Operación: " + registro.getOperacion())
        print("    Rs: " + registro.getRs() + ", Rt: " + registro.getRt() +
              ", Rd: " + registro.getRd() + ", Inm: " + str(registro.getInm()))
        return registros, registro

    if etapa == "ID/OF":
        registro = Reg_ID_EX()
        registro.setInstruccion(instruccion)
        registro.setRs(instruccion.getRs())
        registro.setRt(instruccion.getRt())
        registro.setRd(instruccion.getRd())
        registro.setInm(instruccion.getInm())
        registro.setOp1(registros[instruccion.getRs()])
        registro.setOp2(registros[instruccion.getRt()])
        registro.setOperacion(instruccion.getOperacion())
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            registro.setTipo("MEM")
        else:
            registro.setTipo("ALU")
        print("  Etapa ID/OF de I" + PC +": Mostrando contenido del registro RS_ID_EX")
        print("    Instrucción: " + registro.getInstruccion().toSring())
        print("    Tipo: " + registro.getTipo())
        print("    Operación: " + registro.getOperacion())
        if registro.getTipo() == "ALU":
            print("    Rs: " + registro.getRs() + ", Rt: " + registro.getRt() + ", Rd: " + registro.getRd() +
                  ", Op1: " + str(registro.getOp1()) + ", Op2: " + str(registro.getOp2()))
        else:
            print("    Rt: " + registro.getRt() + ", Rs: " + registro.getRs() + ", Inm: " + str(registro.getInm()))
        return registros, registro

    if etapa == "EX":
        registro = Reg_EX_MEM()
        registro.setInstruccion(instruccion)
        registro.setRd(instruccion.getRd())
        registro.setRt(instruccion.getRt())
        registro.setOp2(registros[instruccion.getRt()])
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            registro.setTipo("MEM")
        else:
            registro.setTipo("ALU")
            if instruccion.getOperacion()=="add":
                almALU = int(registros[instruccion.getRs()])+int(registros[instruccion.getRt()])
                registro.setRes(almALU)
            if instruccion.getOperacion()=="sub":
                almALU = int(registros[instruccion.getRs()]) - int(registros[instruccion.getRt()])
                registro.setRes(almALU)
        print("  Etapa EX de I" + PC +": Mostrando contenido del registro RS_EX_MEM")
        print("    Instrucción: " + registro.getInstruccion().toSring())
        print("    Tipo: " + registro.getTipo())
        print("    Operación: " + instruccion.getOperacion())
        if registro.getTipo() == "ALU":
            print("    Rs: " + instruccion.getRs() + ", Rt: " + registro.getRt() + ", Rd: " + registro.getRd() +
                  ", Op1: " + str(registros[instruccion.getRs()]) + ", Op2: " + str(registro.getOp2()))
            print("    Resultado: " + str(registro.getRes()))
        else:
            print("    Rt: " + registro.getRt() + ", Rs: " + instruccion.getRs() + ", Inm: " + str(instruccion.getInm()))
        return registros, registro

    if etapa == "MEM":
        reg_EX_MEM = registro
        registro = Reg_MEM_WB()
        registro.setInstruccion(instruccion)
        registro.setRes(reg_EX_MEM.getRes())
        registro.setRd(instruccion.getRd())
        registro.setRt(instruccion.getRt())
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            registro.setTipo("MEM")
        else:
            registro.setTipo("ALU")
        print("  Etapa MEM de I" + PC +": Mostrando contenido del registro RS_MEM_WB")
        print("    Instrucción: " + registro.getInstruccion().toSring())
        print("    Tipo: " + registro.getTipo())
        print("    Operación: " + instruccion.getOperacion())
        if registro.getTipo() == "ALU":
            print("    Rs: " + instruccion.getRs() + ", Rt: " + registro.getRt() + ", Rd: " + registro.getRd() +
                  ", Op1: " + str(registros[instruccion.getRs()]) + ", Op2: " + str(registros[instruccion.getRt()]))
            print("    Resultado: " + str(registro.getRes()))
        else:
            print("    Rt: " + registro.getRt() + ", Rs: " + instruccion.getRs() + ", Inm: " + str(instruccion.getInm()))
        return registros, registro

    if etapa == "WB":
        nuevosRegistros = registros
        ejecutaInstruccion(instruccion,registros)
        print("  Etapa WB de I" + PC)
        return nuevosRegistros, registro


# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas

def cargaInstruccionesMemoria(entrada):

    instrucciones = list()

    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        if elem[0] == "lw" or elem[0] == "sw":
            elem2=elem[2].split("(")
            inm=elem2[0]
            elem3=elem2[1].split(")")
            rs=elem3[0]
            inst = Instruccion(operacion=elem[0], id_rt=elem[1], id_rs=rs, inm=inm, id_rd=" ")
        else:
            inst = Instruccion(operacion=elem[0], id_rd=elem[1], id_rs=elem[2], id_rt=elem[3], inm=0)

        if len(instrucciones) != 0:
            instAnt = instrucciones[-1]
            if instAnt.getOperacion() == "lw":
                if inst.getOperacion() == "add" or inst.getOperacion() == "sub":
                    if inst.getRt() == instAnt.getRt() or inst.getRs() == instAnt.getRt():
                        instrucciones.append(Instruccion(operacion="NOP", id_rd="0", id_rs="0", id_rt="0", inm=0))

        instrucciones.append(inst)

    return instrucciones

# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    #Cargamos en memoria las instrucciones
    entrada = [a for a in leerFichero()]
    instrucciones= cargaInstruccionesMemoria(entrada)

    #Inicializacion de los registros de segmentación
    reg_IF_ID = Reg_IF_ID()
    reg_ID_EX = Reg_ID_EX()
    reg_EX_MEM = Reg_EX_MEM()
    reg_MEM_WB = Reg_MEM_WB()

    #Inicailizamos los registros
    registros = {'r0': 0, 'r1': 1,'r2': 2,'r3': 3,'r4': 4,'r5': 5,'r6': 6,
                 'r7': 7,'r8': 8,'r9': 9,'r10': 10,'r11': 11,'r12': 12,
                 'r13': 13,'r14': 14,'r15': 15}
    registro = None
    
    #Dirección de la instrucción
    PC=0

    #Variables varias
    contInstrucciones = 0
    contCiclos = 1
    finSimulador = False


    #Imprimimos la salida del simulador -> Programa Principal <-
    print(" ")
    print("Sea un programa formado por las siguientes instrucciones: ")
    for elem in instrucciones:
        print("  " + elem.toSring())
    print(" ")
    print("Simulación ejecución: ")

    while not (finSimulador):

        print("-------------------------- Ciclo " + str(contCiclos) + ": --------------------------")

        #AQUI ESTAMOS



        registros, registro = ejecutaEtapa("IF",instrucciones[PC],registros,str(contCiclos), registro)
        registros, registro = ejecutaEtapa("ID/OF", instrucciones[PC], registros, str(contCiclos), registro)
        registros, registro = ejecutaEtapa("EX", instrucciones[PC], registros, str(contCiclos), registro)
        registros, registro = ejecutaEtapa("MEM", instrucciones[PC], registros, str(contCiclos), registro)
        registros, registro = ejecutaEtapa("WB", instrucciones[PC], registros, str(contCiclos), registro)
        PC=PC+1

        print(registros)
        finSimulador = True






