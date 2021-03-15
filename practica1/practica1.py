import sys

# DATOS
# Simulador de un procesador segmentado de 5 etapas (IF,ID/OF, EX, MEM, WB).
# 16 registros para numeros de 32 bits de r0 a r15
# Memoria con capacidad para 32 instrucciones de 32 bits, desde 0 a 31
# Memoria de datos con capacidad para 31 numeros de 32 bits, desde 0 a 31

# Memoria de instrucciones
instrucciones = [a for a in range(0,32)]

# Memoria de datos
datos = [a for a in range(0,32)]

# ******************************************************************************************************
#    CLASES PARA INSTRUCCIONES Y REGISTROS DE SEGMENTACIÓN
# ******************************************************************************************************

class Instruccion:  # add rd=r4 rs=r0 rt=r3
    operacion, id_rd, id_rs, id_rt, tipo, inm, res, numInst = "","","","","",0,0,0

    def __init__(self, operacion, id_rd, id_rs, id_rt, inm, numInst):
        self.operacion = operacion
        self.id_rd = id_rd
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.inm = inm
        self.numInst = numInst
        self.res = 0

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

    def getNumInst(self):
        return int(self.numInst)

    def setRes(self, res):
        self.res = res

    def setTipo(self, tipo):
        self.tipo = tipo

    def getRes(self):
        return int(self.res)

    def getTipo(self):
        return self.tipo

    def toSring(self):
        if self.operacion == "NOP":
            return "NOP"
        if self.operacion == "sw":
            return self.operacion + " " + self.id_rt + ", " + self.inm + "(" + self.id_rs + ")"
        if self.operacion == "lw":
            return self.operacion + " " + self.id_rt + ", " + self.inm + "(" + self.id_rs + ")"
        return self.operacion + " " + self.id_rd + ", " + self.id_rs + ", " + self.id_rt

class Reg_IF_ID:

    instruccion, tipo, operacion, id_rs, id_rt, id_rd, inmediato = "","", "", "", "", "", 0

    def __init__(self, instruccion, tipo, operacion, id_rs, id_rt, id_rd, inmediato):
        self.instruccion = instruccion
        self.tipo = tipo
        self.operacion = operacion
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.inmediato = inmediato

    def getTipo(self):
        return self.tipo

    def getInstruccion(self):
        return self.instruccion

class Reg_ID_EX:

    instruccion, tipo, operacion, id_rs, id_rt, id_rd, inmediato, op1, op2 = "","", "", "", "", "", 0, 0, 0

    def __init__(self, instruccion, tipo, operacion, id_rs, id_rt, id_rd, inmediato, op1, op2):
        self.instruccion = instruccion
        self.tipo = tipo
        self.operacion = operacion
        self.id_rs = id_rs
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.inmediato = inmediato
        self.op1 = op1
        self.op2 = op2

    def getTipo(self):
        return self.tipo

    def getInstruccion(self):
        return self.instruccion

class Reg_EX_MEM:

    instruccion, tipo, id_rt, id_rd, operacion, res, op2 = "","","","","",0,0

    def __init__(self, instruccion, tipo, id_rt, id_rd, operacion, res, op2):
        self.instruccion = instruccion
        self.tipo = tipo
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.operacion = operacion
        self.res = res
        self.op2 = op2

    def getTipo(self):
        return self.tipo

    def getInstruccion(self):
        return self.instruccion

class Reg_MEM_WB:

    instruccion, tipo, id_rt, id_rd, res = "","","","",0

    def __init__(self, instruccion, tipo, id_rt, id_rd, res):
        self.instruccion = instruccion
        self.tipo = tipo
        self.id_rt = id_rt
        self.id_rd = id_rd
        self.res = res

    def getTipo(self):
        return self.tipo

    def getInstruccion(self):
        return self.instruccion

# ******************************************************************************************************
#    SIMULADOR
# ******************************************************************************************************

