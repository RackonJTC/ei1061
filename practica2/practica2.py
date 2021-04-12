import sys

# Juego de instrucciones. Código de operación
codOperacion = ["NOP", "add", "sub", "lw", "sw", "mult"]

# Capacidad de las estructuras de almacenamiento es ilimitada pero se pone una máxima
REG = 16
DAT = 32
INS = 32

# Códigos para las UF
TOTAL_UF = 3
ALU = 0
MEM = 1
MULT = 2

# Ciclos de ejecucion de UF
CICLOS_MEM = 2
CICLOS_ALU = 1
CICLOS_MULT = 5

# Etapas de procesamiento de las instrucciones en ROB
ISS = 1
EX = 2
WB = 3

class Instruccion:
    cod = -1
    rd = -1
    rs = -1
    rt = -1
    inmediato = 0
    numInst = -1

    def __init__(self, cod, rd, rs, rt, inmediato, numInst):
        self.cod = cod
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.inmediato = inmediato
        self.numInst = numInst

    def toSring(self):
        if self.cod == 0:
            return "NOP"
        if self.cod == 4:
            return codOperacion[self.cod] + " " + "r" + str(self.rt) + ", " + str(self.inmediato) + "(" + "r" + str(
                self.rs) + ")"
        if self.cod == 3:
            return codOperacion[self.cod] + " " + "r" + str(self.rt) + ", " + str(self.inmediato) + "(" + "r" + str(
                self.rs) + ")"
        return codOperacion[self.cod] + " " + "r" + str(self.rd) + ", " + "r" + str(self.rs) + ", " + "r" + str(self.rt)


class Reg:
    contenido = 0
    ok = -1
    clk_tick_ok = -1
    TAG_ROB = -1

    def __init__(self, contenido, ok, clk_tick_ok, TAG_ROB):
        self.contenido = contenido
        self.ok = ok
        self.clk_tick_ok = clk_tick_ok
        self.TAG_ROB = TAG_ROB


class ER:
    linea_valida = -1
    TAG_ROB = -1
    operacion = -1
    opa = -1
    opa_ok = -1
    clk_tick_ok_a = -1
    opb = -1
    opb_ok = -1
    clk_tick_ok_b = -1
    inmediato = -1

    def __init__(self, linea_valida, TAG_ROB, operacion, opa, opa_ok, clk_tick_ok_a, opb, opb_ok, clk_tick_ok_b,
                 inmediato):
        self.linea_valida = linea_valida
        self.TAG_ROB = TAG_ROB
        self.operacion = operacion
        self.opa = opa
        self.opa_ok = opa_ok
        self.clk_tick_ok_a = clk_tick_ok_a
        self.opb = opb
        self.opb_ok = opb_ok
        self.clk_tick_ok_b = clk_tick_ok_b
        self.inmediato = inmediato


class ROB:
    TAG_ROB = -1
    linea_valida = -1
    destino = -1
    valor = -1
    clk_tick_ok = -1
    etapa = -1

    def __init__(self, TAG_ROB, linea_valida, destino, valor, clk_tick_ok, etapa):
        self.TAG_ROB = TAG_ROB
        self.linea_valida = linea_valida
        self.destino = destino
        self.valor = valor
        self.clk_tick_ok = clk_tick_ok
        self.etapa = etapa


class UF:  # Unidad funcional
    uso = -1
    cont_ciclos = -1
    TAG_ROB = -1
    opa = -1
    opb = -1
    operacion = -1
    res = -1
    res_ok = -1
    clk_tick_ok = -1

    def __init__(self, uso, cont_ciclos, TAG_ROB, opa, opb, operacion, res, res_ok, clk_tick_ok):
        self.uso = uso
        self.cont_ciclos = cont_ciclos
        self.TAG_ROB = TAG_ROB
        self.opa = opa
        self.opb = opb
        self.operacion = operacion
        self.res = res
        self.res_ok = res_ok
        self.clk_tick_ok = clk_tick_ok


