def obtener_ELIMci():
    with open("datos/ELIMci.csv") as archivo:
        cumple = archivo.readlines()
        cumple = list(map(lambda x: x.strip().split(','), cumple))
        cumple = list(map(lambda x: list(map(lambda y: int(y), x)), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_ELIMci()
    diccionario = {(c, i): cumple[c - 1][i - 1] for c in range(1, 6 + 1) for i in range(1, 10 + 1)}
    print(diccionario)