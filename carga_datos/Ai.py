def obtener_Ai():
    with open("datos/Ai.csv") as archivo:
        archivo.readline()
        cumple = archivo.readlines()
        cumple = list(map(lambda x: float(x.strip().split(",")[1]), cumple))
    return cumple

if __name__ == "__main__":
    cumple = obtener_Ai()
    diccionario = {(i): cumple[i - 1] for i in range(1, 10 + 1)}
    print(diccionario)