# ******************************************************************************************************
#    ETAPAS
# ******************************************************************************************************

# def etapa_commit(instruccion):
#
#     #Retirar la instrucción contenida en ROB y apuntada por p_rob_cabeza si se ha ejecutado su etapa WB
#     # en un ciclo anterior. En otro caso no hace nada
#
#


# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas


def cargaInstruccionesMemoria(entrada):
    instrucciones = list()
    i = 1
    cod = -1
    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        if elem[0] == "add":
            cod = 1
        if elem[0] == "sub":
            cod = 2
        if elem[0] == "lw":
            cod = 3
        if elem[0] == "sw":
            cod = 4
        if elem[0] == "mult":
            cod = 5
        if cod == 3 or cod == 4:
            elem2 = elem[2].split("(")
            inm = int(elem2[0])
            elem3 = elem2[1].split(")")
            rs = int(elem3[0][1])
            inst = Instruccion(cod=cod, rt=int(elem[1][1]), rs=rs, inmediato=inm, rd=-1, numInst=i)
        else:
            inst = Instruccion(cod=cod, rd=int(elem[1][1]), rs=int(elem[2][1]), rt=int(elem[3][1]), inmediato=0,
                               numInst=i)

        if len(instrucciones) != 0:
            instAnt = instrucciones[-1]
            if instAnt.cod == 3:
                if inst.cod == 1 or inst.cod == 2:
                    if inst.rt == instAnt.rt or inst.rs == instAnt.rt:
                        instrucciones.append(
                            Instruccion(cod=0, rd=0, rs=0, rt=0, inmediato=0, numInst=i))

        instrucciones.append(inst)
        i += 1

    return instrucciones, i


# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    # Cargamos en memoria las instrucciones
    entrada = [a for a in leerFichero()]
    instrucciones, acaba = cargaInstruccionesMemoria(entrada)

    for elem in instrucciones:
        print(elem.toSring())

    # Registros
    banco_registros = [Reg(0,0,0,0)] * REG

    # Memoria de datos
    memDatos = [a for a in range(0, DAT)]

    # Memoria de instrucciones
    instrucciones = [a for a in range(0, INS)]

    # Inicializamos las Unidades Funcionales
    UnidadesFuncionales = [UF(0,0,0,0,0,0,0,0,0)] * TOTAL_UF

    # Inicializamos las Estaciones de Reserva (Cada unidad funcional tiene una)
    EstacionesDeReserva = [ER(0,0,0,0,0,0,0,0,0,0)] * TOTAL_UF

    #Inicializamos el ROB
    BufferReordenamiento = [ROB(0,0,0,0,0,0)] * INS

    inst_prog = len(instrucciones) #total instrucciones programa
    inst_rob = 0 #instrucciones en rob

    p_rob_cabeza, p_rob_cola = 0, 0 # puntero a las posiciones de rob para introducir (cola) o retirar instrucciones (cabeza)
    PC = 0 # puntero a memoria de instrucciones, siguiente instrucción a IF
    p_er_cola = [0,0,0] #vector de punteros que apuntan a la cola de cada una de las UF

    # ******************************************************************************************************
    #    SIMULADOR
    # ******************************************************************************************************

    ciclos = 1
    i=0
    # while(inst_rob > 0 or inst_prog > 0):
    #

    # ISS = 1  EX = 2  WB = 3
def Etapa_COMMIT():
    if BufferReordenamiento[p_rob_cabeza].linea_valida == 1 and BufferReordenamiento[p_rob_cabeza].etapa == 3:
        id_reg = BufferReordenamiento[p_rob_cabeza].destino
        banco_registros[id_reg].contenido = BufferReordenamiento[p_rob_cabeza].valor
        banco_registros[id_reg].ok = 1
        banco_registros[id_reg].clk_tick_ok = ciclos+1

    BufferReordenamiento[p_rob_cabeza] = ROB(0,0,0,0,0,0)







