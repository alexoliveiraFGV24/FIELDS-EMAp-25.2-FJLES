import numpy as np
import pandas as pd
from utils import probs 


def gerar_amostra(n:int, low:int=1, high:int=1001):
    pacientes = np.zeros((n, 3))
    for i in range(n):
        numeros = np.random.randint(low, high, size=3)
        numeros = numeros / np.sum(numeros)
        pacientes[i] = numeros
        
    return pacientes


data = pd.read_csv('files/data/probabilidades.csv')
data_horarios = data[['TA_DH_PRE_ATENDIMENTO']].values
data_probs = data[['prediction_prob_alta', 'prediction_prob_ui','prediction_prob_uti']].values


def obter_previsoes(indice_paciente_atual, horario_atual):
    """preenche os arrays de pacientes"""
    indice_paciente_final = indice_paciente_atual
    while (indice_paciente_final + 1 < len(data_horarios)):
        proximo_horario = int(data_horarios[indice_paciente_final + 1][0].split()[1][0:2])
        if proximo_horario != horario_atual:
            break
        indice_paciente_final += 1

    # Extrair probabilidades para o bloco de pacientes do mesmo horário
    bloco_probs = data_probs[indice_paciente_atual:indice_paciente_final + 1]

    # Calcular previsões via convolução
    _, results_cdf, mean_count = probs.previsao_convolucao(bloco_probs)

    previsoes = [mean_count[1], mean_count[2], mean_count[0]]

    return mean_count, results_cdf, indice_paciente_final + 1


def previsao_pacientes_futuro(
    pacientes_passado,
    pacientes_futuro,
    horario_atual,
    metric="mean",
    include_future=False,
    k=6,
    ema_alpha=0.3,
    weights=None
):
    """
    Preenche os próximos 5 índices (circular) do vetor pacientes_futuro (24x3)
    usando a métrica escolhida, aplicando a previsão separadamente para cada estado
    do paciente (coluna).

    parâmetros:
    - pacientes_passado: array (24, 3) com dados até agora (passado/historico)
    - pacientes_futuro: array (24, 3) com valores futuros (ás vezes zeros)
    - horario_atual: int 0..23
    - metric: "mean"|"median"|"ema"|"weighted"|"rolling"|"trend"
    - include_future: se True, cada previsão é incorporada antes da próxima (forecast acumulado)
    - k: número de observações recentes a usar (para rolling ou trend)
    - ema_alpha: alpha da EMA (0<alpha<=1), maior alpha → mais peso no recente
    - weights: array de pesos (se metric == "weighted"), comprimento usado automaticamente
    """
    assert pacientes_passado.shape == (24, 3) and pacientes_futuro.shape == (24, 3)
    
    # O resultado y será um array 24x3
    y = pacientes_futuro.copy().astype(float)
    
    # --------------------------------------------------------------------------
    # Sub-função de previsão para um array 1D (uma única coluna/estado)
    # Esta função encapsula toda a lógica original da métrica.
    # --------------------------------------------------------------------------
    def predict_single_column(column_history_vals, produced_vals):
        """
        Calcula um único ponto de previsão para uma série temporal (coluna).
        """
        
        # history_vals: numpy array com dados históricos (0..horario_atual) de UMA coluna
        # produced_vals: lista com previsões já geradas para a coluna
        
        if metric == "mean":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            return np.mean(seq).astype(np.uint8)
        
        elif metric == "median":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            return np.median(seq)
        
        elif metric == "ema":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            if not seq.size: return 0.0
            
            ema = seq[0]
            for v in seq[1:]:
                ema = ema * (1 - ema_alpha) + v * ema_alpha
            return ema
        
        elif metric == "weighted":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            if not seq.size: return 0.0

            n = len(seq)
            if weights is None:
                # pesos decrescentes lineares: mais peso para o mais recente
                w = np.arange(1, n+1)[::-1] 
            else:
                w = np.array(weights[-n:]) 
            
            y = np.dot(seq, w) / np.sum(w)

            
            return y.astype(np.uint8)
        
        elif metric == "rolling":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            if not seq.size: return 0.0
            
            window = min(k, len(seq))
            return np.mean(seq[-window:])
        
        elif metric == "trend":
            seq = np.concatenate([column_history_vals, np.array(produced_vals)]) if include_future and produced_vals else column_history_vals
            n = len(seq)
            if n < 2:
                return float(seq[-1]) if seq.size > 0 else 0.0
            
            x = np.arange(n)
            coeffs = np.polyfit(x, seq, 1)  # linear
            slope, intercept = coeffs[0], coeffs[1]
            # previsão para o próximo ponto = y(n) where x = n
            return slope * n + intercept
        
        else:
            raise ValueError("Métrica desconhecida.")
    # --------------------------------------------------------------------------

    # 3. Iterar sobre as 3 colunas (estados) e aplicar a previsão em cada uma.
    for col in range(3):
        
        # 3.1. Obter o histórico de dados (uma coluna, até a hora atual)
        # history é um array 1D com os valores da coluna 'col' da hora 0 até horario_atual.
        history_col = np.array([pacientes_passado[i, col] for i in range(horario_atual + 1)])
        
        # 3.2. Gerar 5 previsões sequenciais para esta coluna
        produced_col = []
        for i in range(1, 6):
            idx = (horario_atual + i) % 24
            
            # Calcular o próximo ponto de previsão usando a sub-função
            val = predict_single_column(history_col, produced_col)
            
            # Colocar o valor previsto no array de resultados na posição [hora, coluna]
            y[idx, col] = max(0, val) # Garantir que o volume não seja negativo
            
            # Se a previsão é cumulativa (include_future=True), guarde o valor para o próximo cálculo
            if include_future:
                produced_col.append(val)
                
    # Retorna o array 24x3 com as previsões futuras preenchidas
    return y

if __name__ == "__main__":
    print(obter_previsoes(0, 14))