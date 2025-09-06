import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import probs 

data = pd.read_csv('files/data/probabilidades.csv')


result = probs.previsao_convolucao(data[['prediction_prob_alta', 'prediction_prob_ui','prediction_prob_uti']][:20000].values)

plt.plot(result[1])
plt.show()
