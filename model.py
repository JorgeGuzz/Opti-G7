from gurobipy import Model, GRB, quicksum

from datos.parametros import n,m,p,l,s1,s2,s3,s4,PR,MINCOM,M
from carga_datos.Yt import obtener_Yt
from carga_datos.Xts1 import obtener_Xts1
from carga_datos.Xts2 import obtener_Xts2
from carga_datos.Xts3 import obtener_Xts3
from carga_datos.Xts4 import obtener_Xts4
from carga_datos.SEi import obtener_SEi
from carga_datos.STt import obtener_STt
from carga_datos.CTt import obtener_CTt
from carga_datos.DMINd import obtener_DMINd
from carga_datos.ELIMci import obtener_ELIMci
from carga_datos.CMAXc import obtener_CMAXc
from carga_datos.Ai import obtener_Ai
from carga_datos.AMAXc import obtener_AMAXc
from carga_datos.CEi import obtener_CEi
from carga_datos.Pid import obtener_Pid
from carga_datos.Ctc import obtener_Ctc

# ----------------------- Generacion del modelo ------------------------
model = Model()
model.setParam("TimeLimit", 1800)  # Establece el tiempo m ́aximo en segundos
# ----------------------- Generacion de Rangos ------------------------
I_ = range(1, n + 1)
Iprima_ = I_[:m]
T_ = range(1, p + 1)
D_ = range(1, 8 + 1)
C_ = range(1, l + 1)
S1_ = range(1, s1 + 1)
S2_ = range(1, s2 + 1)
S3_ = range(1, s3 + 1)
S4_ = range(1, s4 + 1)
#----------------------- Importacion parametros ------------------------
terreno_cumple_s1 = obtener_Xts1()
terreno_cumple_s2 = obtener_Xts2()
terreno_cumple_s3 = obtener_Xts3()
terreno_cumple_s4 = obtener_Xts4()
terreno_cumple_trabajos = obtener_Yt()
superficie_terrenos = obtener_STt()
superficie_edificios = obtener_SEi()
costo_terrenos = obtener_CTt()
mininmo_beneficiados_decil = obtener_DMINd()
limite_edificios_comuna = obtener_ELIMci()
cant_max_nuevas_personas_comuna = obtener_CMAXc()
altura_edificios = obtener_Ai()
altura_maxima_comunas = obtener_AMAXc()
costo_edificios = obtener_CEi()
personas_decil_edificios = obtener_Pid()
terrenos_comunas = obtener_Ctc()
# ----------------------- Creacion de Parametros ------------------------
PR = PR
CT = {(t): costo_terrenos[t - 1] for t in T_}
CE = {(i): costo_edificios[i - 1] for i in I_}
P = {(i, d): personas_decil_edificios[i - 1][d - 1] for i in I_ for d in D_}
A = {(i): altura_edificios[i - 1] for i in I_}
XS1 = {(t, s): terreno_cumple_s1[t - 1][s - 1] for t in T_ for s in S1_}
XS2 = {(t, s): terreno_cumple_s2[t - 1][s - 1] for t in T_ for s in S2_}
XS3 = {(t, s): terreno_cumple_s3[t - 1][s - 1] for t in T_ for s in S3_}
XS4 = {(t, s): terreno_cumple_s4[t - 1][s - 1] for t in T_ for s in S4_}
DMIN = {(d): mininmo_beneficiados_decil[d - 1] for d in D_}
C = {(t, c): terrenos_comunas[t - 1][c - 1] for t in T_ for c in C_}
CMAX = {(c): cant_max_nuevas_personas_comuna[c - 1] for c in C_}
ELIM = {(c, i): limite_edificios_comuna[c - 1][i - 1] for c in C_ for i in I_}
AMAX = {(c): altura_maxima_comunas[c - 1] for c in C_}
Y = {(t): terreno_cumple_trabajos[t - 1] for t in T_}
MINCOM = MINCOM
SE = {(i): superficie_edificios[i - 1] for i in I_}
ST = {(t): superficie_terrenos[t - 1] for t in T_}

