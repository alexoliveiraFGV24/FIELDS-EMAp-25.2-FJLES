import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from matplotlib import pyplot as plt
import seaborn as sns



def modelo_linear_stacking(matrix_validation):
    
    y_true = matrix_validation[:, 0]
    X_meta = matrix_validation[:, 2:4].astype(float) 
    
    pipe_linear = Pipeline([
        ('scaler', StandardScaler()),
        ('meta_model', LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42))
    ])
    
    pipe_linear.fit(X_meta, y_true)
    
    return pipe_linear

def modelo_quadratico_stacking(matrix_validation):
    
    y_true = matrix_validation[:, 0]
    X_meta = matrix_validation[:, 2:4].astype(float) 
    
    pipe_quadratico = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('scaler', StandardScaler()),
        ('meta_model', LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42))
    ])
    
    pipe_quadratico.fit(X_meta, y_true)
    
    return pipe_quadratico


df = pd.read_csv('files/data/val_fechamentos_e_probabilities.csv')

df_filtrado = df[['MOV_TIPO_LEITO', 'Alta', 'UI','UTI']]



def gerar_visualizacao_linha_tempo(caminho_val, caminho_teste, coluna_hora):

    try:
        df_val = pd.read_csv(caminho_val)
    except FileNotFoundError:
        print(f"Erro: Arquivo de validação '{caminho_val}' não encontrado.")
        return

    colunas_stacking = ['MOV_TIPO_LEITO', 'Alta', 'UI', 'UTI']
    
    try:
        df_val_filtrado = df_val[colunas_stacking]
        matrix_val = df_val_filtrado.to_numpy()
    except KeyError:
        print(f"Erro: Colunas {colunas_stacking} não encontradas no arquivo de validação.")
        return

    modelo_linear = modelo_linear_stacking(matrix_val)
    modelo_quadratico = modelo_quadratico_stacking(matrix_val)

    try:
        df_test = pd.read_csv(caminho_teste)
    except FileNotFoundError:
        print(f"Erro: Arquivo de teste '{caminho_teste}' não encontrado.")
        return

    colunas_necessarias_teste = colunas_stacking + [coluna_hora]
    if not all(col in df_test.columns for col in colunas_necessarias_teste):
        print(f"Erro: O arquivo de teste deve conter as colunas: {colunas_necessarias_teste}")
        return
        
    df_test_filtrado = df_test[colunas_necessarias_teste].copy()

    linhas_invalidas = df_test_filtrado[coluna_hora].isna().sum()
    if linhas_invalidas > 0:
        print(f"Aviso: Removendo {linhas_invalidas} linhas com '{coluna_hora}' nula.")
        df_test_filtrado = df_test_filtrado.dropna(subset=[coluna_hora])
        
    X_meta_test = df_test_filtrado[['UI', 'UTI']].astype(float).to_numpy()

    mapa_outcomes = {
        0.0: 'Alta',
        1.0: 'UI',
        10.0: 'UTI'
    }
    
    y_pred_linear_num = modelo_linear.predict(X_meta_test)
    y_pred_quad_num = modelo_quadratico.predict(X_meta_test)
    y_realizado_num = df_test_filtrado['MOV_TIPO_LEITO'] 

    df_resultados = pd.DataFrame({
        'Hora': df_test_filtrado[coluna_hora].astype(int),
        
        'Original': df_test_filtrado[['Alta', 'UI', 'UTI']].idxmax(axis=1),
        
        'Realizado': y_realizado_num.map(mapa_outcomes),
        'Linear': pd.Series(y_pred_linear_num).map(mapa_outcomes),
        'Quadrático': pd.Series(y_pred_quad_num).map(mapa_outcomes)
    })

    df_long = df_resultados.melt(
        id_vars=['Hora'], 
        value_vars=['Realizado', 'Original', 'Linear', 'Quadrático'],
        var_name='Tipo',  
        value_name='Outcome' 
    )

    df_agg = df_long.groupby(['Hora', 'Tipo', 'Outcome']).size().reset_index(name='Contagem')


    if df_agg.empty:
        print("="*50)
        print("ERRO: O DataFrame agregado está vazio.")
        print("Isso pode acontecer se o 'mapa_outcomes' ainda estiver incorreto.")
        print("Valores únicos em 'MOV_TIPO_LEITO':", df_test_filtrado['MOV_TIPO_LEITO'].unique())
        print("Valores únicos em 'y_pred_linear_num':", np.unique(y_pred_linear_num))
        print("="*50)
        return

    g = sns.relplot(
        data=df_agg,
        x='Hora',
        y='Contagem',
        hue='Tipo',      
        col='Outcome',    
        kind='line',      
        col_wrap=1,      
        height=4,        
        aspect=3,        
        col_order=['Alta', 'UI', 'UTI'], 
        hue_order=['Realizado', 'Original', 'Linear', 'Quadrático'], 
        style='Tipo',  
        markers=True,
        dashes=False
    )
    
    g.set_axis_labels("Hora do Dia", "Contagem de Pacientes")
    g.set_titles("Distribuição por Hora - Outcome: {col_name}")
    g.set(xticks=range(0, 24))
    g.fig.suptitle('Previsão vs. Realizado por Hora do Dia', fontsize=16, y=1.03)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    
    CAMINHO_VALIDACAO = 'files/data/val_fechamentos_e_probabilities.csv'
    CAMINHO_TESTE = 'files/data/test_fechamentos_e_probabilities.csv'

    COLUNA_HORA = 'Hora'

    gerar_visualizacao_linha_tempo(CAMINHO_VALIDACAO, CAMINHO_TESTE, COLUNA_HORA)
    