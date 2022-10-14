def obtener_Yt():
    with open("datos/Yt.csv") as archivo:
        cumple = archivo.readline()
        cumple = cumple.strip().split(',')
        cumple = list(map(lambda x: int(x), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_Yt()
    diccionario = {(t): cumple[t - 1] for t in range(1, 2000 + 1)}
    print(diccionario)