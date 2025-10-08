import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import gui.config as config
from utils.samples import obter_previsoes, previsao_pacientes_futuro


class FrameValor(customtkinter.CTkFrame):
    """
    Frame responsável por exibir um título e um valor numérico grande,
    com a opção de alternar para exibir um gráfico genérico ao clicar
    no botão do título.
    """
    def __init__(self, master, padx, pady, text, value):
        """
        Inicializa o frame com um título e valor.
        """
        super().__init__(master)
        self.valor = 0
        self.mostrando_valor = True
        self.text = text
        self.distribuicao = np.zeros(1)
        
        self.rotulo_titulo = customtkinter.CTkButton(master=self, text=self.text, 
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), 
                                                     fg_color="#B5B2B2", text_color='black', 
                                                     command=self.alternar_conteudo)
        self.rotulo_titulo.pack(side=tk.TOP, padx=padx, pady=(pady, 0))
        
        self.rotulo_valor = customtkinter.CTkLabel(master=self, text=str(value), 
                                                     font=customtkinter.CTkFont(size=70, weight="bold"))
        self.rotulo_valor.pack(side=tk.TOP, expand=True, padx=padx, pady=0)
        
        self.frame_grafico = customtkinter.CTkFrame(self)
        
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def plotar_grafico(self):
        """
        Atualiza o gráfico com a nova distribuição de dados.
        """
        self.ax.clear()  # Limpa o eixo anterior
        self.ax.bar(0, 0, label=f"Valor Esperado: {self.valor}", color="#CFCDCD")
        
        self.ax.bar(np.arange(len(self.distribuicao)), self.distribuicao, color=config.COR_CATEGORIA[0])
        self.ax.set_title('CDF')
        self.ax.set_xlabel('k')
        self.ax.set_ylabel('$P(X < k)$')
        self.ax.tick_params(colors='black', which='both')
        self.ax.set_facecolor("#CFCDCD")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color("#CFCDCD")
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color("#CFCDCD")
        self.ax.grid(False)
        self.ax.legend(prop={'size': 14, 'weight': 'bold'}, labelcolor='black', frameon=False)
        self.fig.tight_layout()
        self.canvas.draw()
    
    def alternar_conteudo(self):
        """
        Alterna entre exibir o valor numérico e o gráfico.
        """
        if self.text == "Total de Pacientes":
            return
        
        if self.mostrando_valor:
            self.rotulo_valor.pack_forget()
            self.frame_grafico.pack(side=tk.TOP, expand=True)
            self.plotar_grafico()  # Chame a plotagem ao mostrar o gráfico
        else:
            self.frame_grafico.pack_forget()
            self.rotulo_valor.pack(side=tk.TOP, expand=True)
        
        self.mostrando_valor = not self.mostrando_valor

    def atualizar_valor(self, novo_valor, nova_distribuicao=None):
        """
        Atualiza o valor exibido no frame.
        """
        self.valor = novo_valor
        self.rotulo_valor.configure(text=str(novo_valor))
        if nova_distribuicao is not None:
            self.distribuicao = nova_distribuicao

    def atualizar(self, novo_valor, nova_distribuicao=None):
        if nova_distribuicao is None:
            nova_distribuicao = np.zeros(1)
        
        self.atualizar_valor(novo_valor, nova_distribuicao)
        
class FramePrioridade(customtkinter.CTkFrame):
    """
    Frame que exibe informações de tempo médio para determinada prioridade,
    com cor de fundo representando a gravidade.
    """
    def __init__(self, master, text, value, cor):
        """
        Inicializa o frame de prioridade.

        :param master: Widget pai
        :param text: Texto do rótulo (não usado atualmente)
        :param value: Valor inicial exibido
        :param cor: Cor de fundo do frame
        """
        super().__init__(master, fg_color=cor)
        self.inner_frame = customtkinter.CTkFrame(master=self)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10,ipady=0)
        # self.rotulo_titulo = customtkinter.CTkLabel(master=self.inner_frame, text=text, font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.rotulo_titulo.pack(pady=(10, 0))
        frame_valor_unidade = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        frame_valor_unidade.pack(expand=True, pady=(0,0))
        self.rotulo_valor = customtkinter.CTkLabel(master=frame_valor_unidade, text=str(value), font=customtkinter.CTkFont(size=30, weight="bold"))
        self.rotulo_valor.pack(expand=True, pady=(0,0))
        self.rotulo_unidade = customtkinter.CTkLabel(master=frame_valor_unidade, text="min", font=customtkinter.CTkFont(size=12))
        self.rotulo_unidade.pack(expand=True, pady=(0, 0))
    
    def atualizar_valor(self, novo_valor):
        """
        Atualiza o valor exibido no frame.

        :param novo_valor: Novo valor numérico (tempo em minutos)
        """
        self.rotulo_valor.configure(text=str(novo_valor))

