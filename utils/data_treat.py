import pandas as pd
import numpy as np
import plot

import probs 

data = pd.read_csv('files/data/probabilidades.csv')
n = 200
result = probs.previsao_convolucao(data[['prediction_prob_alta', 'prediction_prob_ui','prediction_prob_uti']][:n].values)

plot.plot_probs_acumul(result)
