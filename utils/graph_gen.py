#imports

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


#configurando data sets
desfechos_test = pd.read_csv('files\data\desfechos_test_dataset.csv')
desfechos_train = pd.read_csv('files\data\desfechos_train_dataset.csv')
desfechos_validation = pd.read_csv('files\data\desfechos_val_dataset.csv')

desfechos_total = pd.read_csv('files\data\desfechos_todos_dataset.csv')

probabilidades_lr = pd.read_csv('files\data\probabilidades_lr.csv')
probabilidades_rf = pd.read_csv('files\data\probabilidades_rf.csv')

#visualizações

prob_cols = ['prediction_prob_alta', 'prediction_prob_ui', 'prediction_prob_uti']

df_limpo = probabilidades_lr.dropna(subset=prob_cols).copy()

df_limpo.loc[:, 'PREVISTO'] = df_limpo[prob_cols].idxmax(axis=1).str.replace('prediction_prob_', '')



df_final = df_limpo.drop(columns=prob_cols)
df_final.loc[:, 'actual_class'] = np.nan

df_final.loc[df_final['MOV_TIPO_LEITO'] == 0.0, 'actual_class'] = 'alta'
df_final.loc[df_final['MOV_TIPO_LEITO'] == 1.0, 'actual_class'] = 'ui'
df_final.loc[df_final['MOV_TIPO_LEITO'] == 10.0, 'actual_class'] = 'uti'


print(df_final[['actual_class', 'PREVISTO']].head())







