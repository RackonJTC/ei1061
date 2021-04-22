# ******************************************************************************************************
#    VARIABLES GLOBALES
# ******************************************************************************************************

# Juego de instrucciones. Código de operación
#                 0      1      2      3     4     5
codOperacion = ["NOP", "add", "sub", "lw", "sw", "mult"]

# Capacidad de las estructuras de almacenamiento es ilimitada pero se pone una máxima
REG = 16  # Numerode registros
DAT = 32  # Tamaño de memoria de datos
INS = 32  # Tamaño de memoria de instrucciones

# Códigos para las uf
TOTAL_UF = 3
ALU = 0
MEM = 1
MULT = 2
unidadesFuncionales = ["ALU", "MEM", "MULT"]

# Ciclos de ejecucion de uf
CICLOS_MEM = 2  # Carga y almacenamiento
CICLOS_ALU = 1  # Suma y Resta
CICLOS_MULT = 5  # Multiplicación
ciclosEjecucion = [CICLOS_ALU, CICLOS_MEM, CICLOS_MULT]
max = 0
codUF = 0

# Etapas de procesamiento de las instrucciones en rob
ISS = 1
EX = 2
WB = 3


# ******************************************************************************************************
#    ESTRUCTURAS DE DATOS
# ******************************************************************************************************


class Instruccion:

    def __init__(self, cod, rd, rs, rt, inmediato, num, tipouf):
        self.cod = cod  # Operación a realizar
        self.rd = rd  # Registro destino
        self.rs = rs  # Registro fuente OP1
        self.rt = rt  # Registro fuente OP2
        self.inmediato = inmediato  # Dato inmediato
        self.numInst = num  # Numero de instrucción
        self.tipoUF = tipouf  # Tipo UF (ALU, MEM, MULT)

    def __str__(self):
        if self.cod == 0:
            return "NOP"
        if self.cod == 4:
            return codOperacion[self.cod] + " " + "r" + str(self.rt) + ", " + str(self.inmediato) + "(" + "r" + str(
                self.rs) + ")"
        if self.cod == 3:
            return codOperacion[self.cod] + " " + "r" + str(self.rt) + ", " + str(self.inmediato) + "(" + "r" + str(
                self.rs) + ")"
        return codOperacion[self.cod] + " " + "r" + str(self.rd) + ", " + "r" + str(self.rs) + ", " + "r" + str(self.rt)

    def imprime(self):
        print("Codigo: " + str(self.cod) + ", Rd: " + str(self.rd) + ", Rs: " + str(self.rs) + ", Rt: " + str(self.rt)
              + ", Inm: " + str(self.inmediato) + ", numInst: " + str(self.numInst) + ", tipoUF: " + str(self.tipoUF))


class Registro:

    def __init__(self, contenido, ok, clk_tick_ok, tag):
        self.contenido = contenido  # Contenido del registro
        self.ok = ok  # Contenido valido(1) o no (0)
        self.clk_tick_ok = clk_tick_ok  # Indicar a partir de que ciclo de reloj es ok
        self.TAG_ROB = tag  # Si el contenido no es valido, indicar que linea de rob lo actualiza

    def __str__(self) -> str:
        cadena = str(self.contenido) + "\t" + str(self.ok) + "\t" + str(self.clk_tick_ok) + "\t" + str(self.TAG_ROB)
        return cadena


class EstacionReserva:

    def __init__(self, linea_valida, tag, operacion, opa, opa_ok, clk_tick_ok_a, opb, opb_ok, clk_tick_ok_b,
                 inmediato):
        self.linea_valida = linea_valida  # contenido de la línea válido (1) o no (0)
        self.TAG_ROB = tag  # línea del rob donde se ha almacenado esta instrucción
        self.operacion = operacion  # operación a realizar en uf (suma,resta,mult,lw,sw)
        self.opa = opa  # operando a
        self.opa_ok = opa_ok  # opa válido (1) o no (0)
        self.clk_tick_ok_a = clk_tick_ok_a  # a partir de qué ciclo de reloj el opa es válido
        self.opb = opb  # operando b
        self.opb_ok = opb_ok  # opb válido(1) o no(0)
        self.clk_tick_ok_b = clk_tick_ok_b  # a partir de qué ciclo de reloj el opb es válido
        self.inmediato = inmediato  # utilizado para las instrucciones lw/sw

    def __str__(self) -> str:
        cadena = str(self.linea_valida) + "\t   " + str(self.TAG_ROB) + "\t   " + str(self.operacion) + "\t   " \
                 + str(self.opa) + "\t   " + str(self.opa_ok) + "\t   " + str(self.clk_tick_ok_a) + "\t   " \
                 + str(self.opb) + "\t   " + str(self.opb_ok) + "\t   " + str(self.clk_tick_ok_b) + "\t   " \
                 + str(self.inmediato)
        return cadena


