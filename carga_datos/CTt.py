def obtener_CTt():
    with open("datos/CTt.csv") as archivo:
        costo = archivo.readline()
        costo = costo.strip().split(',')
        costo = list(map(lambda x: int(x), costo))
    return costo

if __name__ == "__main__":
    costo = obtener_CTt()
    diccionario = {(t): costo[t - 1] for t in range(1, 2000 + 1)}
    print(diccionario)