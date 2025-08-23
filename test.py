from utils.poibin import PoiBin
import numpy as np

from itertools import product

x = np.random.rand(40)

pb = PoiBin(x)

def previsao(pacientes:np.array, utis:int=4, internacoes:int=4, altas:int=4, threshold:float=0):
    
    # Número de pacientes
    num_pacientes = pacientes.shape[0]

    # Verificações básicas
    if (utis <= 0 or internacoes <= 0 or altas <= 0 or threshold > 1):
        return "Não pode"
    if (utis > num_pacientes or internacoes > num_pacientes or altas > num_pacientes):
        return "Não pode"
    if (pacientes.shape[1] != 3):
        return "Não pode"
    for paciente in pacientes:
        if sum(paciente) != 1:
            return "Não pode"
    
    # Variáveis
    probs_utis = np.zeros(utis + 1)
    probs_internacoes = np.zeros(internacoes + 1)
    probs_altas = np.zeros(altas + 1)
    
    # Lógica para calcular as probabilidades e armazená-las nas listas (permutação dos estados, já que são eventos independentes)
    for estados in product([0,1,2], repeat=num_pacientes): # tupla (ex: (0,2,1,...)) representando UTI, Alta, Internação, ...
        prob = 1.0
        cont_u, cont_i, cont_a = 0, 0, 0
        for k, estado in enumerate(estados):
            prob *= pacientes[k, estado]
            if estado == 0:
                cont_u += 1
            elif estado == 1:
                cont_i += 1
            else:
                cont_a += 1
        # Acumula apenas se dentro dos limites
        if cont_u <= utis and cont_i <= internacoes and cont_a <= altas:
            probs_utis[cont_u] += prob
            probs_internacoes[cont_i] += prob
            probs_altas[cont_a] += prob
    
    # Verificação para o threshold passado
    probs_utis[probs_utis < threshold] = 0
    probs_internacoes[probs_internacoes < threshold] = 0
    probs_altas[probs_altas < threshold] = 0
        
    return probs_utis, probs_internacoes, probs_altas 

print(previsao(pacientes=x))