def ejecutaEtapa(etapa, instruccion, registros):

    if instruccion.getOperacion() == "NOP":
        return registros, instruccion

    if etapa == "IF":
        rs=instruccion.getRs()
        rt=instruccion.getRt()
        rd=instruccion.getRd()
        inm=instruccion.getInm()
        op=instruccion.getOperacion()
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            tipo="MEM"
        else:
            tipo="ALU"
        instruccion.setTipo(tipo)
        print("  Etapa IF de I" + str(instruccion.getNumInst()) + ": \n   >> Mostrando contenido del registro RS_IF_ID")
        print("       >> Instrucción: " + instruccion.toSring(), end=" | ")
        print("Tipo: " + tipo, end=" | ")
        print("Operación: " + op, end=" | ")
        print("Rs: " + rs + " | Rt: " + rt + " | Rd: " + rd + " | Inm: " + str(inm))
        return registros, instruccion

    if etapa == "ID/OF":
        rs=instruccion.getRs()
        rt=instruccion.getRt()
        rd=instruccion.getRd()
        inm=instruccion.getInm()
        op1=registros[instruccion.getRs()]
        op2=registros[instruccion.getRt()]
        op=instruccion.getOperacion()
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            tipo="MEM"
        else:
            tipo="ALU"
        instruccion.setTipo(tipo)
        print("  Etapa ID/OF de I" + str(instruccion.getNumInst()) + ": \n   >> Mostrando contenido del registro RS_ID_EX")
        print("       >> Instrucción: " + instruccion.toSring(), end=" | ")
        print("Tipo: " + tipo, end=" | ")
        print("Operación: " + op, end=" | ")
        if tipo == "ALU":
            print("Rs: " + rs + " | Rt: " + rt + " | Rd: " + rd + " | Op1: " + str(op1) + " | Op2: " + str(op2))
        else:
            print("Rt: " + rt + " | Rs: " + rs + " | Inm: " + str(inm))
        return registros, instruccion

    if etapa == "EX":
        rd=instruccion.getRd()
        rt=instruccion.getRt()
        op2=registros[instruccion.getRt()]
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            tipo="MEM"
        else:
            tipo="ALU"
            if instruccion.getOperacion() == "add":
                res = int(registros[instruccion.getRs()]) + int(registros[instruccion.getRt()])
                instruccion.setRes(res)
            if instruccion.getOperacion() == "sub":
                res = int(registros[instruccion.getRs()]) - int(registros[instruccion.getRt()])
                instruccion.setRes(res)
        instruccion.setTipo(tipo)
        print("  Etapa EX de I" + str(instruccion.getNumInst()) + ": \n   >> Mostrando contenido del registro RS_EX_MEM")
        print("       >> Instrucción: " + instruccion.toSring(), end=" | ")
        print("Tipo: " + tipo, end=" | ")
        print("Operación: " + instruccion.getOperacion(), end=" | ")
        if tipo == "ALU":
            print("Rs: " + instruccion.getRs() + " | Rt: " + rt + " | Rd: " + rd +
                  " | Op1: " + str(registros[instruccion.getRs()]) + " | Op2: " + str(op2), end=" | ")
            print("Resultado: " + str(res))
        else:
            print(
                "Rt: " + rt + " | Rs: " + instruccion.getRs() + " | Inm: " + str(instruccion.getInm()))
        return registros, instruccion

    if etapa == "MEM":
        rd=instruccion.getRd()
        rt=instruccion.getRt()
        op2=registros[instruccion.getRt()]
        if instruccion.getOperacion() == "sw" or instruccion.getOperacion() == "lw":
            tipo="MEM"
        else:
            tipo="ALU"
        instruccion.setTipo(tipo)
        print("  Etapa MEM de I" + str(instruccion.getNumInst()) + ": \n   >> Mostrando contenido del registro RS_MEM_WB")
        print("       >> Instrucción: " + instruccion.toSring(), end=" | ")
        print("Tipo: " + tipo, end=" | ")
        print("Operación: " + instruccion.getOperacion(), end=" | ")
        if tipo == "ALU":
            print("Rs: " + instruccion.getRs() + " | Rt: " + rt + " | Rd: " + rd +
                  " | Op1: " + str(registros[instruccion.getRs()]) + " | Op2: " + str(op2), end=" | ")
            print("Resultado: " + str(instruccion.getRes()))
        else:
            print(
                "Rt: " + rt + " | Rs: " + instruccion.getRs() + " | Inm: " + str(instruccion.getInm()))
        return registros, instruccion

    if etapa == "WB":
        nuevosRegistros = registros
        ejecutaInstruccion(instruccion, registros)
        print("  Etapa WB de I" + str(instruccion.getNumInst()))
        return nuevosRegistros, instruccion

