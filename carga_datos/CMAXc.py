def obtener_CMAXc():
    with open("datos/CMAXc.csv") as archivo:
        archivo.readline()
        cumple = archivo.readlines()
        cumple = list(map(lambda x: int(x.strip().split(",")[1]), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_CMAXc()
    diccionario = {(d): cumple[d - 1] for d in range(1, 6 + 1)}
    print(diccionario)