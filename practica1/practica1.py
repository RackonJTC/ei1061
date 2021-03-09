import sys

# DATOS
# Simulador de un procesador segmentado de 5 etapas (IF,ID/OF, EX, MEM, WB).
# 16 registros para numeros de 32 bits de r0 a r15
# Memoria con capacidad para 32 instrucciones de 32 bits, desde 0 a 31
# Memoria de datos con capacidad para 31 numeros de 32 bits, desde 0 a 31

class instruccion:
    operaciones = ["lw", "sw", "add", "sub"]

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




# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas

# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    entrada = [a for a in leerFichero()]
    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        print(elem)



    # registros = [0] * 16
    # memInstrucciones = [None] * 32
    # memDatos = [None] * 32
    #
    #
    # def IF():
    #     pass
    #
    #
    # def ID():
    #     pass
    #
    #
    # def EX():
    #     pass
    #
    #
    # def MEM():
    #     pass
    #
    #
    # def WB():
    #     pass