# ----------------------- Creacion de Variables ------------------------
Z = model.addVars(I_, T_, vtype=GRB.BINARY, name="Z_it")
B = model.addVars(C_, vtype=GRB.BINARY, name="B_c")

# ----------------------- Creacion de Restricciones ------------------------
# R1
model.addConstrs((quicksum(Z[i, t] for i in I_) <= 1 for t in T_), name="R1")

# R2
model.addConstr((quicksum(quicksum(Z[i, t] * (CT[t] + CE[i]) for i in I_) for t in T_) <= PR), name="R2")

# R3
model.addConstrs((quicksum(quicksum(
    Z[i, t] * P[i, d] for i in I_) for t in T_) >= DMIN[d] for d in D_), name="R3")

# R4
model.addConstrs((quicksum(XS1[t, s] for s in S1_) + quicksum(XS4[t, s]
                 for s in S4_) >= quicksum(Z[i, t] for i in Iprima_) for t in T_), name="R4.1")
model.addConstrs((quicksum(XS2[t, s] for s in S2_) + quicksum(XS4[t, s]
                 for s in S4_) >= quicksum(Z[i, t] for i in Iprima_) for t in T_), name="R4.2")
model.addConstrs((quicksum(XS3[t, s] for s in S3_) + quicksum(XS4[t, s]
                 for s in S4_) >= quicksum(Z[i, t] for i in Iprima_) for t in T_), name="R4.3")

# R5
model.addConstrs((quicksum(quicksum(Z[i, t] * C[t, c] * quicksum(P[i, d]
                 for d in D_) for i in I_) for t in T_) <= CMAX[c] for c in C_), name="R5")

# R6
model.addConstrs((quicksum(Z[i, t] * C[t, c] for t in T_)
                 <= ELIM[c, i] for c in C_ for i in I_), name="R6")

# R7 falta definir M grande
model.addConstrs((quicksum(quicksum(Z[i, t] * C[t, c] for t in T_)
                 for i in I_) >= 1 + M * (B[c] - 1) for c in C_), name="R7")

# R8
model.addConstr((quicksum(B[c] for c in C_) >= MINCOM), name="R8")

# R9
model.addConstrs((quicksum(XS4[t, s] for s in S4_) + Y[t] >=
                 quicksum(Z[i, t] for i in Iprima_) for t in T_), name="R9")

# R10
model.addConstrs((Z[i, t] * SE[i] <= ST[t]
                 for i in I_ for t in T_), name="R10")

# R11
model.addConstrs((Z[i, t] * C[t, c] * A[i] <= AMAX[c]
                 for i in I_ for t in T_ for c in C_), name="R11")

#----------------------- Creacion de Funcion Objetivo ------------------------

#Funcion Objetivo
obj = quicksum( quicksum( Z[i,t] * quicksum( P[i,d] for d in D_) for i in I_) for t in T_)
model.setObjective(obj, GRB.MAXIMIZE)

#-----------------------        Resultados       ------------------------

model.optimize()
valor_objetivo = model.ObjVal

print("\n+--------------------------------------------------------------------------------------------------+")
print(f"Las personas beneficiadas por el proyecto de viviendas sociales serán: {valor_objetivo}")
print("+--------------------------------------------------------------------------------------------------+\n")
print("Para lograr este valor se deben construir en los siguientes terrenos y los edificios respectivos.\n")

print("+----------+----------+")
print("|Terreno   |Edificio  |")
print("+----------+----------+")
for t in T_:
    for i in I_:
        if Z[i,t].x == 1:
            cadena = "|{:<10}|{:<10}|".format(t, i)
            print(cadena)
print("+----------+----------+")


with open("resultados/resultados_Z.csv", "w") as archivo: 
    archivo.write("Z,i,t")
    for t in T_:
        for i in I_:
            archivo.write(f"\n{Z[i,t].x},{i},{t}")

with open("resultados/resultados_B.csv", "w") as archivo: 
    archivo.write("B,c")
    for c in C_:
        archivo.write(f"\n{B[c].x},{c}")