class BufferReordenamiento:

    def __init__(self, tag, linea_valida, destino, valor, valor_ok, clk_tick_ok, etapa):
        self.TAG_ROB = tag  # Etiqueta que identifica la línea de rob
        self.linea_valida = linea_valida  # Indica si el contenido de la línea es válido (1) o no (0)
        self.destino = destino  # identificador registro destino (rd)
        self.valor = valor  # resultado tras finalizar la etapa EX
        self.valor_ok = valor_ok  # indica si valor es válido (1) o no (0)
        self.clk_tick_ok = clk_tick_ok  # a partir de qué ciclo de reloj es válido
        self.etapa = etapa  # Etapa de procesamiento de la instrucción ISS, EX, WB

    def __str__(self) -> str:
        cadena = str(self.TAG_ROB) + "\t  " + str(self.linea_valida) + "\t\t " + str(self.destino) + "\t\t " \
                 + str(self.valor) + "\t\t " + str(self.valor_ok) + "\t\t " + str(self.clk_tick_ok) + "\t\t  " \
                 + str(self.etapa)
        return cadena


class UnidadFuncional:  # Unidad funcional

    def __init__(self, uso, cont_ciclos, tag, opa, opb, operacion, res, res_ok, clk_tick_ok):
        self.uso = uso  # Indica si uf está utilizada (1) o no (0)
        self.cont_ciclos = cont_ciclos  # contador de ciclos consumidos por la uf
        self.TAG_ROB = tag  # Línea del rob donde se tiene que almacenar el resultado tras EX
        self.opa = opa  # valor opa (en almacenamiento contiene dato a escribir en memoria
        self.opb = opb  # valor opb (en lw y sw contiene dirección de memoria de datos )
        self.operacion = operacion  # se utiliza para indicar operacion a realizar add/sub y lw/sw o mult
        self.res = res  # resultado
        self.res_ok = res_ok  # resultado valido
        self.clk_tick_ok = clk_tick_ok  # a partir de qué ciclo de reloj es válido el resultado

    def __str__(self) -> str:
        cadena = "uso: " + str(self.uso) + " cont_c: " + str(self.cont_ciclos) + " TAG_R: " + str(self.TAG_ROB) + \
                 " opa: " + str(self.opa) + " opb: " + str(self.opb) + " op: " + str(self.operacion) + " res: " \
                 + str(self.res) + " res_ok: " + str(self.res_ok) + " clk_t_ok: " + str(self.clk_tick_ok)
        return cadena

    def libera(self):
        self.uso = 0
        self.cont_ciclos = 0
        self.TAG_ROB = 0
        self.opa = 0
        self.opb = 0
        self.operacion = 0
        self.res = 0
        self.res_ok = 0
        self.clk_tick_ok = 0


# ******************************************************************************************************
#    ETAPAS
# ******************************************************************************************************

# ISS = 1  EX = 2  WB = 3
def commit(listadatos):
    registros, memoriadatos, instrucciones, uf, er, rob, otros = listadatos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo = otros

    if rob[p_rob_cabeza].linea_valida == 1 and rob[p_rob_cabeza].etapa == 3:
        id_reg = rob[p_rob_cabeza].destino
        if rob[p_rob_cabeza].TAG_ROB == registros[id_reg].TAG_ROB and rob[p_rob_cabeza].destino != -1:
            registros[id_reg].contenido = rob[p_rob_cabeza].valor
            registros[id_reg].ok = 1
            registros[id_reg].clk_tick_ok = ciclo + 1

        rob[p_rob_cabeza] = 0
        rob[p_rob_cabeza] = BufferReordenamiento(0, 0, 0, 0, 0, 0, 0)

        p_rob_cabeza += 1
        inst_rob -= 1

    ciclo += 1

    otros = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo]
    listadatos = [registros, memoriadatos, instrucciones, uf, er, rob, otros]

    return listadatos


