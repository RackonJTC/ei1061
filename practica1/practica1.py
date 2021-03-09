import sys

# DATOS
# Simulador de un procesador segmentado de 5 etapas (IF,ID/OF, EX, MEM, WB).
# 16 registros para numeros de 32 bits de r0 a r15
# Memoria con capacidad para 32 instrucciones de 32 bits, desde 0 a 31
# Memoria de datos con capacidad para 31 numeros de 32 bits, desde 0 a 31

class Instruccion:
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
        return self.inm

    def toSring(self):
        if self.operacion=="NOP":
            return "NOP"
        if self.operacion=="sw":
            return self.operacion + " " + self.id_rs + ", " + self.id_rt
        if self.operacion=="lw":
            return self.operacion + " " + self.id_rd + ", " + self.id_rs
        return self.operacion + " " + self.id_rd + ", " + self.id_rs + ", " + self.id_rt

class Reg_IF_ID:
    instruccion = None
    tipo = None
    operacion = None
    id_rs = None
    id_rt = None
    id_rd = None
    inmediato = None

    def __init__(self, instruccion, tipo, operacion, id_rs, id_rt, id_rd, inm):
        self.instruccion = instruccion
        self.tipo = tipo
        self.operacion = operacion
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.inm = inm

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

    def __init__(self, instruccion, tipo, operacion, id_rs, id_rt, id_rd, inm, op1, op2):
        self.instruccion = instruccion
        self.tipo = tipo
        self.operacion = operacion
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.inm = inm
        self.op1 = op1
        self.op2 = op2

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

    def __init__(self, instruccion, tipo, id_rt, id_rd, res, op2):
        self.instruccion = instruccion
        self.tipo = tipo
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.res= res
        self.op2 = op2

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

    def __init__(self, instruccion, tipo, id_rt, id_rd, res, op2):
        self.instruccion = instruccion
        self.tipo = tipo
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.res= res
        self.op2 = op2

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
def ejecutaInstruccion(self, instruccion):
    registros = {'r0': None, 'r1': None,'r2': None,'r3': None,'r4': None,'r5': None,'r6': None,
                 'r7': None,'r8': None,'r9': None,'r10': None,'r11': None,'r12': None,
                 'r13': None,'r14': None,'r15': None,}
    operaciones = ["lw", "sw", "add", "sub"]



# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas

def crearInstrucciones(entrada):

    instrucciones = list()

    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        if elem[0] == "lw":
            inst = Instruccion(operacion=elem[0], id_rd=elem[1], id_rs=elem[2], inm=elem[2], id_rt=" ")
        elif elem[0] == "sw":
            inst = Instruccion(operacion=elem[0], id_rt=elem[2], id_rs=elem[1], inm=elem[2], id_rd=" ")
        else:
            inst = Instruccion(operacion=elem[0], id_rd=elem[1], id_rs=elem[2], id_rt=elem[3], inm=" ")

        if len(instrucciones) != 0:
            instAnt = instrucciones[-1]
            if instAnt.getOperacion() == "lw":
                if inst.getOperacion() == "add" or inst.getOperacion() == "sub":
                    if inst.getRt() == instAnt.getRd() or inst.getRs() == instAnt.getRd():
                        instrucciones.append(Instruccion(operacion="NOP", id_rd=" ", id_rs=" ", id_rt=" ", inm=" "))

        instrucciones.append(inst)

    return instrucciones

# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    entrada = [a for a in leerFichero()]
    instrucciones= crearInstrucciones(entrada)

    print(" ")
    print("Sea un programa formado por las siguientes instrucciones: ")
    for elem in instrucciones:
        print("  " + elem.toSring())
    print(" ")
    print("Simulación ejecución: ")
    i=1
    print("  Ciclo " + str(i) + ":")