def ejecutaInstruccion(instruccion, registros):
    registrosNuevos = registros
    if instruccion.getOperacion() == "lw":
        registrosNuevos[instruccion.getRt()] = registros.get(instruccion.getRs()) + instruccion.getInm()
    if instruccion.getOperacion() == "sw":
        registrosNuevos[instruccion.getRs()] = registros[instruccion.getRt()]
    if instruccion.getOperacion() == "add":
        registrosNuevos[instruccion.getRd()] = registros.get(instruccion.getRs()) + registros.get(instruccion.getRt())
    if instruccion.getOperacion() == "sub":
        registrosNuevos[instruccion.getRd()] = registros.get(instruccion.getRs()) - registros.get(instruccion.getRt())

    return registrosNuevos

# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas

def cargaInstruccionesMemoria(entrada):
    instrucciones = list()
    i=1
    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        if elem[0] == "lw" or elem[0] == "sw":
            elem2 = elem[2].split("(")
            inm = elem2[0]
            elem3 = elem2[1].split(")")
            rs = elem3[0]
            inst = Instruccion(operacion=elem[0], id_rt=elem[1], id_rs=rs, inm=inm, id_rd=" ", numInst=i)
        else:
            inst = Instruccion(operacion=elem[0], id_rd=elem[1], id_rs=elem[2], id_rt=elem[3], inm=0,numInst=i)

        if len(instrucciones) != 0:
            instAnt = instrucciones[-1]
            if instAnt.getOperacion() == "lw":
                if inst.getOperacion() == "add" or inst.getOperacion() == "sub":
                    if inst.getRt() == instAnt.getRt() or inst.getRs() == instAnt.getRt():
                        instrucciones.append(Instruccion(operacion="NOP", id_rd="0", id_rs="0", id_rt="0", inm=0, numInst=i))
                        instrucciones.append(Instruccion(operacion="NOP", id_rd="0", id_rs="0", id_rt="0", inm=0, numInst=i))

        instrucciones.append(inst)
        i += 1

    instrucciones.append(Instruccion(operacion="ACABAR", id_rd="0", id_rs="0", id_rt="0", inm=0, numInst=0))

    return instrucciones

# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    # Cargamos en memoria las instrucciones
    entrada = [a for a in leerFichero()]
    instrucciones = cargaInstruccionesMemoria(entrada)

    # Inicializacion de los registros de segmentación
    reg_IF_ID = Reg_IF_ID("","","","","","",0)
    reg_ID_EX = Reg_ID_EX("","","","","","",0,0,0)
    reg_EX_MEM = Reg_EX_MEM("","","","","",0,0)
    reg_MEM_WB = Reg_MEM_WB("","","","",0)

    # Inicailizamos los registros
    registros = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4, 'r5': 5, 'r6': 6,
                 'r7': 7, 'r8': 8, 'r9': 9, 'r10': 10, 'r11': 11, 'r12': 12,
                 'r13': 13, 'r14': 14, 'r15': 15}
    registro = ""

    # Dirección de la instrucción
    PC = 0

    # Variables varias
    contCiclos = 1
    continuaSimulador = True

    # Imprimimos la salida del simulador -> Programa Principal <-
    print(" ")
    print("Sea un programa formado por las siguientes instrucciones: ")
    for elem in instrucciones[:-1]:
        print("  " + elem.toSring())
    print(" ")
    print("Simulación ejecución: ")

    while (continuaSimulador):

        # ******************************************************************************************************
        #    PROCESO DE DETECCIÓN DE RIESGOS
        # ******************************************************************************************************

        # LOAD + ALU
        if (reg_ID_EX.id_rs == reg_EX_MEM.id_rt and reg_ID_EX.getTipo() == "ALU" and reg_EX_MEM.operacion == "lw"):
            contCiclos += 1
            reg_ID_EX.op1 = reg_EX_MEM.res
            # print("HELLO BUENAS")
        if (reg_ID_EX.id_rt == reg_EX_MEM.id_rt and reg_ID_EX.getTipo() == "ALU" and reg_EX_MEM.operacion == "lw"):
            contCiclos += 1
            reg_ID_EX.op2 = reg_EX_MEM.res
            # print("HELLO BUENAS")

        # ALU + ALU
        if (reg_ID_EX.id_rs == reg_EX_MEM.id_rd and reg_EX_MEM.getTipo() == "ALU" and reg_ID_EX.getTipo() == "ALU"):
            reg_ID_EX.op1 = reg_EX_MEM.res
            # print("HELLO BUENAS2")
        if (reg_ID_EX.id_rt == reg_EX_MEM.id_rd and reg_EX_MEM.getTipo() == "ALU" and reg_ID_EX.getTipo() == "ALU"):
            reg_ID_EX.op2 = reg_EX_MEM.res
            # print("HELLO BUENAS2")

        # ALU + INSTRUCCIÓN + ALU
        if (reg_ID_EX.id_rs == reg_MEM_WB.id_rd and reg_MEM_WB.getTipo() == "ALU" and reg_ID_EX.getTipo() == "ALU"):
            reg_ID_EX.op1 = reg_MEM_WB.res
            # print("HELLO BUENAS3")
        if (reg_ID_EX.id_rt == reg_MEM_WB.id_rd and reg_MEM_WB.getTipo() == "ALU" and reg_ID_EX.getTipo() == "ALU"):
            reg_ID_EX.op2 = reg_MEM_WB.res
            # print("HELLO BUENAS3")

        # ALU + STORE
        if (reg_EX_MEM.id_rt == reg_MEM_WB.id_rd and reg_EX_MEM.operacion == "sw" and reg_MEM_WB.getTipo() == "ALU"):
            reg_EX_MEM.op2 = reg_MEM_WB.res
            # print("HELLO BUENAS4")


        # ******************************************************************************************************
        #    PROCESO DE SEGMENTACIÓN
        # ******************************************************************************************************

        print("-------------------------- Ciclo " + str(contCiclos) + ": --------------------------")
        if (reg_MEM_WB.getTipo() != ""):
            ejecutaEtapa("WB",reg_MEM_WB.getInstruccion(),registros)
            reg_MEM_WB = Reg_MEM_WB("","","","",0)

        if (reg_EX_MEM.getTipo() != ""):
            registros, instruccion = ejecutaEtapa("MEM",reg_EX_MEM.getInstruccion(),registros)
            reg_MEM_WB = Reg_MEM_WB(instruccion,instruccion.getTipo(),instruccion.getRt(),instruccion.getRd(),instruccion.getRes())

            reg_EX_MEM = Reg_EX_MEM("","","","","",0,0)
        if (reg_ID_EX.getTipo() != ""):
            registros, instruccion = ejecutaEtapa("EX",reg_ID_EX.getInstruccion(),registros)
            reg_EX_MEM = Reg_EX_MEM(instruccion,instruccion.getTipo(),instruccion.getRt(),instruccion.getRd(),
                                    instruccion.getOperacion(),instruccion.getRes(),registros[instruccion.getRt()])
            reg_ID_EX = Reg_ID_EX("","","","","","",0,0,0)

        if (reg_IF_ID.getTipo() != ""):
            registros, instruccion = ejecutaEtapa("ID/OF",reg_IF_ID.getInstruccion(),registros)
            reg_ID_EX = Reg_ID_EX(instruccion,instruccion.getTipo(),instruccion.getOperacion(),instruccion.getRs(),instruccion.getRt(),
                                  instruccion.getRd(),instruccion.getInm(),registros[instruccion.getRs()],registros[instruccion.getRt()])
            reg_IF_ID = Reg_IF_ID("","","","","","",0)

        if (instrucciones[PC].getOperacion() != "ACABAR"):  # Introduce instruccion al cauce
            registros, instruccion = ejecutaEtapa("IF", instrucciones[PC], registros)
            reg_IF_ID = Reg_IF_ID(instruccion,instruccion.getTipo(),instruccion.getOperacion(),instruccion.getRs(),
                                  instruccion.getRt(),instruccion.getRd,instruccion.getInm())
            PC += 1

        continuaSimulador = reg_IF_ID.getInstruccion() != "" or reg_ID_EX.getInstruccion() != "" \
                       or reg_EX_MEM.getInstruccion() != "" or reg_MEM_WB.getInstruccion() != ""
        contCiclos += 1

    print("")
    print("Ciclos totales: " + str(contCiclos-1))
    print("")
    print("Contenido de la Memoria de datos")
    for i in range(12):
        print("MD[" + str(i) + "] = " + str(datos[i]), end=" | ")
    print("")
    for i in range(10):
        print("MD[" + str(i+12) + "] = " + str(datos[i+12]), end=" | ")
    print("")
    for i in range(10):
        print("MD[" + str(i+22) + "] = " + str(datos[i+22]), end=" | ")
    print("")
    print("")
    print("Contenido del Banco de registros:")
    for elem in registros:
        print(str(elem) + " = " + str(registros[elem]), end=" | ")
    print("")