def wb(datos):
    registros, memoriadatos, instrucciones, uf, er, rob, otros = datos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo = otros

    i = 0
    bucle = 0

    while bucle == 0 and i < TOTAL_UF:
        if uf[i].operacion == 4 and uf[i].res_ok == 1:
            rob[uf[i].TAG_ROB].etapa = WB  # WB
            rob[uf[i].TAG_ROB].destino = -1  # diferenciar de sw
            # Se deja libre la uf
            uf[i].libera()
            # Se ha escrito un dato. No se pueden escribir más.
            bucle = 1
        elif uf[i].uso == 1 and uf[i].res_ok == 1 and uf[i].clk_tick_ok <= ciclo:
            # Se actualiza rob
            id = uf[i].TAG_ROB
            rob[id].valor = uf[i].res
            rob[id].valor_ok = 1
            rob[id].clk_tick_ok = ciclo + 1
            rob[id].etapa = 3  # WB = 3

            # Se deja libre la uf
            uf[i].libera()

            # Se ha escrito un dato. No se pueden escribir más.
            bucle = 1

            for k in range(TOTAL_UF):
                fin = p_er_cola[k]
                for j in range(fin):
                    # Si el operando depende de ese resultado
                    if er[k][j].linea_valida == 1:  # Si la linea es valida
                        if er[k][j].opa_ok == 0 and er[k][j].opa == id:  # Si opa no disponible y depende de TAG_ROB
                            # er[k][j].opa = registros[rob[id].destino].contenido
                            er[k][j].opa = uf[i].res
                            er[k][j].opa_ok = 1
                            er[k][j].clk_tick_ok_a = ciclo + 1
                        if er[k][j].opb_ok == 0 and er[k][j].opb == id:  # Si opb depende de ese resultado
                            # er[k][j].opb = registros[rob[id].destino].contenido
                            er[k][j].opB = uf[i].res
                            er[k][j].opb_ok = 1
                            er[k][j].clk_tick_ok_b = ciclo + 1

        else:
            i += 1

    otros = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo]
    datos = [registros, memoriadatos, instrucciones, uf, er, rob, otros]
    return datos


def ex(datos):
    global max
    global codUF
    registros, memoriadatos, instrucciones, uf, er, rob, otros = datos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo = otros
    i = 0
    enviar = 0

    while i < TOTAL_UF:
        # Establecer cilos máximos para cada uf
        if i == 0:
            max = CICLOS_ALU
        elif i == 1:
            max = CICLOS_MEM
        elif i == 2:
            max = CICLOS_MULT
        if uf[i].uso == 1:  # si está en uso, se incrementa el ciclo y no se pueden enviar otra instrucción.
            if uf[i].cont_ciclos < max:
                uf[i].cont_ciclos = uf[i].cont_ciclos + 1  # incrementar el ciclo

                if uf[i].cont_ciclos == max:  # si se ha finalizado la operación genera resultado y valida. uf_.oper
                    # Este dato solo se podrá utilizar en el siguiente ciclo después de haberlo generado
                    if uf[i].operacion == 1:  # add
                        uf[i].res = uf[i].opa + uf[i].opb
                    elif uf[i].operacion == 2:  # sub
                        uf[i].res = uf[i].opa - uf[i].opb
                    elif uf[i].operacion == 3:  # lw. En opb esta la direccion de memoria de datos
                        uf[i].res = memoriadatos[uf[i].opa]
                    elif uf[i].operacion == 4:  # sw. En opb esta la direccion de memoria de datos
                        # (MEM(inm+(rs))) = (rt)
                        #print("HOLA: " + str(uf[i].opa))
                        memoriadatos[uf[i].opb] = registros[uf[i].opa].contenido
                    elif uf[i].operacion == 5:  # mult
                        uf[i].res = uf[i].opa * uf[i].opb

                    uf[i].res_ok = 1
                    uf[i].clk_tick_ok = ciclo + 1

        elif enviar == 0:  # no está en uso y todavía no se ha enviado ninguna instrucción
            # se comprueba si se puede enviar alguna de este tipo
            er_ = er[i]
            fin = p_er_cola[i]  # última línea insertada
            j = 0  # contador de líneas de er[i] desde 0 hasta fin
            while enviar == 0 and j < fin:  # búsqueda de instrucción a ejecutar en todas las líneas validas de er_
                if er_[j].linea_valida == 1:  # línea válida. comprueba si los operandos están disponibles
                    if er_[j].opa_ok == 1 and er_[j].clk_tick_ok_a <= ciclo and er_[j].opb_ok == 1 \
                            and er_[j].clk_tick_ok_b <= ciclo:  # operandos disponibles
                        if er_[j].operacion == 1 or er_[j].operacion == 2:
                            codUF = 0
                        elif er_[j].operacion == 3 or er_[j].operacion == 4:
                            codUF = 1
                        elif er_[j].operacion == 5:
                            codUF = 2
                        uf[codUF] = 0
                        uf[codUF] = UnidadFuncional(uso=1, cont_ciclos=0, tag=er_[j].TAG_ROB, opa=er_[j].opa,
                                                    opb=er_[j].opb, operacion=er_[j].operacion, res=0, res_ok=0,
                                                    clk_tick_ok=0)

                        if er_[j].operacion == 3 or er_[j].operacion == 4:
                            print("HOLA: " + str(er_[j].opa))
                            uf[i].opa = er_[j].opa + er_[j].inmediato

                        rob[er[i][j].TAG_ROB].etapa = 2  # Actualizar en etapa en rob a EX
                        er[i][j].linea_valida = 0  # TODO: Linea añadida por mi
                        enviar = 1

                    else:
                        j += 1
                else:  # buscar otra instrucción
                    j += 1
        i += 1

    otros = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo]
    datos = [registros, memoriadatos, instrucciones, uf, er, rob, otros]
    return datos


