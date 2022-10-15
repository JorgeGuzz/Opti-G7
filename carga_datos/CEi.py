def obtener_CEi():
    with open("datos/CEi.csv") as archivo:
        archivo.readline()
        cumple = archivo.readlines()
        cumple = list(map(lambda x: int(x.strip().split(",")[1]), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_CEi()
    diccionario = {(i): cumple[i - 1] for i in range(1, 10 + 1)}
    print(diccionario)