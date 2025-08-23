from utils.poibin import PoiBin
import numpy as np
from utils.get_probs_hist import *
from utils.get_samples import *

n=6
x = gerar_amostra(n=n)

uti = x[:,0]
pb = PoiBin(uti)

utis1 = np.zeros(x.shape[0])

for i in range(x.shape[0]):
    utis1[i] = pb.pmf(i)

utis2 = previsao(pacientes=x, utis=n-1)[0]

print(f"utis1 = {utis1}")
print(f"utis2 = {utis2}")
print(np.linalg.norm(utis1 - utis2))


