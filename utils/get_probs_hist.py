import numpy as np
import time
from itertools import product
from scipy.stats import norm
from .get_samples import *



def previsao_permutacao(pacientes:np.array, utis:int=4, internacoes:int=4, altas:int=4, threshold:float=0):
    
    # Iniciando contador de tempo
    t = time.time()
    
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
        if not np.isclose(sum(paciente), 1):
            return "Não pode"
    
    # Distribuições marginais (incluindo o caso 0)
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
    
    # Finalizo a contagem de tempo
    t = time.time() - t
    
    # Retorno
    return probs_utis, probs_internacoes, probs_altas, t



def previsao_recursiva(pacientes: np.ndarray, utis: int=4, internacoes: int=4, altas: int=4, threshold:float=0):
    
    # Iniciando contador de tempo
    t = time.time()

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
        if not np.isclose(sum(paciente), 1):
            return "Não pode"
    
    # Distribuições marginais (incluindo o caso 0)
    probs_utis = np.zeros(utis+1)
    probs_internacoes = np.zeros(internacoes+1)
    probs_altas = np.zeros(altas+1)
    
    # Função auxiliar para percorrer todos os pacientes recursivamente
    def backtrack(idx, u, i, a, prob):
        # Se já ultrapassou os limites, para
        if u > utis or i > internacoes or a > altas:
            return
        # Caso base: percorreu todos os pacientes, para
        if idx == num_pacientes:
            probs_utis[u] += prob
            probs_internacoes[i] += prob
            probs_altas[a] += prob
            return
        # Paciente atual pode ir para UTI, Internação ou Alta
        p_u, p_i, p_a = pacientes[idx]
        backtrack(idx+1, u+1, i, a, prob * p_u)  # vai para UTI
        backtrack(idx+1, u, i+1, a, prob * p_i)  # vai para Internação
        backtrack(idx+1, u, i, a+1, prob * p_a)  # vai para Alta
    
    # Inicia no primeiro paciente (idx=0)
    backtrack(0, 0, 0, 0, 1.0)
    
    # Verificação para o threshold passado
    probs_utis[probs_utis < threshold] = 0
    probs_internacoes[probs_internacoes < threshold] = 0
    probs_altas[probs_altas < threshold] = 0
    
    # Finalizo a contagem de tempo
    t = time.time() - t
    
    # Retorno    
    return probs_utis, probs_internacoes, probs_altas, t



def previsao_convolucao(pacientes: np.ndarray, threshold:float=0, lim_leitos = False, prob_disj = True):
    
    # Definindo limites de calculo (a implementar)
    if not lim_leitos:
        lim_leitos = pacientes.shape[0]


    # Iniciando contador de tempo
    t = time.time()

    # Número de pacientes
    num_pacientes = pacientes.shape[0]
    
    # Verificações básicas

    if (pacientes.shape[1] != 3):
        return "Verifique o formato do array"
    
    for paciente in pacientes:
        if not np.isclose(sum(paciente), 1):
            return "Inconsistência no vetor de probabilidade de algum paciente!"
        
    pacientes[pacientes<threshold] = 0
    # Vetores de probabilidades
    probs_utis = pacientes[:,0]
    probs_internacao = pacientes[:,1]
    probs_altas = pacientes[:,2]
    

    
    # Função auxiliar para convolução
    def convolve(fmp, vetor_aplicado):
        result = [0] * (len(fmp) + len(vetor_aplicado) - 1)
        for i, a in enumerate(fmp):
            for j, b in enumerate(vetor_aplicado):
                result[i + j] += a * b
        return np.array(result)
    

    #histograma uti:
    dist_uti = np.array([1 - probs_utis[0], probs_utis[0]])

    for p in probs_utis[1:]:
        dist_uti = convolve(dist_uti, [1 - p, p])


    #histograma internacao:
    dist_internacao = np.array([1 - probs_internacao[0], probs_internacao[0]])

    for p in probs_internacao[1:]:
        dist_internacao = convolve(dist_internacao, [1-p, p])

    #histograma alta:
    dist_altas = np.array([1-probs_altas[0], probs_altas[0]])

    for p in probs_altas[1:]:
        dist_altas = convolve(dist_altas, [1-p,p])

    #prints
    print("Distribuição uti: ", dist_uti)

    print("Distribuição internação: ", dist_internacao)

    print("Distribuição alta: ", dist_altas)

        
    
    # Finalizo a contagem de tempo
    t = time.time() - t
    
    # Retorno
    return dist_uti, dist_internacao, dist_altas, t



