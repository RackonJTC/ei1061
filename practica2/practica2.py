
#Juego de instrucciones. Código de operación
add=1
sub=2
lw=3
sw=4
mult=5

#Capacidad de las estructuras de almacenamiento es ilimitada pero se pone una máxima
REG=16
DAT=32
INS=32

#Códigos para las UF
TOTAL_UF=3
ALU=0
MEM=1
MULT=2

#Ciclos de ejecucion de UF
CICLOS_MEM=2
CICLOS_ALU=1
CICLOS_MULT=5

#Etapas de procesamiento de las instrucciones en ROB
ISS=1
EX=2
WB=3

class Instruccion:
    cod=""
    rd=""
    rs=""
    rt=""
    inmediato=0

    def __init__(self, cod, rd, rs, rt, inmediato):
        self.cod = cod
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.inmediato = inmediato

class Reg:
    contenido=0
    ok=-1
    clk_tick_ok=-1
    TAG_ROB=-1

    def __init__(self, contenido, ok, clk_tick_ok, TAG_ROB):
        self.contenido = contenido
        self.ok = ok
        self.clk_tick_ok = clk_tick_ok
        self.TAG_ROB = TAG_ROB

class ER:
    linea_valida=-1
    TAG_ROB=-1
    operacion=-1
    opa=-1
    opa_ok=-1
    clk_tick_ok_a=-1
    opb=-1
    opb_ok=-1
    clk_tick_ok_b=-1
    inmediato=-1

    def __init__(self, linea_valida, TAG_ROB, operacion, opa, opa_ok, clk_tick_ok_a, opb, opb_ok, clk_tick_ok_b, inmediato):
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
