import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import config

def obter_previsoes():
    """
    Gera valores fictícios de previsões.

    Em uma aplicação real, esta função se conectaria a um modelo de aprendizado
    de máquina para obter os dados de previsão.

    Returns:
        tuple: Uma tupla contendo as previsões para internação, alta e UTI.
    """
    previsao_internacao = 25
    previsao_alta = 18
    previsao_uti = 5
    return previsao_internacao, previsao_alta, previsao_uti

class FrameValor(customtkinter.CTkFrame):
    """
    Um frame personalizado para exibir um valor numérico com um título.

    Args:
        master (customtkinter.CTk): O widget mestre.
        padx (int): Preenchimento horizontal.
        pady (int): Preenchimento vertical.
        text (str): O texto do título.
        value (any): O valor a ser exibido.
    """
    def __init__(self, master, padx, pady, text, value):
        super().__init__(master)
        
        # Rótulo para o título do frame
        self.rotulo_titulo = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.rotulo_titulo.pack(side=tk.TOP, padx=padx, pady=(pady, 0))
        
        # Rótulo para o valor, centralizado verticalmente
        self.rotulo_valor = customtkinter.CTkLabel(master=self, text=str(value), font=customtkinter.CTkFont(size=70, weight="bold"))
        self.rotulo_valor.pack(side=tk.TOP, expand=True, padx=padx, pady=0)


class FramePrioridade(customtkinter.CTkFrame):
    """
    Um frame que exibe um tempo de espera com uma borda colorida
    conforme a prioridade.

    Args:
        master (customtkinter.CTk): O widget mestre.
        text (str): O texto do título da prioridade (e.g., "P1").
        value (int): O valor do tempo de espera em minutos.
        cor (str): A cor da borda do frame.
    """
    def __init__(self, master, text, value, cor):
        # O frame externo tem a cor da borda
        super().__init__(master, fg_color=cor)
        
        # O frame interno tem a cor padrão do tema (a "cor do interior")
        self.inner_frame = customtkinter.CTkFrame(master=self)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # padx/pady controlam a espessura da borda

        # Rótulo para o título da prioridade (dentro do inner_frame)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self.inner_frame, text=text, 
                                                    font=customtkinter.CTkFont(size=14, weight="bold"))
        self.rotulo_titulo.pack(pady=(10, 0))

        # Rótulo para o valor e a unidade (dentro do inner_frame)
        frame_valor_unidade = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        frame_valor_unidade.pack(expand=True)

        self.rotulo_valor = customtkinter.CTkLabel(master=frame_valor_unidade, text=str(value), 
                                                   font=customtkinter.CTkFont(size=30, weight="bold"))
        self.rotulo_valor.pack(expand=True)

        self.rotulo_unidade = customtkinter.CTkLabel(master=frame_valor_unidade, text="min", 
                                                    font=customtkinter.CTkFont(size=12))
        self.rotulo_unidade.pack(expand=True, pady=(8, 0))


class FrameTempo(customtkinter.CTkFrame):
    """
    Um frame personalizado para exibir um valor de tempo e suas sub-prioridades.

    Args:
        master (customtkinter.CTk): O widget mestre.
        padx (int): Preenchimento horizontal.
        pady (int): Preenchimento vertical.
        text (str): O texto do título.
        tempos_prioridade (list): Lista com os tempos de espera para cada prioridade.
        cores_prioridade (list): Lista com as cores para cada prioridade.
    """
    def __init__(self, master, padx, pady, text, tempos_prioridade, cores_prioridade):
        super().__init__(master)
        
        # Rótulo para o título do frame (no topo)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.rotulo_titulo.pack(pady=(pady, 0), padx=padx)
        
        # Frame para agrupar as caixas de prioridade
        self.painel_prioridades = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.painel_prioridades.pack(expand=True, fill=tk.BOTH)

        # Adiciona os frames de prioridade no painel, lado a lado
        for i in range(len(tempos_prioridade)):
            FramePrioridade(
                master=self.painel_prioridades,
                text=f"{i+1}",
                value=np.random.randint(1,20),
                cor=cores_prioridade[i],
            ).pack(side=tk.LEFT, padx=config.FRAME_GAP, expand=True, fill=tk.BOTH)


class FrameVolumePS(customtkinter.CTkFrame):
    """
    Um frame para exibir um gráfico de volume do pronto-socorro.
    ...
    """
    def __init__(self, master, padx, pady, text, current_time=24):
        super().__init__(master)

        self.title_label = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(pady, 0))

        x = np.linspace(0, current_time, current_time)
        y = 10*(np.exp(-0.5 * ((x - 8) / 2) ** 2) + np.exp(-0.1 * ((x - 18) / 2) ** 2))

        x2 = np.linspace(current_time, 24, 24 - current_time)
        y2 = 10*(np.exp(-0.5 * ((x2 - 8) / 2) ** 2) + np.exp(-0.1 * ((x2 - 18) / 2) ** 2))

        fig, ax = plt.subplots(facecolor="#CFCDCD")
        # passado
        ax.bar(x, y, color="#778E84", width=1.0, align="center")
        # futuro
        ax.bar(x2, y2, color="#069E34", width=1.0, align="center")
        ax.set_xlabel("Hora do dia")
        ax.set_ylabel("Ocorrências")
        ax.set_xticks([0,5,10,15,20,24])
        ax.tick_params(colors='black', which='both')
        ax.set_facecolor("#CFCDCD")
        ax.set_xlabel('Horário do Dia', color='black', fontsize=16)
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color("#CFCDCD")
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color("#CFCDCD")

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        
        self.widget_canvas = self.canvas.get_tk_widget()
        self.widget_canvas.pack(expand=True, fill=tk.BOTH, padx=padx, pady=pady)


class PaginaStatusHospital(customtkinter.CTkFrame):
    """
    Página principal do painel de controle do hospital.
    Organiza e exibe todos os frames de status e gráficos.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        padding_pequeno = 10
        
        horario_atual = 17
        previsao_internacao, previsao_alta, previsao_uti = obter_previsoes()
        total_pacientes = previsao_internacao + previsao_alta + previsao_uti

        self.tp = FrameValor(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Total de Pacientes", value=total_pacientes)
        self.tp.grid(column=0, row=0, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.lws = FrameValor(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Previsão de Alta", value=previsao_alta)
        self.lws.grid(column=0, row=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.ip = FrameValor(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Previsão de Internação", value=previsao_internacao)
        self.ip.grid(column=0, row=2, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.sod = FrameValor(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Previsão de UTI", value=previsao_uti)
        self.sod.grid(column=0, row=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.erv = FrameVolumePS(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Volume do PS", current_time=horario_atual)
        self.erv.grid(column=1, row=0, columnspan=2, rowspan=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")
        
        # Definindo as cores e tempos para cada prioridade
        tempos_prioridade = [10, 20, 35, 60, 120] 
        cores_prioridade = ["#E53935", "#FFEB3B", "#FB8C00", "#2196F3", "#4CAF50"] # Vermelho, Laranja, Amarelo, Verde, Azul
        
        # Criação e posicionamento do FrameTempo com as prioridades
        self.mtt = FrameTempo(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Tempo Médio de Tratamento", 
                              tempos_prioridade=tempos_prioridade, cores_prioridade=cores_prioridade)
        self.mtt.grid(column=1, row=3, columnspan=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.mwt = FrameTempo(master=self, padx=padding_pequeno, pady=padding_pequeno, text="Tempo Médio de Espera", 
                              tempos_prioridade=tempos_prioridade, cores_prioridade=cores_prioridade)
        self.mwt.grid(column=2, row=3, columnspan=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")