def previsao_rna_fft(pacientes: np.ndarray, utis: int=4, internacoes: int=4, altas: int=4, threshold:float=0):


    t = time.time()
    num_pacientes = pacientes.shape[0]
    
    # Verificações básicas
    if (utis <= 0 or internacoes <= 0 or altas <= 0 or threshold > 1):
        return "Não pode"
    if (utis > num_pacientes or internacoes > num_pacientes or altas > num_pacientes):
        return "Não pode"
    if (pacientes.shape[1] != 3):
        return "Não pode"
    for paciente in pacientes:
        if not np.isclose(sum(paciente), 1):
            return "Não pode"
    
    # Vetores de probabilidades
    probs_utis_bruto = pacientes[:,0]
    probs_internacoes_bruto = pacientes[:,1]
    probs_altas_bruto = pacientes[:,2]
    
    # Variáveis de interesse para aproximação Poisson Binomial
    mu_utis = np.sum(probs_utis_bruto)
    mu_internacoes = np.sum(probs_internacoes_bruto)  
    mu_altas = np.sum(probs_altas_bruto)
    
    ro_utis = np.sqrt(np.sum(probs_utis_bruto*(1-probs_utis_bruto)))
    ro_internacoes = np.sqrt(np.sum(probs_internacoes_bruto*(1-probs_internacoes_bruto)))
    ro_altas = np.sqrt(np.sum(probs_altas_bruto*(1-probs_altas_bruto)))
    
    gamma_utis = np.sum(probs_utis_bruto*(1-probs_utis_bruto)*(1-2*probs_utis_bruto)) / (ro_utis**3)
    gamma_internacoes = np.sum(probs_internacoes_bruto*(1-probs_internacoes_bruto)*(1-2*probs_internacoes_bruto)) / (ro_internacoes**3)
    gamma_altas = np.sum(probs_altas_bruto*(1-probs_altas_bruto)*(1-2*probs_altas_bruto)) / (ro_altas**3)
    
    # Função da RNA (aproximação Edgeworth)
    def G(k, mu, ro, gamma):
        x = (k + 0.5 - mu)/ro
        return norm.cdf(x) - norm.pdf(x) * (gamma * (1 - x**2) / 6)
    
    # Probabilidades (cumulativas)
    probs_utis = np.array([G(k, mu_utis, ro_utis, gamma_utis) - G(k-1, mu_utis, ro_utis, gamma_utis) for k in range(utis+1)])
    probs_internacoes = np.array([G(k, mu_internacoes, ro_internacoes, gamma_internacoes) - G(k-1, mu_internacoes, ro_internacoes, gamma_internacoes)for k in range(internacoes+1)])
    probs_altas = np.array([G(k, mu_altas, ro_altas, gamma_altas) - G(k-1, mu_altas, ro_altas, gamma_altas)for k in range(altas+1)])
    
    # Garantir que está no intervalo [0,1]
    probs_utis = np.clip(probs_utis, 0, 1)
    probs_internacoes = np.clip(probs_internacoes, 0, 1)
    probs_altas = np.clip(probs_altas, 0, 1)
    
    # Threshold
    probs_utis[probs_utis < threshold] = 0
    probs_internacoes[probs_internacoes < threshold] = 0
    probs_altas[probs_altas < threshold] = 0
    
    # Finalizo a contagem de tempo
    t = time.time() - t
    
    # Retorno
    return probs_utis, probs_internacoes, probs_altas, t





