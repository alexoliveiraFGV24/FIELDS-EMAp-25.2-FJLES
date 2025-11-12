import customtkinter
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator 

# Placeholder para simular a obtenção de dados para a comparação temporal
def obter_dados_comparacao():
    # Simula dados de volume de pacientes para dois períodos (ex: Hoje vs Média Histórica)
    horas = np.arange(24)
    volume_hoje = np.random.randint(5, 30, 24)
    volume_historico = np.random.randint(10, 25, 24)
    return horas, volume_hoje, volume_historico

class ComparacaoVolumeFrame(customtkinter.CTkFrame):
    """
    Frame para exibir a comparação temporal do volume de pacientes em um gráfico de linhas.
    """
    def __init__(self, master, padx, pady, text, **kwargs):
        super().__init__(master, **kwargs)
        self.title_label = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(pady, 0))
        
        # Ajusta a cor de fundo do Matplotlib (assumindo #CFCDCD como padrão)
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD") 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill=tk.BOTH, padx=padx, pady=pady)
        
        self.plotar_grafico()

    def plotar_grafico(self, horas=None, volume_hoje=None, volume_historico=None):
        """
        Plota o gráfico de comparação de volume.
        """
        self.ax.clear()
        
        if horas is None or volume_hoje is None or volume_historico is None:
            horas, volume_hoje, volume_historico = obter_dados_comparacao()
            
        # Plotar os dados
        self.ax.plot(horas, volume_hoje, label='Volume Hoje', color='#3498DB', marker='o')
        self.ax.plot(horas, volume_historico, label='Média Histórica', color='#E74C3C', linestyle='--')
        
        # Configurações do gráfico
        self.ax.set_title('Comparação Temporal do Volume de Pacientes (24h)')
        self.ax.set_xlabel('Hora do Dia (h)')
        self.ax.set_ylabel('Número de Pacientes')
        self.ax.set_xticks(horas[::2]) # Mostrar a cada 2 horas
        self.ax.set_xlim(0, 23)
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Estilo
        self.ax.tick_params(colors='black', which='both')
        self.ax.set_facecolor("#CFCDCD")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color("#CFCDCD")
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color("#CFCDCD")
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.legend(loc='upper right')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def refresh(self):
        """
        Atualiza o gráfico com novos dados.
        """
        horas, volume_hoje, volume_historico = obter_dados_comparacao()
        self.plotar_grafico(horas, volume_hoje, volume_historico)


class PaginaComparacaoTemporal(customtkinter.CTkFrame):
    """
    Página que exibe a comparação temporal de métricas do hospital.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#F2F2F2", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame principal de comparação de volume
        self.comparacao_volume = ComparacaoVolumeFrame(
            master=self, 
            padx=20, 
            pady=20, 
            text="Volume de Pacientes: Hoje vs Média Histórica",
            fg_color="white" # Cor de fundo para destacar o frame
        )
        self.comparacao_volume.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")
        
        # Adicionar outros frames de comparação aqui, se necessário
        
    def refresh(self):
        """
        Método de atualização da página.
        """
        self.comparacao_volume.refresh()