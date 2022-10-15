def obtener_STt():
    with open("datos/STt.csv") as archivo:
        cumple = archivo.readlines()
        cumple.pop(0)
        cumple = list(map(lambda x: x.strip(), cumple))
        cumple = list(map(lambda x: int(x), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_STt()
    diccionario = {(i): cumple[i - 1] for i in range(1, 2000 + 1)}
    print(diccionario)