class FrameTempo(customtkinter.CTkFrame):
    """
    Frame que exibe múltiplos FramePrioridade lado a lado,
    representando os tempos médios por prioridade.
    """
    def __init__(self, master, padx, pady, text, tempos_prioridade, cores_prioridade):
        """
        Inicializa o frame de tempos médios.

        :param master: Widget pai
        :param padx: Espaçamento horizontal
        :param pady: Espaçamento vertical
        :param text: Texto do título
        :param tempos_prioridade: Lista com tempos médios por prioridade
        :param cores_prioridade: Lista com cores correspondentes
        """
        super().__init__(master)
        self.rotulo_titulo = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.rotulo_titulo.pack(pady=(pady, 0), padx=padx)
        self.painel_prioridades = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.painel_prioridades.pack(expand=True, fill=tk.BOTH, pady=(0,0))
        
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
        """
        Atualiza os valores de tempo em todos os frames de prioridade.

        :param novos_tempos: Lista de novos tempos por prioridade
        """
        for i, frame in enumerate(self.frames_prioridade):
            frame.atualizar_valor(novos_tempos[i])


class ERVolumeFrame(customtkinter.CTkFrame):
    """
    Frame responsável por exibir o gráfico de volume do pronto-socorro,
    mostrando pacientes passados e previstos.
    """
    def __init__(self, master, padx, pady, text, current_time=24, pacientes_passado=np.zeros(24), pacientes_futuro=np.zeros(24)):
        """
        Inicializa o frame com gráfico de volume do PS.

        :param master: Widget pai
        :param padx: Espaçamento horizontal
        :param pady: Espaçamento vertical
        :param text: Texto do título
        :param current_time: Hora atual (0-23)
        :param pacientes_passado: Array com dados do passado
        :param pacientes_futuro: Array com previsões
        """
        super().__init__(master)
        self.title_label = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(pady, 0))
        
        self.current_time = current_time
        
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill=tk.BOTH, padx=padx, pady=pady)
        
        self.plotar_grafico(current_time, pacientes_passado, pacientes_futuro)

    def plotar_grafico(self, tempo_atual, pacientes_passado, pacientes_futuro):
        """
        Plota o gráfico de volume de pacientes no PS.

        :param tempo_atual: Hora atual
        :param pacientes_passado: Dados históricos
        :param pacientes_futuro: Dados previstos
        """
        self.ax.clear()
        
        x = np.arange(24)
        y = pacientes_futuro.copy()
        indices = np.array(range(tempo_atual - config.JANELA_TEMPO, tempo_atual+1)) % 24
        cores = [config.COR_FUTURO for i in range(24)]
        for i in indices:
            y[i] = pacientes_passado[i]
            cores[i]=config.COR_PASSADO
        cores[tempo_atual] = config.COR_HORARIO_ATUAL

        self.ax.bar(x, y, color=cores, width=0.8, align="center")
        
        # Adiciona a legenda manualmente para controlar o texto e cores
        self.ax.bar(0, 0, color=config.COR_PASSADO, label="Passado")
        self.ax.bar(0, 0, color=config.COR_FUTURO, label="Futuro")
        self.ax.bar(0, 0, color=config.COR_HORARIO_ATUAL, label="Atual")

        # Configurações do eixo e legenda
        self.ax.set_xlabel(f'Horário do Dia: {tempo_atual}h', color='black', fontsize=16)
        self.ax.set_ylabel("Ocorrências", color='black', fontsize=16)
        self.ax.set_xticks(np.arange(0, 25, 5))
        self.ax.tick_params(colors='black', which='both')
        self.ax.set_xticks([0,5,10,15,20,23])
        self.ax.set_facecolor("#CFCDCD")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color("#CFCDCD")
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color("#CFCDCD")
        self.ax.legend(prop={'size': 14, 'weight': 'bold'}, labelcolor='black', frameon=False)
        self.fig.tight_layout()
        self.canvas.draw()
    
    def atualizar_grafico(self, novo_tempo_atual, pacientes_passado, pacientes_futuro):
        """
        Atualiza o gráfico com novos dados.

        :param novo_tempo_atual: Novo horário atual
        :param pacientes_passado: Dados históricos
        :param pacientes_futuro: Dados previstos
        """
        self.plotar_grafico(novo_tempo_atual, pacientes_passado, pacientes_futuro)


