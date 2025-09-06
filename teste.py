from .src import get_samples, get_probs_hist


pacientes = get_samples.gerar_amostra(15)

utis1, internacoes1, altas1, tempo1 = get_probs_hist.previsao_convolucao()
utis1, internacoes1, altas1, tempo1 = get_probs_hist.previsao_rna_fft()