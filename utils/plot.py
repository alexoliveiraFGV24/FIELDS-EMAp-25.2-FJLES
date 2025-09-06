import numpy as np
import matplotlib.pyplot as plt


def plot_probs_acumul(probs):
    cores = ['#9a031e', '#fb8b24', "#ad07db"]
    pmf = probs[0]
    cdf = probs[1]

    plt.figure(figsize=(8,8))
    
    plt.subplot(2,1,1)
    plt.plot(cdf[0], label="UTI", color=cores[0])
    plt.plot(cdf[1], label="INTERNACOES", color=cores[1])
    plt.plot(cdf[2], label="ALTAS", color=cores[2])
    plt.grid(visible=True, alpha=0.7)
    plt.title('Distribuições de Probabilidade Cumulativa (CDF)')
    plt.xlabel('k')
    plt.ylabel('$P(X > k)$')
    plt.legend()

    plt.subplot(2,3,4)
    plt.bar(np.arange(len(pmf[0])), pmf[0], width=0.8, label="UTI", color=cores[0] )
    plt.ylim(0,1)
    plt.legend()
    
    plt.subplot(2,3,5)
    plt.bar(np.arange(len(pmf[1])), pmf[1], width=0.8, label="INTERNACOES", color=cores[1])
    plt.title('Distribuições de Probabilidade de Massa (PMF)')
    plt.xlabel('k')
    plt.ylabel('$P(X = k)$')
    plt.ylim(0,1)
    plt.legend()
    
    plt.subplot(2,3,6)
    plt.bar(np.arange(len(pmf[2])), pmf[2], width=0.8, label="ALTAS", color=cores[2])
    plt.ylim(0,1)
    plt.legend()

    plt.tight_layout()
    plt.show()