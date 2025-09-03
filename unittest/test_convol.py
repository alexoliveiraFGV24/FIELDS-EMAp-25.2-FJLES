import numpy as np
import pytest
from utils.get_probs_hist import previsao_convolucao  


def test_formato_incorreto():
    pacientes = np.array([[0.5, 0.5]])  # só 2 colunas
    resultado = previsao_convolucao(pacientes)
    assert resultado == "Verifique o formato do array"


def test_probabilidades_inconsistentes():
    pacientes = np.array([[0.5, 0.3, 0.3]])  # soma = 1.1
    resultado = previsao_convolucao(pacientes)
    assert resultado == "Inconsistência no vetor de probabilidade de algum paciente!"


def test_um_paciente_caso_simples():
    pacientes = np.array([[0.2, 0.3, 0.5]])  # um paciente
    dist_uti, dist_internacao, dist_altas, t = previsao_convolucao(pacientes)

    # Deve ser apenas uma bernoulli
    assert np.allclose(dist_uti, [0.8, 0.2])
    assert np.allclose(dist_internacao, [0.7, 0.3])
    assert np.allclose(dist_altas, [0.5, 0.5])


def test_dois_pacientes_mesma_prob():
    pacientes = np.array([
        [0.5, 0.25, 0.25],
        [0.5, 0.25, 0.25]
    ])
    dist_uti, dist_internacao, dist_altas, t = previsao_convolucao(pacientes)

   
    assert np.allclose(dist_uti, [0.25, 0.5, 0.25])
    
    assert np.allclose(dist_internacao, [0.5625, 0.375, 0.0625])
    assert np.allclose(dist_altas, [0.5625, 0.375, 0.0625])


def test_threshold_aplica_zero():
    pacientes = np.array([[0.01, 0.99, 0.0]])  
    dist_uti, dist_internacao, dist_altas, t = previsao_convolucao(pacientes, threshold=0.05)

    
    assert np.allclose(dist_uti, [1.0, 0.0])
    assert np.allclose(dist_internacao, [0.01, 0.99])



