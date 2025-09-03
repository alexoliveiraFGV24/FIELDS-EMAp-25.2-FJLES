import numpy as np


p_list = np.array(np.random.rand(10))
p_list = np.array([0.5, 0.5, 0.5, 0.5, 0.5])

pmf = np.array([1 - p_list[0], p_list[0]])


def convolve(fmp, vetor_aplicado):
    result = [0] * (len(fmp) + len(vetor_aplicado) - 1)

    for i, a in enumerate(fmp):
        for j, b in enumerate(vetor_aplicado):
            result[i + j] += a * b

    return np.array(result)

for p in p_list[1:]:
    pmf = convolve(pmf, [1 - p, p])


for k, prob in enumerate(pmf):
    print(f"P(S={k}) = {prob}")

