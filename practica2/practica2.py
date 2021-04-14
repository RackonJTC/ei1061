import sys

# ******************************************************************************************************
#    DEFINICIONES
# ******************************************************************************************************

# Juego de instrucciones. Código de operación
codOperacion = ["NOP", "add", "sub", "lw", "sw", "mult"]

# Capacidad de las estructuras de almacenamiento es ilimitada pero se pone una máxima
REG = 16
DAT = 32
INS = 32

# Códigos para las UF_class
TOTAL_UF = 3
ALU = 0
MEM = 1
MULT = 2

# Ciclos de ejecucion de UF_class
CICLOS_MEM = 2
CICLOS_ALU = 1
CICLOS_MULT = 5

# Etapas de procesamiento de las instrucciones en ROB_class
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

    def __str__(self) -> str:
        cadena = str(self.contenido) + "\t" + str(self.ok) + "\t" + str(self.clk_tick_ok) + "\t" + str(self.TAG_ROB)
        return cadena


class ER_class:
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

    def __str__(self) -> str:
        cadena = str(self.linea_valida) + "\t" + str(self.TAG_ROB) + "\t" + str(self.operacion) + "\t" + str(self.opa)\
        + "\t" + str(self.opa_ok) + "\t" + str(self.clk_tick_ok_a) + "\t" + str(self.opb) + "\t" + str(self.opb_ok)\
        + "\t" + str(self.clk_tick_ok_b) + "\t" + str(self.inmediato)
        return cadena


class ROB_class:
    TAG_ROB = -1
    linea_valida = -1
    destino = -1
    valor = -1
    valor_ok = -1
    clk_tick_ok = -1
    etapa = -1

    def __init__(self, TAG_ROB, linea_valida, destino, valor, valor_ok, clk_tick_ok, etapa):
        self.TAG_ROB = TAG_ROB
        self.linea_valida = linea_valida
        self.destino = destino
        self.valor = valor
        self.valor_ok = valor_ok
        self.clk_tick_ok = clk_tick_ok
        self.etapa = etapa

    def __str__(self) -> str:
        cadena = str(self.TAG_ROB) + "\t" + str(self.linea_valida) + "\t" + str(self.destino) + "\t" + str(self.valor)\
        + "\t" + str(self.valor_ok) + "\t" + str(self.clk_tick_ok) + "\t" + str(self.etapa)
        return cadena


class UF_class:  # Unidad funcional
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

# ISS = 1  EX = 2  WB = 3
def Etapa_COMMIT(listaDatos):

    BR, MD, MI, UF, ER, ROB, Var = listaDatos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola = Var

    if ROB[p_rob_cabeza].linea_valida == 1 and ROB[p_rob_cabeza].etapa == 3:
        id_reg = ROB[p_rob_cabeza].destino
        BR[id_reg].contenido = ROB[p_rob_cabeza].valor
        BR[id_reg].ok = 1
        BR[id_reg].clk_tick_ok = ciclo + 1

    ROB[p_rob_cabeza] = ROB_class(0, 0, 0, 0, 0, 0, 0)

    Var = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola]
    listaDatos = [BR, MD, MI, UF, ER, ROB, Var]
    return listaDatos


def Etapa_WB(listaDatos):

    BR, MD, MI, UF, ER, ROB, Var = listaDatos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola = Var

    i = 0
    bucle = 0
    while bucle == 0 and i < TOTAL_UF:
        if UF[i].uso == 1 and UF[i].res_ok == 1 and UF[i].clk_tick_ok <= ciclo:
            # Se actualiza ROB
            id = UF[i].TAG_ROB
            ROB[UF[i].TAG_ROB].valor = UF[i].res
            ROB[UF[i].TAG_ROB].valor_ok = 1
            ROB[UF[i].TAG_ROB].clk_tick_ok = ciclo + 1
            ROB[id].etapa = WB
            # Se deja libre la UF
            UF[i] = UF_class(0, 0, 0, 0, 0, 0, 0, 0, 0)

            # se ha escrito un dato. No se pueden escribir más.
            bucle = 1

            k, j = 0, 0
            for k in range(TOTAL_UF):
                fin = p_er_cola[k]
                for j in range(fin):
                    # Si el operando depende de ese resultado
                    if ER_class[k][j].linea_valida == 1:  # Si la linea es valida
                        if ER[k][j].opa_ok == 0 and ER[k][j].opa == id:  # Si opa no disponible y depende de TAG_ROB
                            ER[k][j].opa \
                                = UF[i].res
                            ER[k][j].opa_ok = 1
                            ER[k][j].clk_tick_ok_a = ciclo + 1
                        if ER[k][j].opb_ok == 0 and ER[k][j].opb == id:  # Si opb depende de ese resultado
                            ER[k][j].opb = UF[i].res
                            ER[k][j].opb_ok = 1
                            ER[k][j].clk_tick_ok_b = ciclo + 1
                    j += 1
                k += 1
        else:
            i += 1

    Var = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola]
    listaDatos = [BR, MD, MI, UF, ER, ROB, Var]
    return listaDatos


