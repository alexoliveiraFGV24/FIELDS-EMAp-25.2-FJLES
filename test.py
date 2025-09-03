from utils.get_probs_hist import *
from utils.get_samples import *

n=80
x = gerar_amostra(n)

# utis1 = previsao_permutacao(x)
utis2, t2 = previsao_permutacao(x, n-2)
utis3, t3 = previsao_rna_fft(x, n-2)

# print(utis1)
print(utis2)
print(utis3)
print("")
print(t2)
print(t3)
