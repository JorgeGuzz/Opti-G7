from gurobipy import Model, GRB, quicksum

# ----------------------- Generacion del modelo ------------------------
model = Model()
model.setParam("TimeLimit", 1800)  # Establece el tiempo m ́aximo en segundos
# ----------------------- Generacion de Rangos ------------------------
I_ = range(1, n + 1)
Iprima_ = Edificios[:m]
T_ = range(1, p + 1)
D_ = range(1, 8 + 1)
C_ = range(1, l + 1)
S1_ = range(1, s1 + 1)
S2_ = range(1, s2 + 1)
S3_ = range(1, s3 + 1)
S4_ = range(1, s4 + 1)
# ----------------------- Creacion de Parametros ------------------------
PR =
CT = {(t):}
TMIN =
CE = {(i):}
P = {(i, d): }
D = {(i):}
A = {(i):}
DISTMAX =
XS1 = {(t, s): }
XS2 = {(t, s): }
XS3 = {(t, s): }
XS4 = {(t, s): }
DMIN = {(d):}
C = {(t, c): }
CMAX = {(c):}
ELIM = {(c, i): }
DMAX = {(c):}
AMAX = {(c):}
Y = {(t):}
MINCOM =
SE = {(i):}
ST = {(t):}


# ----------------------- Creacion de Variables ------------------------
Z = model.addVars(I_, T_, vtype=GRB.BINARY, name="Z_it")
B = model.addVars(C_, vtype=GRB.BINARY, name="B_c")

# ----------------------- Creacion de Restricciones ------------------------
# R1
model.addConstrs((quicksum(Z[i, t] for i in I_) <= 1 for t in T_), name="R1")

# R2
model.addConstrs((quicksum(
    quicksum(Z[i, t] * (CT[t] + CE[i]) for i in I_) for t in T_) <= PR), name="R2")

# R3
model.addConstrs((quicksum(quicksum(
    Z[i, t] * P[i, d] for i in I_) for t in T_) <= DMIN[d] for d in D_), name="R3")

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
model.addConstrs((quicksum(B[c] for c in C_) >= MINCOM), name="R8")

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

print(f"Las personas beneficiadas por el proyecto de viviendas sociales serán: {valor_objetivo}\n")

print("Para lograr este valor se deben construir en los siguientes terrenos los edificios respectivos.\n")

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