def Etapa_EX(listaDatos):

    BR, MD, MI, UF, ER, ROB, Var = listaDatos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola = Var

    i = 0
    enviar = 0
    while i < TOTAL_UF:
        uf_ = UF[i]
        max = -1
        # Establecer cilos máximos para cada UF
        if i == 0:
            max = CICLOS_ALU
        elif i == 1:
            max = CICLOS_MEM
        elif i == 2:
            max = CICLOS_MULT

        if uf_.uso == 1:  # si está en uso, se incrementa el ciclo y no se pueden enviar otra instrucción.
            if uf_.cont_ciclos < max:
                uf_.cont_ciclos = uf_.cont_ciclos + 1  # incrementar el ciclo

                if uf_.cont_ciclos == max:  # si se ha finalizado la operación generar resultado y validarlo. uf_.operacion
                    # codOperacion = ["NOP", "add", "sub", "lw", "sw", "mult"]
                    if uf_.operacion == 1:
                        UF[i].res = UF[i].opa + UF[i].opb
                    elif uf_.operacion == 2:
                        UF[i].res = UF[i].opa - UF[i].opb
                    # ME FALTA LW Y SW *********************************************************************************************************************
                    elif uf_.operacion == 5:
                        UF[i].res = UF[i].opa * UF[i].opb

                    UF.res_ok = 1
                    UF[i].clk_tick_ok = ciclo + 1
        elif enviar == 0:
            er_ = ER[i]
            fin = p_er_cola[i]  # última línea insertada
            j = 0  # contador de líneas de ER[i] desde 0 hasta fin
            while enviar == 0 and j < fin:
                if er_[j].linea_valida == 1:
                    if er_[j].opa_ok == 1 and er_[j].clk_tick_ok_a <= ciclo and er_[j].opb_ok == 1 and er_[j].clk_tick_ok_b <= ciclo:
                        # enviar operación a ejecutar a UF actualizando UF[i] con los datos necesarios e inicializar ciclo
                        # No entiendo lo de enviar ****************************************************************************************************************
                        ER[i].TAG_ROB = 2  # Actualizar en etapa en ROB a EX
                        enviar = 1
                else:
                    j += 1
        i += 1

    Var = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola]
    listaDatos = [BR, MD, MI, UF, ER, ROB, Var]
    return listaDatos


def Etapa_ID_ISS(listaDatos):

    BR, MD, MI, UF, ER, ROB, Var = listaDatos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola = Var

    if inst_prog > 0:
        inst = MI[PC]
        linea_aux = ER_class(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        # Actualizamos linea
        linea_aux.linea_valida = 1
        linea_aux.operacion = inst.cod

        if BR[inst.rs].ok == 1:
            linea_aux.opa = BR[inst.rs].contenido
            linea_aux.opa_ok = 1
        else:
            linea_aux.opa = BR[inst.rs].TAG_ROB
            linea_aux.opa_ok = 0
        if BR[inst.rt].ok == 1:
            linea_aux.opb = BR[inst.rt].contenido
            linea_aux.opb_ok = 1
        else:
            linea_aux.opb = BR[inst.rs].TAG_ROB
            linea_aux.opb_ok = 0

        linea_aux.inmediato = inst.inmediato

        # codOperacion = ["NOP", "add", "sub", "lw", "sw", "mult"]
        # Códigos para las UF_class  TOTAL_UF = 3  ALU = 0  MEM = 1  MULT = 2

        tipo = -1
        # Insertar línea_aux en la ER correspondiente
        if inst.cod == 1 or inst.cod == 2:
            tipo = 0
        elif inst.cod == 3 or inst.cod == 4:
            tipo = 1
        elif inst.cod == 5:
            tipo = 2

        linea = p_er_cola[tipo]
        # print(linea)
        # print(ER[tipo])
        # ER[tipo][linea] = linea_aux
        p_er_cola[tipo] += 1

        # Añadir instrucción en ROB y actualizar todos sus campos. Posición apuntada por p_rob_cola
        # si instrucción es sw poner en el campo destino un 0 para identificar que no se escribe nada en etapa commit
        # ROB -> def __init__(self, TAG_ROB, linea_valida, destino, valor, valor_ok, clk_tick_ok, etapa):
        #ROB[p_rob_cola] = ROB  # ************************************************************************************************DUDA CON clk_tick_ok
        ROB[p_rob_cola]=ROB_class(TAG_ROB=p_rob_cola,linea_valida=1,destino=0,valor=0,valor_ok=0,clk_tick_ok=-1,etapa=ISS)
        if inst.cod == 4:
            ROB[p_rob_cola].destino = 0
        else:
            ROB[p_rob_cola].destino = inst.rd

        p_rob_cola += 1

        # Invalidar el registro destino de esta instrucción
        BR[inst.rd].ok = 0
        BR[inst.rd].TAG_ROB = p_rob_cola

        # Actualiza PC + 1 y inst_prog - 1
        PC += 1
        inst_prog = inst_prog - 1

    Var = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola]
    listaDatos = [BR, MD, MI, UF, ER, ROB, Var]
    return listaDatos


