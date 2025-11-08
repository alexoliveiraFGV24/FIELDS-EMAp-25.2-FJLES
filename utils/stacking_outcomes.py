import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from probs import previsao_convolucao


def calcular_metricas_grupo(caminho_dataset, agregacao="hora" , nome_arquivo="data_frame", salvar=False):
    '''
    recebe um dataset com as colunas: TA_DH_PRE_ATENDIMENTO,Dia,Hora,MOV_TIPO_LEITO,Alta,UI,UTI

    e retorna um dataset do tipo: dia, hora, numero observado altas, ui e uti, numero previsto altas, ui e uti

    '''

    data_frame = pd.read_csv(caminho_dataset)
    data_frame = data_frame.sort_values(by='TA_DH_PRE_ATENDIMENTO')

    if agregacao.lower() == '6h':
        data_frame['Hora'] = (data_frame['Hora'] // 6) * 6

    elif agregacao.lower() == 'dia':
        data_frame['Hora'] = 0

    grupos = data_frame.groupby(['Dia','Hora'])
    linhas = []

    for (dia, hora), grupo in grupos:
        num_observado_altas = (grupo['MOV_TIPO_LEITO'] == 0).sum()
        num_observado_ui = (grupo['MOV_TIPO_LEITO'] == 1).sum()
        num_observado_uti = (grupo['MOV_TIPO_LEITO'] == 10).sum()
        previsto_uti = grupo['UTI'].sum()
        previsto_ui = grupo['UI'].sum()
        previsto_alta = grupo['Alta'].sum()
        
        linhas.append({
            'Dia':dia,
            'Hora': hora,
            'num_observado_altas': num_observado_altas,
            'num_observado_ui': num_observado_ui,
            'num_observado_uti': num_observado_uti,
            'num_previsto_altas': previsto_alta,
            'num_previsto_ui': previsto_ui,
            'num_previsto_uti': previsto_uti
        })

    data_frame_agg = pd.DataFrame(linhas)

    if agregacao.lower() == 'dia':
        data_frame = data_frame.drop(columns=['Hora'])

    if agregacao.lower() in ['hora', '6h', 'dia']:
        if salvar:
            data_frame_agg.to_csv(f'{nome_arquivo}.csv', index=False)
        
        return data_frame_agg        
    else:
        print('verifique a agregacao escolhida!')
        return None
    pass

def visualizacao(data_set, agregacao="hora", titulo=" "):
    
    if isinstance(data_set, str):
        df = pd.read_csv(data_set)
    else:
        df = data_set

    if agregacao.lower() == 'dia':
        eixo_x = df['Dia']
        
    elif agregacao.lower() == '6h':
        eixo_x = df['Dia'].astype(str) + ' ' + df['Hora'].astype(str) + 'h'
        
    else:
        eixo_x = df['Dia'].astype(str) + ' ' + df['Hora'].astype(str) + 'h'
        

    corr_alta = df['num_observado_altas'].corr(df['num_previsto_altas'])
    corr_ui = df['num_observado_ui'].corr(df['num_previsto_ui'])
    corr_uti = df['num_observado_uti'].corr(df['num_previsto_uti'])

    fig, axes = plt.subplots(3, 1, figsize=(10, 5), sharex=True)


    axes[0].plot(eixo_x, df['num_observado_altas'], label='observado')
    axes[0].plot(eixo_x, df['num_previsto_altas'], label='previsto', alpha=0.8)
    axes[0].set_title(f'Altas (correlação Real x Previsto ={corr_alta:.3f})')
    axes[0].legend()
    axes[0].tick_params(axis='x', rotation=90)

    axes[1].plot(eixo_x, df['num_observado_ui'], label='observado')
    axes[1].plot(eixo_x, df['num_previsto_ui'], label='previsto', alpha=0.8)
    axes[1].set_title(f'UI (correlação Real x Previsto ={corr_ui:.3f})')
    axes[1].legend()
    axes[1].tick_params(axis='x', rotation=90)

    axes[2].plot(eixo_x, df['num_observado_uti'], label='observado')
    axes[2].plot(eixo_x, df['num_previsto_uti'], label='previsto', alpha=0.8)
    axes[2].set_title(f'UTI (correlação Real x Previsto ={corr_uti:.3f})')
    axes[2].legend()
    axes[2].tick_params(axis='x', rotation=90)

    axes[0].set_xticks([])
    axes[1].set_xticks([])
    axes[2].set_xticks([])


    fig.suptitle(titulo)
    plt.tight_layout()
    plt.savefig(f'{titulo}.png')
    #plt.show()


def visualizacao_alta_naoalta(data_set, agregacao="hora", titulo=" "):
    
    if isinstance(data_set, str):
        df = pd.read_csv(data_set)
    else:
        df = data_set

    # Define eixo X
    if agregacao.lower() == 'dia':
        eixo_x = df['Dia']
    elif agregacao.lower() == '6h':
        eixo_x = df['Dia'].astype(str) + ' ' + df['Hora'].astype(str) + 'h'
    else:
        eixo_x = df['Dia'].astype(str) + ' ' + df['Hora'].astype(str) + 'h'
        
    # Cria colunas somadas UI + UTI
    df['num_observado_naoalta'] = df['num_observado_ui'] + df['num_observado_uti']
    df['num_previsto_naoalta'] = df['num_previsto_ui'] + df['num_previsto_uti']

    # Correlações
    corr_alta = df['num_observado_altas'].corr(df['num_previsto_altas'])
    corr_naoalta = df['num_observado_naoalta'].corr(df['num_previsto_naoalta'])

    # Gráficos
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Altas
    axes[0].plot(eixo_x, df['num_observado_altas'], label='Observado', alpha=0.8,  linewidth=1.5)
    axes[0].plot(eixo_x, df['num_previsto_altas'], label='Previsto', alpha=0.7, linewidth=1.0)
    axes[0].set_title(f'Altas (Correlação Real x Previsto = {corr_alta:.3f})')
    axes[0].legend()
    axes[0].tick_params(axis='x', rotation=90)

    # UI + UTI (Não Altas)
    axes[1].plot(eixo_x, df['num_observado_naoalta'], label='Observado', alpha=0.8, linewidth=1.5)
    axes[1].plot(eixo_x, df['num_previsto_naoalta'], label='Previsto', alpha=0.7, linewidth=1)
    axes[1].set_title(f'UI + UTI (Correlação Real x Previsto = {corr_naoalta:.3f})')
    axes[1].legend()
    axes[1].tick_params(axis='x', rotation=90)

    axes[0].set_xticks([])
    axes[1].set_xticks([])

    fig.suptitle(titulo)
    plt.tight_layout()
    plt.savefig(f'{titulo}.png')
    #plt.show()


if __name__ == "__main__":

    for each in ['dia', '6h', 'hora']:

        dataset = calcular_metricas_grupo('files/data/val_fechamentos_e_probabilities.csv', each, nome_arquivo=f"{each}")

        visualizacao_alta_naoalta(dataset, each, titulo=f"Validation agregado hierarquico - {each}")

    