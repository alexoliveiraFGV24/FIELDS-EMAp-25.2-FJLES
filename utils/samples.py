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
    Preenche os próximos 5 índices (circular) do vetor pacientes_futuro
    usando a métrica escolhida.

    parâmetros:
    - pacientes_passado: array (24,) com dados até agora (passado/historico)
    - pacientes_futuro: array (24,) com valores futuros (ás vezes zeros)
    - horario_atual: int 0..23
    - metric: "mean"|"median"|"ema"|"weighted"|"rolling"|"trend"
    - include_future: se True, cada previsão é incorporada antes da próxima (forecast acumulado)
    - k: número de observações recentes a usar (para rolling ou trend)
    - ema_alpha: alpha da EMA (0<alpha<=1), maior alpha → mais peso no recente
    - weights: array de pesos (se metric == "weighted"), comprimento usado automaticamente
    """
    assert len(pacientes_passado) == 24 and len(pacientes_futuro) == 24
    y = pacientes_futuro.copy().astype(float)

    # helper para pegar últimos n valores do "histórico conhecido"
    def get_recent_values(include_predicted=False, n= k):
        vals = []
        # coletar da hora 0 até horario_atual inclusive -> histórico conhecido
        for i in range(horario_atual + 1):
            vals.append(pacientes_passado[i])
        # se incluir previsões já feitas, buscar em y (apenas índices > horario_atual)
        if include_predicted:
            # pegar valores já preenchidos em y que correspondem a previsões feitas
            # isto assume que previsões já foram colocadas em y
            # não filtramos zeros automaticamente; assumimos y contém previsões reais
            for i in range(24):
                # adicionar previsões que estão depois do horario_atual (em tempo circular)
                # mas aqui só queremos os últimos n valores no tempo — montar sequência temporal:
                pass
        # para simplicidade nas métricas, retornamos a sequência histórica completa até agora
        return np.array(vals)

    # Construir base de dados para a métrica:
    history = np.array([pacientes_passado[i] for i in range(horario_atual+1)])

    # função para obter ponto de previsão único dependendo da métrica
    def predict_point(history_vals, produced_vals):
        # history_vals: numpy array com dados históricos (0..horario_atual)
        # produced_vals: lista com previsões já geradas (se include_future True)
        if metric == "mean":
            base = np.mean(np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals)
            return base
        elif metric == "median":
            base = np.median(np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals)
            return base
        elif metric == "ema":
            # EMA sobre history then incorporate produced_vals if include_future
            seq = np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals
            # calcular EMA manualmente
            ema = seq[0]
            for v in seq[1:]:
                ema = ema * (1 - ema_alpha) + v * ema_alpha
            return ema
        elif metric == "weighted":
            seq = np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals
            n = len(seq)
            if weights is None:
                # pesos decrescentes lineares: mais peso para o mais recente
                w = np.arange(1, n+1)[::-1]  # ex: [n, n-1, ..., 1]
            else:
                w = np.array(weights[-n:])  # pega últimos n pesos dados
            return np.dot(seq, w) / np.sum(w)
        elif metric == "rolling":
            seq = np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals
            window = min(k, len(seq))
            return np.mean(seq[-window:])
        elif metric == "trend":
            seq = np.concatenate([history_vals, np.array(produced_vals)]) if include_future and produced_vals else history_vals
            n = len(seq)
            if n < 2:
                return float(seq[-1])
            # x: 0..n-1, y: seq, ajustar reta e extrapolar 1 passo à frente
            x = np.arange(n)
            coeffs = np.polyfit(x, seq, 1)  # linear
            slope, intercept = coeffs[0], coeffs[1]
            # previsão para o próximo ponto = y(n) where x = n
            return slope * n + intercept
        else:
            raise ValueError("Métrica desconhecida.")

    # gerar 5 previsões sequenciais (com ou sem usar previsões anteriores)
    produced = []
    for i in range(1, 6):
        idx = (horario_atual + i) % 24
        val = predict_point(history, produced)
        y[idx] = val
        produced.append(val)
        if include_future:
            # se incluímos previsões nos cálculos seguintes, também podemos considerá-las
            # nada a fazer: produced já contém elas
            pass

    return y

if __name__ == "__main__":
    print(obter_previsoes(0, 14))