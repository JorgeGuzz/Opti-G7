def obtener_XS3ts():
    with open("datos/XS3ts.csv") as archivo:
        cumple = archivo.readlines()
        cumple = list(map(lambda x: x.strip().split(','), cumple))
        cumple = list(map(lambda x: list(map(lambda y: int(y), x)), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_XS3ts()
    diccionario = {(t, s): cumple[t - 1][s - 1] for t in range(1, 2000 + 1) for s in range(1, 600 + 1)}
    print(diccionario)