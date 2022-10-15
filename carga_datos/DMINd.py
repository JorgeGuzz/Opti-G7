def obtener_DMINd():
    with open("datos/DMINd.csv") as archivo:
        archivo.readline()
        cumple = archivo.readlines()
        cumple = list(map(lambda x: int(x.strip().split(",")[1]), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_DMINd()
    diccionario = {(d): cumple[d - 1] for d in range(1, 8 + 1)}
    print(diccionario)