class PaginaStatusHospital(customtkinter.CTkFrame):
    """
    Página principal que exibe os status do hospital,
    incluindo totais de pacientes, previsões e gráficos.
    """
    def __init__(self, master, **kwargs):
        """
        Inicializa a página de status do hospital.
        """
        super().__init__(master, **kwargs)
        
        self.indice_paciente_atual = 0
        self.pacientes_passado = np.zeros(24)
        self.pacientes_futuro = np.zeros(24)
        self.means = []
        
        self.simulacao_pausada = False
        self.after_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0) # Nova linha para o botão de pausa

        small_pad = 10
        self.horario_atual = 14
        self.tempos_prioridade_base = [10, 10, 10, 10, 10] 
        self.cores_prioridade = ["#E53935", "#FFEB3B", "#FB8C00", "#004075", "#4CAF50"] 

        previsoes, _, proximo_indice = obter_previsoes(self.indice_paciente_atual, self.horario_atual)
        internacao_pred, alta_pred, uti_pred = previsoes
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
        
        # Botão para pausar a simulação
        self.btn_pausa = customtkinter.CTkButton(
            master=self,
            text="Pausar Simulação",
            command=self.alternar_simulacao
        )
        self.btn_pausa.grid(column=3, row=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="se")

        self.after_id = self.after(2000, self.atualizar_dados)

    def alternar_simulacao(self):
        self.simulacao_pausada = not self.simulacao_pausada
        if self.simulacao_pausada:
            self.btn_pausa.configure(text="Continuar Simulação")
        else:
            self.btn_pausa.configure(text="Pausar Simulação")
            self.atualizar_dados()

    def atualizar_dados(self):
        """
        Atualiza os dados da página periodicamente:
        - Novas previsões de pacientes
        - Atualização dos frames de valores
        - Atualização dos tempos médios
        - Atualização do gráfico
        """
        if self.simulacao_pausada:
            return

        previsoes, cdf, proximo_indice = obter_previsoes(self.indice_paciente_atual, self.horario_atual)
        internacao_pred, alta_pred, uti_pred = previsoes
        internacao_cdf, alta_cdf, uti_cdf = tuple(cdf)
        self.means = cdf
        self.indice_paciente_atual = proximo_indice

        total_pacientes = internacao_pred + alta_pred + uti_pred
        
        # Atualiza os dados dos frames
        self.tp.atualizar(total_pacientes)
        self.lws.atualizar(alta_pred, alta_cdf)
        self.ip.atualizar(internacao_pred, internacao_cdf)
        self.sod.atualizar(uti_pred, uti_cdf)
        
        # Chama a atualização do gráfico se ele estiver visível
        if not self.lws.mostrando_valor:
            self.lws.plotar_grafico()
        if not self.ip.mostrando_valor:
            self.ip.plotar_grafico()
        if not self.sod.mostrando_valor:
            self.sod.plotar_grafico()
            
        novos_tempos_espera = [np.random.randint(10, 30), np.random.randint(10, 30), np.random.randint(10, 30), np.random.randint(10, 30), np.random.randint(10, 30)]
        self.mtt.atualizar_tempos(novos_tempos_espera)
        self.mwt.atualizar_tempos(novos_tempos_espera)

        self.horario_atual = (self.horario_atual + 1) % 24
        self.pacientes_passado[self.horario_atual] = total_pacientes
        self.pacientes_futuro = previsao_pacientes_futuro(self.pacientes_passado, self.pacientes_futuro, self.horario_atual, metric='weighted',k=8, ema_alpha=0.5)
        self.erv.atualizar_grafico(self.horario_atual, self.pacientes_passado, self.pacientes_futuro)

        self.after_id = self.after(1000, self.atualizar_dados)