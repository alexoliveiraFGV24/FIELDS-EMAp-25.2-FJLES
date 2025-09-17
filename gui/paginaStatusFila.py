import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import config


def obter_previsoes():
    """Gera valores fictícios de previsões de forma dinâmica."""
    previsao_internacao = np.random.randint(15, 30)
    previsao_alta = np.random.randint(10, 25)
    previsao_uti = np.random.randint(2, 10)
    return previsao_internacao, previsao_alta, previsao_uti

class FrameValor(customtkinter.CTkFrame):
    def __init__(self, master, padx, pady, text, value):
        super().__init__(master)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.rotulo_titulo.pack(side=tk.TOP, padx=padx, pady=(pady, 0))
        self.rotulo_valor = customtkinter.CTkLabel(master=self, text=str(value), font=customtkinter.CTkFont(size=70, weight="bold"))
        self.rotulo_valor.pack(side=tk.TOP, expand=True, padx=padx, pady=0)
    
    def atualizar_valor(self, novo_valor):
        self.rotulo_valor.configure(text=str(novo_valor))

class FramePrioridade(customtkinter.CTkFrame):
    def __init__(self, master, text, value, cor):
        super().__init__(master, fg_color=cor)
        self.inner_frame = customtkinter.CTkFrame(master=self)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self.inner_frame, text=text, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.rotulo_titulo.pack(pady=(10, 0))
        frame_valor_unidade = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        frame_valor_unidade.pack(expand=True)
        self.rotulo_valor = customtkinter.CTkLabel(master=frame_valor_unidade, text=str(value), font=customtkinter.CTkFont(size=30, weight="bold"))
        self.rotulo_valor.pack(expand=True)
        self.rotulo_unidade = customtkinter.CTkLabel(master=frame_valor_unidade, text="min", font=customtkinter.CTkFont(size=12))
        self.rotulo_unidade.pack(expand=True, pady=(8, 0))
    
    def atualizar_valor(self, novo_valor):
        self.rotulo_valor.configure(text=str(novo_valor))

class FrameTempo(customtkinter.CTkFrame):
    def __init__(self, master, padx, pady, text, tempos_prioridade, cores_prioridade):
        super().__init__(master)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.rotulo_titulo.pack(pady=(pady, 0), padx=padx)
        self.painel_prioridades = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.painel_prioridades.pack(expand=True, fill=tk.BOTH)
        
        self.frames_prioridade = []
        for i in range(len(tempos_prioridade)):
            frame_p = FramePrioridade(
                master=self.painel_prioridades,
                text=f"{i+1}",
                value=tempos_prioridade[i],
                cor=cores_prioridade[i],
            )
            frame_p.pack(side=tk.LEFT, padx=config.FRAME_GAP, expand=True, fill=tk.BOTH)
            self.frames_prioridade.append(frame_p)

    def atualizar_tempos(self, novos_tempos):
        for i, frame in enumerate(self.frames_prioridade):
            frame.atualizar_valor(novos_tempos[i])


class ERVolumeFrame(customtkinter.CTkFrame):
    def __init__(self, master, padx, pady, text, current_time=24):
        super().__init__(master)
        self.title_label = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(pady, 0))
        
        self.current_time = current_time
        
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill=tk.BOTH, padx=padx, pady=pady)
        
        self.plotar_grafico(current_time)

    def plotar_grafico(self, tempo_atual):
        self.ax.clear()
        
        # Gera dados para todas as 24 horas
        x = np.arange(24)
        y = 10*(np.exp(-0.5 * ((x - 8) / 2) ** 2) + np.exp(-0.1 * ((x - 18) / 2) ** 2))
        
        # Cria uma lista de cores baseada no tempo atual
        cores = ["#778E84" if i < tempo_atual else "#069E34" for i in range(24)]

        # Plota todas as barras de uma vez
        self.ax.bar(x, y, color=cores, width=0.8, align="center")
        
        # Adiciona a legenda manualmente para controlar o texto e cores
        self.ax.bar(0, 0, color="#778E84", label="Passado")
        self.ax.bar(0, 0, color="#069E34", label="Futuro")

        # Configurações do eixo e legenda
        self.ax.set_xlabel('Horário do Dia', color='black', fontsize=16)
        self.ax.set_ylabel("Ocorrências", color='black', fontsize=16)
        self.ax.set_xticks(np.arange(0, 25, 5))
        self.ax.tick_params(colors='black', which='both')
        self.ax.set_facecolor("#CFCDCD")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color("#CFCDCD")
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color("#CFCDCD")
        self.ax.legend(prop={'size': 14, 'weight': 'bold'}, labelcolor='black', frameon=False)
        self.fig.tight_layout()
        self.canvas.draw()
    
    def atualizar_grafico(self, novo_tempo_atual):
        self.plotar_grafico(novo_tempo_atual)


class PaginaStatusHospital(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        small_pad = 10
        self.horario_atual = 17
        self.tempos_prioridade_base = [10, 10, 10, 10, 10] 
        self.cores_prioridade = ["#E53935", "#FFEB3B", "#FB8C00", "#2196F3", "#4CAF50"] 

        internacao_pred, alta_pred, uti_pred = obter_previsoes()
        total_pacientes = internacao_pred + alta_pred + uti_pred

        self.tp = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Total de Pacientes", value=total_pacientes)
        self.tp.grid(column=0, row=0, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.lws = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de Alta", value=alta_pred)
        self.lws.grid(column=0, row=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.ip = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de Internação", value=internacao_pred)
        self.ip.grid(column=0, row=2, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.sod = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de UTI", value=uti_pred)
        self.sod.grid(column=0, row=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.erv = ERVolumeFrame(master=self, padx=small_pad, pady=small_pad, text="Volume do PS", current_time=self.horario_atual)
        self.erv.grid(column=1, row=0, columnspan=2, rowspan=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")
        
        self.mtt = FrameTempo(master=self, padx=small_pad, pady=small_pad, text="Tempo Médio de Tratamento", 
                              tempos_prioridade=self.tempos_prioridade_base, cores_prioridade=self.cores_prioridade)
        self.mtt.grid(column=1, row=3, columnspan=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.mwt = FrameTempo(master=self, padx=small_pad, pady=small_pad, text="Tempo Médio de Espera", 
                              tempos_prioridade=self.tempos_prioridade_base, cores_prioridade=self.cores_prioridade)
        self.mwt.grid(column=2, row=3, columnspan=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.after(2000, self.atualizar_dados)

    def atualizar_dados(self):
        internacao_pred, alta_pred, uti_pred = obter_previsoes()
        total_pacientes = internacao_pred + alta_pred + uti_pred

        self.tp.atualizar_valor(total_pacientes)
        self.lws.atualizar_valor(alta_pred)
        self.ip.atualizar_valor(internacao_pred)
        self.sod.atualizar_valor(uti_pred)
        
        novos_tempos_espera = [np.random.randint(10, 30), np.random.randint(10, 30),np.random.randint(10, 30),np.random.randint(10, 30),np.random.randint(10, 30)]
        self.mtt.atualizar_tempos(novos_tempos_espera)
        self.mwt.atualizar_tempos(novos_tempos_espera)

        self.horario_atual = (self.horario_atual + 1) % 24
        self.erv.atualizar_grafico(self.horario_atual)

        self.after(2900 , self.atualizar_dados)