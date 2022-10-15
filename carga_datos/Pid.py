def obtener_Pid():
    with open("datos/Pid.csv") as archivo:
        cumple = archivo.readlines()
        cumple = list(map(lambda x: x.strip().split(','), cumple))
        cumple = list(map(lambda x: list(map(lambda y: int(y), x)), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_Pid()
    diccionario = {(t, s): cumple[t - 1][s - 1] for t in range(1, 10 + 1) for s in range(1, 8 + 1)}
    print(diccionario)