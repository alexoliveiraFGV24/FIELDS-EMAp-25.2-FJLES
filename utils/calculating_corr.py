import pandas as pd
import numpy as np
from probs import previsao_convolucao

def calcular_metricas_grupo(group):
    """
    Função auxiliar para ser usada com .apply()
    Calcula as 3 métricas (Real, idxmax, Conv) para um 
    grupo específico de (Dia, Hora).
    """
    
    mapa_outcomes = {
        0.0: 'Alta',
        1.0: 'UI',
        10.0: 'UTI'
    }
    colunas_outcomes = ['Alta', 'UI', 'UTI']
    colunas_conv_input = ['UTI', 'UI', 'Alta'] # Ordem para a convolução
    all_outcomes = ['Alta', 'UI', 'UTI'] # Ordem padrão
    
    # --- 1. Contagem Realizado ---
    # .value_counts() conta as ocorrências de cada outcome
    # .reindex() garante que 'Alta', 'UI', 'UTI' sempre existam, preenchendo com 0
    real_counts = group['MOV_TIPO_LEITO'].map(mapa_outcomes).value_counts() \
                    .reindex(all_outcomes).fillna(0)

    # --- 2. Contagem idxmax ---
    idxmax_counts = group[colunas_outcomes].idxmax(axis=1).value_counts() \
                      .reindex(all_outcomes).fillna(0)

    # --- 3. Contagem Convolução (Valor Esperado) ---
    prob_pacientes = group[colunas_conv_input].values
    
    try:
        # Chama a convolução para este pequeno grupo (um dia, uma hora)
        _, _, (mean_uti, mean_ui, mean_alta) = previsao_convolucao(prob_pacientes)
        
        # Mapeia os resultados para uma Série (com a ordem correta)
        conv_counts = pd.Series({'Alta': mean_alta, 'UI': mean_ui, 'UTI': mean_uti})
    
    except Exception as e:
        print(f"Erro na convolução do grupo: {e}. Zerando valores.")
        conv_counts = pd.Series({'Alta': 0.0, 'UI': 0.0, 'UTI': 0.0})

    # --- Combina os resultados ---
    # Renomeia os índices para evitar colisão (ex: 'Alta' -> 'Real_Alta')
    real_counts.rename(lambda x: f'Real_{x}', inplace=True)
    idxmax_counts.rename(lambda x: f'idxmax_{x}', inplace=True)
    conv_counts.rename(lambda x: f'Conv_{x}', inplace=True)
    
    # Retorna uma única série com 9 valores (3 métricas * 3 outcomes)
    return pd.concat([real_counts, idxmax_counts, conv_counts])


def calcular_medias_horarias(caminho_arquivo, coluna_hora, coluna_dia):
    """
    Orquestra o processo de cálculo das médias horárias.
    
    1. Carrega dados.
    2. Agrupa por [Dia, Hora].
    3. Aplica a função 'calcular_metricas_grupo' para obter contagens diárias/horárias.
    4. Agrupa o resultado por [Hora] e calcula a média.
    
    Retorna:
        Um DataFrame com 24 linhas (horas) e 9 colunas (métricas).
    """
    
    colunas_outcomes = ['Alta', 'UI', 'UTI']
    colunas_base = ['MOV_TIPO_LEITO']
    
    try:
        df_full = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    colunas_necessarias = colunas_base + colunas_outcomes + [coluna_hora, coluna_dia]
    if not all(col in df_full.columns for col in colunas_necessarias):
        print(f"Erro: O arquivo deve conter as colunas: {colunas_necessarias}")
        return None
        
    df_filtrado = df_full[colunas_necessarias].copy()

    # Limpeza de dados nulos
    linhas_invalidas = df_filtrado[coluna_hora].isna().sum()
    if linhas_invalidas > 0:
        print(f"Aviso: Removendo {linhas_invalidas} linhas com '{coluna_hora}' nula.")
        df_filtrado = df_filtrado.dropna(subset=[coluna_hora])
    
    if df_filtrado.empty:
        print("Erro: Nenhum dado válido restante após a limpeza.")
        return None

    # Garante que a hora é int para o groupby
    df_filtrado[coluna_hora] = df_filtrado[coluna_hora].astype(int)

    # --- Passo 1: Agrupar por [Dia, Hora] e aplicar os cálculos ---
    # para CADA combinação única de dia e hora.
    df_day_hour_agg = df_filtrado.groupby([coluna_dia, coluna_hora]) \
                                 .apply(calcular_metricas_grupo)
    
    df_day_hour_agg = df_day_hour_agg.reset_index()


    # --- Passo 2: Calcular a média por hora ---

    
    # Pega todas as colunas que NÃO são 'Dia' ou 'Hora'
    col_metricas = list(df_day_hour_agg.columns.drop([coluna_dia, coluna_hora]))
    
    df_final_mean = df_day_hour_agg.groupby(coluna_hora)[col_metricas].mean()
    

    
    return df_final_mean

CAMINHO_ARQUIVO = 'files/data/test_fechamentos_e_probabilities.csv'
COLUNA_HORA = 'Hora'
COLUNA_DIA = 'Dia' 

df_medias = calcular_medias_horarias(CAMINHO_ARQUIVO, COLUNA_HORA, COLUNA_DIA)

medias = df_medias[['Real_Alta', 'Real_UI', 'Real_UTI']]

print(medias)

medias.to_csv(f"medias.csv", index=False)


