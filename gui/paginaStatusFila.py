import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.ticker import MaxNLocator 

from utils.samples import *
import gui.config as config


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
        self.color = config.dicio[self.text]
        
        self.rotulo_titulo = customtkinter.CTkButton(master=self, text=self.text, 
                                                     font=customtkinter.CTkFont(size=16, weight="bold"), 
                                                     fg_color="#B5B2B2", text_color='black', 
                                                     command=self.alternar_conteudo)
        self.rotulo_titulo.pack(side=tk.TOP, padx=padx, pady=(pady, 0))
        
        self.rotulo_valor = customtkinter.CTkLabel(master=self, text=str(value), 
                                                     font=customtkinter.CTkFont(size=70, weight="bold"))
        self.rotulo_valor.pack(side=tk.TOP, expand=True, padx=padx, pady=0)
        
        self.frame_grafico = customtkinter.CTkFrame(self)
        
        # Ajusta a cor de fundo do Matplotlib
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD") 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def plotar_grafico(self):
        """
        Atualiza o gráfico com a nova distribuição de dados (CDF).
        """
        self.ax.clear()  # Limpa o eixo anterior
        
        # O valor aqui está sendo usado como rótulo do valor esperado/médio da distribuição
        label_valor = self.valor if isinstance(self.valor, (int, float)) else np.sum(self.valor)
        self.ax.bar(0, 0, label=f"Valor Esperado: {label_valor:.0f}", color="#CFCDCD")
        
        self.ax.bar(np.arange(len(self.distribuicao)), self.distribuicao, color=self.color)
        
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
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
        # Se for um array (Total de Pacientes), exibe a soma. Senão, exibe o valor
        if isinstance(novo_valor, np.ndarray):
            valor_display = int(np.sum(novo_valor))
        else:
            valor_display = int(novo_valor)
            
        self.rotulo_valor.configure(text=str(valor_display))
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
        """
        super().__init__(master, fg_color=cor)
        self.inner_frame = customtkinter.CTkFrame(master=self)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10,ipady=0)
        
        frame_valor_unidade = customtkinter.CTkFrame(master=self.inner_frame, fg_color="transparent")
        frame_valor_unidade.pack(expand=True, pady=(0,0))
        self.rotulo_valor = customtkinter.CTkLabel(master=frame_valor_unidade, text=str(value), font=customtkinter.CTkFont(size=30, weight="bold"))
        self.rotulo_valor.pack(expand=True, pady=(0,0))
        self.rotulo_unidade = customtkinter.CTkLabel(master=frame_valor_unidade, text="min", font=customtkinter.CTkFont(size=12))
        self.rotulo_unidade.pack(expand=True, pady=(0, 0))
    
    def atualizar_valor(self, novo_valor):
        """
        Atualiza o valor exibido no frame.
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
        """
        for i, frame in enumerate(self.frames_prioridade):
            frame.atualizar_valor(novos_tempos[i])


class ERVolumeFrame(customtkinter.CTkFrame):
    """
    Frame responsável por exibir o gráfico de volume do pronto-socorro,
    mostrando pacientes passados e previstos como um gráfico de barras empilhadas.
    """
    def __init__(self, master, padx, pady, text, current_time=24, pacientes_passado=np.zeros((24, 3)), pacientes_futuro=np.zeros((24, 3))):
        """
        Inicializa o frame com gráfico de volume do PS.
        
        OBS: pacientes_passado e pacientes_futuro são arrays 24x3: (Hora, Estado)
        """
        super().__init__(master)
        self.title_label = customtkinter.CTkLabel(master=self, text=text, font=customtkinter.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(pady, 0))
        
        self.current_time = current_time
        
        self.modo_visualizacao_idx = 0  # 0: Total, 1: Internação, 2: Alta, 3: UTI
        self.MODOS = ["Total (Empilhado)", "Internação", "Alta", "UTI"]
        self.pacientes_passado = pacientes_passado # Armazena para alternância
        self.pacientes_futuro = pacientes_futuro # Armazena para alternância
        
        # Ajusta a cor de fundo do Matplotlib
        self.fig, self.ax = plt.subplots(facecolor="#CFCDCD") 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        self.canvas_and_button_frame = customtkinter.CTkFrame(master=self, fg_color='transparent')
        self.canvas_and_button_frame.pack(expand=True, fill=tk.BOTH, padx=padx, pady=pady)
        
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.btn_alternar_categoria = customtkinter.CTkButton(
            master=self.canvas_and_button_frame, 
            text=f"Visualizar: {self.MODOS[self.modo_visualizacao_idx]}",
            command=self.alternar_visualizacao,
            font=customtkinter.CTkFont(size=12),
            fg_color="#B5B2B2", text_color='black'
        )
        self.btn_alternar_categoria.pack(side=tk.BOTTOM, pady=(5, 0))
        
        self.plotar_grafico(current_time, pacientes_passado, pacientes_futuro)

    def alternar_visualizacao(self):
        """
        Alterna o modo de visualização entre Total e as categorias individuais.
        """
        # Avança para o próximo modo, ciclando de 0 a 3
        self.modo_visualizacao_idx = (self.modo_visualizacao_idx + 1) % len(self.MODOS)
        
        # Atualiza o texto do botão
        self.btn_alternar_categoria.configure(text=f"Visualizar: {self.MODOS[self.modo_visualizacao_idx]}")
        
        # Redesenha o gráfico com o novo modo, usando os dados armazenados
        self.plotar_grafico(self.current_time, self.pacientes_passado, self.pacientes_futuro)


    def plotar_grafico(self, tempo_atual, pacientes_passado, pacientes_futuro):
        """
        Plota o gráfico de volume de pacientes no PS como um gráfico de barras empilhadas ou individual,
        centralizado no tempo atual e com rolagem circular.

        :param tempo_atual: Hora atual (0-23)
        :param pacientes_passado: Dados históricos (24x3)
        :param pacientes_futuro: Dados previstos (24x3)
        """
        self.ax.clear()
        
        # Dimensões: [0] Internação, [1] Alta, [2] UTI
        CATEGORIAS = ["Internação", "Alta", "UTI"] 
        # Cores para o futuro (cores cheias)
        CORES_CATEGORIAS_FUTURO = config.COR_CATEGORIA[:3] 
        # Cores para o passado (cores com alpha menor)
        CORES_CATEGORIAS_PASSADO = config.COR_CATEGORIA_PASSADO[:3] 
        
        # 1. Preparar os dados combinados (Passado + Futuro)
        dados_plot = pacientes_futuro.copy()
        
        # Identifica o intervalo do passado/histórico a ser mostrado
        indices_passado = np.array(range(tempo_atual - config.JANELA_TEMPO + 1, tempo_atual + 1)) % 24
        
        for i in indices_passado:
            # Substitui os dados futuros pelos dados passados para as horas históricas
            dados_plot[i] = pacientes_passado[i]

        # 2. Definir as cores de BORDA (Passado/Futuro/Atual) para o destaque
        cores_por_hora = [config.COR_FUTURO] * 24 # Cor padrão: Futuro (para borda)
        for i in indices_passado:
            cores_por_hora[i] = config.COR_PASSADO # Cores do passado (para borda)
            
        cores_por_hora[tempo_atual] = config.COR_HORARIO_ATUAL # Cor do horário atual (para borda)
        
        JANELA_DE_VISUALIZACAO = 10 
        metade_janela_esquerda = 5 # 5 horas antes do tempo atual
        metade_janela_direita = 4  # 4 horas depois do tempo atual (total 10 barras: 5+1+4)
        
        # 1. Calcular os índices (horas do dia 0-23) que serão plotados
        # O intervalo de índices brutos (coordenada x) que centralizam o tempo_atual
        indices_brutos = np.arange(tempo_atual - metade_janela_esquerda, tempo_atual + metade_janela_direita + 1)
        
        # O índice real do array de dados (0-23) usando o operador módulo
        indices_data = indices_brutos % 24
        
        # O valor do x (coordenada) que será plotado
        x_plot = indices_brutos 
        
        # 2. Reorganizar os dados para o trecho visualizado
        dados_plot_unrolled = dados_plot[indices_data]
        # Pegar as cores de BORDA apenas para as barras que serão mostradas na janela
        cores_por_hora_unrolled = np.array(cores_por_hora)[indices_data] 
        
        # Labels para os ticks (os horários reais que serão mostrados)
        x_ticks_labels = indices_data

        # Define quais categorias e cores serão usadas com base no modo
        if self.modo_visualizacao_idx == 0:
            # Modo Total (Empilhado)
            categorias_a_plotar = CATEGORIAS
            
            # Cria uma lista de cores para cada categoria (Passado vs. Futuro)
            cores_a_usar_por_categoria = [] 
            for i in range(len(CATEGORIAS)):
                cores_para_plotagem = []
                for j, hora in enumerate(indices_data):
                    # Se for passado E não for o tempo atual, usa a cor de passado
                    if hora in indices_passado and hora != tempo_atual: 
                        cores_para_plotagem.append(CORES_CATEGORIAS_PASSADO[i])
                    else:
                        # Futuro ou a hora atual (usa a cor cheia para o preenchimento)
                        cores_para_plotagem.append(CORES_CATEGORIAS_FUTURO[i]) 
                cores_a_usar_por_categoria.append(cores_para_plotagem)
            
            bottoms = np.zeros(len(x_plot)) 
            titulo_grafico = "Total (Empilhado)"
            
        else:
            # Modos Individuais (1: Internação, 2: Alta, 3: UTI)
            idx_categoria = self.modo_visualizacao_idx - 1 
            categoria_selecionada = CATEGORIAS[idx_categoria]
            
            categorias_a_plotar = [categoria_selecionada]
            
            # --- MODIFICAÇÃO CHAVE AQUI PARA MODOS INDIVIDUAIS ---
            cores_para_plotagem_individual = []
            for j, hora in enumerate(indices_data):
                # Se for passado E não for o tempo atual, usa a cor de passado
                if hora in indices_passado and hora != tempo_atual:
                    cores_para_plotagem_individual.append(CORES_CATEGORIAS_PASSADO[idx_categoria])
                else:
                    # Futuro ou a hora atual (usa a cor cheia para o preenchimento)
                    cores_para_plotagem_individual.append(CORES_CATEGORIAS_FUTURO[idx_categoria])
            
            # cores_a_usar_por_categoria é uma lista de listas. No modo individual, é uma lista com a lista de 10 cores.
            cores_a_usar_por_categoria = [cores_para_plotagem_individual]
            
            # Cria uma matriz de dados onde apenas a categoria selecionada tem valores
            dados_plot_individual = np.zeros_like(dados_plot_unrolled)
            dados_plot_individual[:, 0] = dados_plot_unrolled[:, idx_categoria] 
            dados_plot_unrolled = dados_plot_individual 
            
            bottoms = np.zeros(len(x_plot))
            titulo_grafico = categoria_selecionada
            
        # 3. Plotar as barras
        for i, categoria in enumerate(categorias_a_plotar):
            valores = dados_plot_unrolled[:, i] 
            
            # Lista de 10 cores (uma para cada barra)
            cores_para_categoria = cores_a_usar_por_categoria[i]
            
            # Plota as barras da categoria
            barras = self.ax.bar(x_plot, valores, bottom=bottoms, color=cores_para_categoria, width=0.6, align="center") 
            
            # Aplica o destaque de borda para o horário ATUAL em todas as categorias
            # len(barras)//2 é o índice da barra do tempo atual na janela
            barras[len(barras)//2].set_edgecolor(cores_por_hora_unrolled[len(barras)//2])
            barras[len(barras)//2].set_linewidth(6) 
            
            # Adiciona a entrada da categoria na legenda (usando a cor cheia/futuro)
            self.ax.bar(0, 0, color=CORES_CATEGORIAS_FUTURO[i if self.modo_visualizacao_idx == 0 else idx_categoria], linewidth=0, label=categoria)
            
            # Atualiza o `bottom` SOMENTE no modo Total
            if self.modo_visualizacao_idx == 0:
                bottoms += valores

        # 4. Adicionar a legenda de status (Passado/Futuro/Atual)
        # Usamos cores de borda para representar os status na legenda
        self.ax.bar(0, 0, color='none', edgecolor=config.COR_PASSADO, linewidth=5, label="Passado") 
        self.ax.bar(0, 0, color='none', edgecolor=config.COR_FUTURO, linewidth=5, label="Futuro") 
        self.ax.bar(0, 0, color='none', edgecolor=config.COR_HORARIO_ATUAL, linewidth=6, label="Atual")

        # Configurações do eixo e legenda
        self.ax.set_title(f"Volume do PS - {titulo_grafico}") 
        self.ax.set_xlabel(f'Horário do Dia: {tempo_atual:02d}h', color='black', fontsize=16)
        self.ax.set_ylabel("Ocorrências", color='black', fontsize=16)
        
        # Força o eixo Y a mostrar apenas valores inteiros
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Define os ticks no eixo X
        self.ax.set_xticks(x_plot)
        self.ax.set_xticklabels([f"{h:02d}" for h in x_ticks_labels])
        
        # Centraliza o tempo atual
        x_min_plot = x_plot[0] - 0.5
        x_max_plot = x_plot[-1] + 0.5
        self.ax.set_xlim(x_min_plot, x_max_plot) 

        self.ax.tick_params(colors='black', which='both')
        self.ax.set_facecolor("#CFCDCD")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color("#CFCDCD")
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color("#CFCDCD")
        
        # Coloca a legenda fora do gráfico para não obstruir as barras
        self.ax.legend(prop={'size': 10, 'weight': 'bold'}, labelcolor='black', frameon=False, loc='upper left', bbox_to_anchor=(1, 1))

        self.fig.tight_layout(rect=[0, 0, 0.9, 1]) # Ajusta o layout para acomodar a legenda
        self.canvas.draw()
    
    def atualizar_grafico(self, novo_tempo_atual, pacientes_passado, pacientes_futuro):
        """
        Atualiza o gráfico com novos dados.
        """
        self.current_time = novo_tempo_atual # Armazena o tempo atual
        self.pacientes_passado = pacientes_passado # Armazena os dados
        self.pacientes_futuro = pacientes_futuro # Armazena os dados
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
        self.pacientes_passado = np.zeros((24, 3)) 
        self.pacientes_futuro = np.zeros((24, 3)) 
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
        self.grid_rowconfigure(4, weight=0) 

        small_pad = 10
        self.horario_atual = 14
        self.tempos_prioridade_base = [10, 10, 10, 10, 10] 
        self.cores_prioridade = ["#E53935", "#FFEB3B", "#FB8C00", "#004075", "#4CAF50"] 

        # Dados iniciais
        previsoes, _, proximo_indice = obter_previsoes(self.indice_paciente_atual, self.horario_atual)
        internacao_pred, alta_pred, uti_pred = previsoes
        # total_pacientes agora é um array 1x3: [Internação, Alta, UTI]
        total_pacientes_estados = np.array([internacao_pred, alta_pred, uti_pred]) 
        total_pacientes_soma = np.sum(total_pacientes_estados)

        self.tp = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Total de Pacientes", value=total_pacientes_soma)
        self.tp.grid(column=0, row=0, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.lws = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de Alta", value=alta_pred)
        self.lws.grid(column=0, row=1, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.ip = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de Internação", value=internacao_pred)
        self.ip.grid(column=0, row=2, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        self.sod = FrameValor(master=self, padx=small_pad, pady=small_pad, text="Previsão de UTI", value=uti_pred)
        self.sod.grid(column=0, row=3, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="nsew")

        # Passa os arrays 24x3 para o Frame
        self.erv = ERVolumeFrame(master=self, padx=small_pad, pady=small_pad, text="Volume do PS", current_time=self.horario_atual,
                                 pacientes_passado=self.pacientes_passado, pacientes_futuro=self.pacientes_futuro)
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
        self.btn_pausa.grid(column=2, row=4, pady=config.FRAME_GAP, padx=config.FRAME_GAP, sticky="se") 

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
        Atualiza os dados da página periodicamente.
        """
        if self.simulacao_pausada:
            return

        previsoes, cdf, proximo_indice = obter_previsoes(self.indice_paciente_atual, self.horario_atual)
        internacao_pred, alta_pred, uti_pred = previsoes
        internacao_cdf, alta_cdf, uti_cdf = tuple(cdf)
        self.means = cdf
        self.indice_paciente_atual = proximo_indice

        # Total de pacientes por estado (Internação, Alta, UTI) para o horário atual
        total_pacientes_estados = np.array([internacao_pred, alta_pred, uti_pred])
        total_pacientes_soma = np.sum(total_pacientes_estados)
        
        # Atualiza os dados dos frames
        self.tp.atualizar(total_pacientes_soma) # Usa a soma para o Total de Pacientes
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

        # 1. Avança o horário
        self.horario_atual = (self.horario_atual + 1) % 24
        
        # 2. Atualiza o array de dados passados (Histórico)
        self.pacientes_passado[self.horario_atual] = total_pacientes_estados
        
        # 3. Atualiza o array de previsões futuras (24x3)
        self.pacientes_futuro = previsao_pacientes_futuro(self.pacientes_passado, self.pacientes_futuro, self.horario_atual, metric='mean')
        
        # 4. Atualiza o gráfico de volume do PS
        self.erv.atualizar_grafico(self.horario_atual, self.pacientes_passado, self.pacientes_futuro)

        self.after_id = self.after(1000, self.atualizar_dados)