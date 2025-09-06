import numpy as np

def gerar_amostra(n:int, low:int=1, high:int=1001):
    pacientes = np.zeros((n, 3))
    for i in range(n):
        numeros = np.random.randint(low, high, size=3)
        numeros = numeros / np.sum(numeros)
        pacientes[i] = numeros
        
    return pacientes


