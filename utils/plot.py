import numpy as np
import matplotlib.pyplot as plt


def plot_probs_acumul(probs):
    plt.figure(figsize=(12,4))

    plt.plot(probs[0], label="UTI")
    plt.plot(probs[1], label="INTERNACOES")
    plt.plot(probs[2], label="ALTAS")

    plt.grid(visible=True, alpha=0.7)
    plt.legend()
    plt.show()