def idiss(datos):
    registros, memoriadatos, instrucciones, uf, er, rob, otros = datos
    inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo = otros

    if inst_prog > 0:
        # Cogemos la intruccione en la ER correspondiente (se omite IF)
        inst = instrucciones[pc]
        inst.imprime()
        # Actualizamos linea
        er[inst.tipoUF][p_er_cola[inst.tipoUF]] = EstacionReserva(linea_valida=0, tag=0, operacion=0, opa=0, opa_ok=1,
                                                                  clk_tick_ok_a=0, opb=0, opb_ok=0, clk_tick_ok_b=0,
                                                                  inmediato=0)
        er[inst.tipoUF][p_er_cola[inst.tipoUF]].linea_valida = 1

        er[inst.tipoUF][p_er_cola[inst.tipoUF]].operacion = inst.cod

        if registros[inst.rs].ok == 1:
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opa = registros[inst.rs].contenido
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opa_ok = 1
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].clk_tick_ok_a = ciclo + 1
        else:
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opa = registros[inst.rs].TAG_ROB
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opa_ok = 0

        if registros[inst.rt].ok == 1:
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb = registros[inst.rt].contenido
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb_ok = 1
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].clk_tick_ok_b = ciclo + 1
        else:
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb = registros[inst.rt].TAG_ROB
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb_ok = 0

        if inst.cod == 4 or inst.cod == 3:
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb = inst.rt
            er[inst.tipoUF][p_er_cola[inst.tipoUF]].opb_ok = 1

        er[inst.tipoUF][p_er_cola[inst.tipoUF]].inmediato = inst.inmediato

        # Añadir instrucción en rob y actualizar todos sus campos. Posición apuntada por p_rob_cola
        # si instrucción es sw poner en el campo destino un 0 para identificar que no se escribe nada en etapa commit
        # rob -> def __init__(self, TAG_ROB, linea_valida, destino, valor, valor_ok, clk_tick_ok, etapa):

        inst_rob += 1

        rob[p_rob_cola].TAG_ROB = p_rob_cola
        rob[p_rob_cola].linea_valida = 1
        rob[p_rob_cola].etapa = ISS

        if inst.cod == 4:
            rob[p_rob_cola].destino = 0
        elif inst.cod == 3:
            rob[p_rob_cola].destino = inst.rt
        else:
            rob[p_rob_cola].destino = inst.rd

        # Invalidar el registro destino de esta instrucción
        registros[inst.rd].ok = 0
        registros[inst.rd].TAG_ROB = p_rob_cola
        er[inst.tipoUF][p_er_cola[inst.tipoUF]].TAG_ROB = p_rob_cola

        p_er_cola[inst.tipoUF] += 1
        p_rob_cola += 1

        # Actualiza pc + 1 y inst_prog - 1
        pc += 1
        inst_prog = inst_prog - 1

    otros = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo]
    datos = [registros, memoriadatos, instrucciones, uf, er, rob, otros]
    return datos