# ******************************************************************************************************
#    METODOS MOSTRAR CONTENIDO
# ******************************************************************************************************
def Mostrar_ER(ER):
    nombresEstaciones=["ALU","MEM","MULT"]
    print("*** ESTACIONES DE RESERVA ***************************************")
    print("\t\tl_val\tTGROB\toper\topa\topa_ok\tcA_ok\topb\topb_ok\tcB_ok\tinmed")
    for i in range(len(ER)):
        for j in range(len(ER[i])):
            print("ER " + nombresEstaciones[i] + " " + str(j) + ":\t" + ER[i][j].__str__())


def Mostrar_ROB(ROB):
    print("*** BUFFER DE REORDENAMIENTO ************************************")
    print("\tTAG\tlinVal\tdest\tvalor\tv_ok\tclk_ok\tetapa")
    for i in range(len(ROB)):
        print("ROB" + str(i) + ":\t" + ROB[i].__str__())

def Mostar_Banco_Registros(BR):
    print("*** BANCO DE REGISTROS ******************************************")
    print("\tC\tok\tclk\tTAG")
    for i in range(len(BR)):
        print("R" + str(i) + ":\t" + BR[i].__str__())

# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************

def leerFichero():
    lineas = sys.stdin.readlines()
    return lineas


def cargaInstruccionesMemoria(entrada):
    MI = list()
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

        if len(MI) != 0:
            instAnt = MI[-1]
            if instAnt.cod == 3:
                if inst.cod == 1 or inst.cod == 2:
                    if inst.rt == instAnt.rt or inst.rs == instAnt.rt:
                        MI.append(
                            Instruccion(cod=0, rd=0, rs=0, rt=0, inmediato=0, numInst=i))

        MI.append(inst)
        i += 1

    return MI, i


# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    # Cargamos en memoria las instrucciones
    entrada = [a for a in leerFichero()]
    # MI-> Memoria de instrucciones
    MI, acaba = cargaInstruccionesMemoria(entrada)

    for elem in MI:
        print(elem.toSring())

    INS = len(MI) #*********************************************************************************************************************************FFFFFFF

    # Registros
    BR=list()
    for i in range(REG):
        BR.append(Reg(contenido=(i+1)*10, ok=1, clk_tick_ok=0, TAG_ROB=0))

    # Memoria de datos
    MD = [a for a in range(0, DAT)]

    # Inicializamos las Unidades Funcionales
    UF = [UF_class(uso=0, cont_ciclos=0, TAG_ROB=0, opa=0, opb=0, operacion=0, res=0, res_ok=0, clk_tick_ok=0)] * TOTAL_UF

    # Inicializamos las Estaciones de Reserva (Cada unidad funcional tiene una)
    ER = [a for a in range(0, TOTAL_UF)]
    for i in range(len(ER)):
        ER[i]= [ER_class(linea_valida=0, TAG_ROB=0, operacion=0, opa=0, opa_ok=0, clk_tick_ok_a=0,
                         opb=0, opb_ok=0, clk_tick_ok_b=0, inmediato=0)] * INS


    # Inicializamos el ROB_class
    ROB = [ROB_class(0, 0, 0, 0, 0, 0, 0)] * INS

    inst_prog = len(MI)  # total instrucciones programa
    inst_rob = 0  # instrucciones en rob

    p_rob_cabeza = 0
    p_rob_cola = 0  # puntero a las posiciones de rob para introducir (cola) o retirar instrucciones (cabeza)
    PC = 0  # puntero a memoria de instrucciones, siguiente instrucción a IF
    p_er_cola = [0, 0, 0]  # vector de punteros que apuntan a la cola de cada una de las UF_class

    # ******************************************************************************************************
    #    SIMULADOR
    # ******************************************************************************************************

    #****** DATOS PARA PASARLE A LOS METODOS *****************************************
    #BR -> BancoRegistros, MD->MemoriaDatos, MI->MemoriaInstrucciones, Var-Variables
    Var = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola]
    listaDatos = [BR, MD, MI, UF, ER, ROB, Var]
    #**********************************************************************************

    ciclo = 1
    i = 0
    while (inst_rob > 0 or inst_prog > 0):
        print()
        print("---- CICLO " + str(ciclo) + " -----------------------------------------------------------------------------------------------")
        print()
        listaDatos = Etapa_COMMIT(listaDatos)
        listaDatos = Etapa_WB(listaDatos)
        listaDatos = Etapa_EX(listaDatos)
        listaDatos = Etapa_ID_ISS(listaDatos)
        inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, PC, p_er_cola = listaDatos[6]
        BR, MD, MI, UF, ER, ROB, Var = listaDatos
        ciclo += 1

        # MOSTRAR EL CONTENIDO DE LAS ESTRUCTURAS
        Mostrar_ER(ER)
        Mostrar_ROB(ROB)
        Mostar_Banco_Registros(BR)