# ******************************************************************************************************
#    METODOS MOSTRAR CONTENIDO
# ******************************************************************************************************
def imprime(unidad, tipo):
    if tipo == "uf":
        print("*** UNIDADES FUNCIONALES *********************************************************")
        for i in range(len(unidadesFuncionales)):
            print("UF " + unidadesFuncionales[i] + ": " + unidad[i].__str__())

    elif tipo == "er":
        nombresEstaciones = ["ALU", "MEM", "MULT"]
        print("*** ESTACIONES DE RESERVA *********************************************************")
        print("\t\tl_val\tTGROB\toper\topa\t  opa_ok\tcA_ok\t  opb\t opb_ok\t cB_ok\tinmed")
        for i in range(len(unidad)):
            for j in range(len(unidad[i])):
                if type(unidad[i][j]) != int:
                    print("ER " + nombresEstaciones[i] + " " + str(j) + ":\t" + unidad[i][j].__str__())

    elif tipo == "rob":
        print("*** BUFFER DE REORDENAMIENTO ******************************************************")
        print("\t\tTAG\tlinVal\tdest\tvalor\tv_ok\tclk_ok\tetapa")
        for i in range(len(unidad)):
            print("ROB" + str(i) + ":\t" + unidad[i].__str__())

    elif tipo == "reg":
        print("*** BANCO DE REGISTROS ************************************************************")
        print("\t  C\t   ok\tclk\tTAG")
        for i in range(len(unidad)):
            print("R" + str(i) + ":   " + unidad[i].__str__())

    elif tipo == "mem":
        print("*** MEMORIA DE DATOS **************************************************************")
        for i in range(len(unidad) // 3 + 2):
            print("M" + str(i) + ": " + unidad[i].__str__() + ",", end=' ')
        print()
        for i in range(len(unidad) // 3 + 2, len(unidad) - len(unidad) // 3):
            print("M" + str(i) + ": " + unidad[i].__str__() + ",", end=' ')
        print()
        for i in range(len(unidad) - len(unidad) // 3, len(unidad)):
            print("M" + str(i) + ": " + unidad[i].__str__() + ",", end=' ')

# ******************************************************************************************************
#    METODO DE ENTRADA Y SALIDA
# ******************************************************************************************************


def leerfichero(fichero):
    # Imprime en consola
    # lineas = sys.stdin.readlines()
    # print(lineas)

    # Imprime en run
    f = open(fichero)
    memIns = []
    i = 0
    for linea in f:
        linea.replace(",", "")
        memIns.append(linea.rstrip())
        i += 1
    return memIns


def cargainstruccionesmemoria(entrada):
    instrucciones = list()
    i = 1
    cod, tipouf = -1, -1
    for linea in entrada:
        elem = linea.rstrip("\n").split(" ")
        if elem[0] == "add":
            cod, tipouf = 1, 0
        if elem[0] == "sub":
            cod, tipouf = 2, 0
        if elem[0] == "lw":
            cod, tipouf = 3, 1
        if elem[0] == "sw":
            cod, tipouf = 4, 1
        if elem[0] == "mult":
            cod, tipouf = 5, 2
        if cod == 3 or cod == 4:
            elem2 = elem[2].split("(")
            inm = int(elem2[0])
            elem3 = elem2[1].split(")")
            rs = int(elem3[0][1])
            inst = Instruccion(cod=cod, rt=int(elem[1][1]), rs=rs, inmediato=inm, rd=0, num=i, tipouf=tipouf)
        else:
            inst = Instruccion(cod=cod, rd=int(elem[1][1]), rs=int(elem[2][1]), rt=int(elem[3][1]), inmediato=0,
                               num=i, tipouf=tipouf)

        # Añadir NOPS automaticos

        if len(instrucciones) != 0:
            ant = instrucciones[-1]
            if ant.cod == 3:
                if inst.cod == 1 or inst.cod == 2:
                    if inst.rt == ant.rt or inst.rs == ant.rt:
                        instrucciones.append(
                            Instruccion(cod=0, rd=0, rs=0, rt=0, inmediato=0, num=i, tipouf=tipouf))

        instrucciones.append(inst)
        i += 1

    return instrucciones, i


# ******************************************************************************************************
#    MAIN
# ******************************************************************************************************

if __name__ == '__main__':

    # **************************************************************************************************
    #    DECLARACION DE VARIABLES
    # **************************************************************************************************

    # Cargamos las instrucciones desde el fichero
    entrada = [a for a in leerfichero("instrucciones13")]
    instrucciones, acaba = cargainstruccionesmemoria(entrada)
    for elem in instrucciones:
        print(elem.__str__())

    INS = len(instrucciones)  # Modificamos el INS con el total de instrucciones del fichero

    # Banco de Registros, r0=10, r1=20, r2=30, ...
    registros = list()
    for i in range(REG):
        registros.append(Registro(contenido=(i + 1) * 10, ok=1, clk_tick_ok=0, tag=0))

    # Memoria de datos
    memoriadatos = [0 for a in range(0, DAT)]

    # Inicializamos las Unidades Funcionales
    uf = [a for a in range(0, TOTAL_UF)]
    uf[0] = UnidadFuncional(uso=0, cont_ciclos=0, tag=0, opa=0, opb=0, operacion=0, res=0, res_ok=0, clk_tick_ok=0)
    uf[1] = UnidadFuncional(uso=0, cont_ciclos=0, tag=0, opa=0, opb=0, operacion=0, res=0, res_ok=0, clk_tick_ok=0)
    uf[2] = UnidadFuncional(uso=0, cont_ciclos=0, tag=0, opa=0, opb=0, operacion=0, res=0, res_ok=0, clk_tick_ok=0)

    # Inicializamos las Estaciones de Reserva (Cada unidad funcional tiene una)
    er = [a for a in range(0, TOTAL_UF)]
    for i in range(len(er)):
        er[i] = [a for a in range(0, 32)]

    # Inicializamos el BufferReordenamiento
    rob = list()
    for i in range(INS):
        rob.append(BufferReordenamiento(0, 0, 0, 0, 0, 0, 0))

    inst_prog = len(instrucciones)  # total instrucciones programa
    inst_rob = 0  # instrucciones en rob

    p_rob_cabeza = 0
    p_rob_cola = 0  # puntero a las posiciones de rob para introducir (cola) o retirar instrucciones (cabeza)
    pc = 0  # puntero a memoria de instrucciones, siguiente instrucción a IF
    p_er_cola = [0, 0, 0]  # vector de punteros que apuntan a la cola de cada una de las UnidadFuncional
    ciclo = 0

    # ******************************************************************************************************
    #    SIMULADOR
    # ******************************************************************************************************

    # ****** DATOS PARA PASARLE A LOS METODOS ***********************************************************************
    # registros -> BancoRegistros, memoriadatos->MemoriaDatos, instrucciones->MemoriaInstrucciones, otros->Variables
    otros = [inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo]
    datos = [registros, memoriadatos, instrucciones, uf, er, rob, otros]
    # ****************************************************************************************************************

    while inst_rob > 0 or inst_prog > 0:  # Un ciclo de reloj ejecuta las 5 etapas de procesamiento de un inst
        print()
        print("---- CICLO " + str(
            ciclo) + " -----------------------------------------------------------------------------------------------")
        print()
        # Ejecutamos etapas
        datos = commit(datos)
        datos = wb(datos)
        datos = ex(datos)
        datos = idiss(datos)

        inst_prog, inst_rob, p_rob_cabeza, p_rob_cola, pc, p_er_cola, ciclo = datos[6]
        registros, memoriadatos, instrucciones, uf, er, rob, otros = datos

        print("FINAL: " + "inst_rob: " + str(inst_rob) + ", inst_prog: " + str(inst_prog))

        # MOSTRAR EL CONTENIDO DE LAS ESTRUCTURAS
        imprime(uf, "uf")
        imprime(er, "er")
        imprime(rob, "rob")
        imprime(registros, "reg")
        imprime(memoriadatos, "mem")
        print()
