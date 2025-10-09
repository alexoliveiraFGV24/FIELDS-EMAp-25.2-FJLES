"""
Módulo da Página de Status do Paciente.

Este arquivo contém a classe principal 'PaginaStatusPaciente' que constrói
e gerencia o dashboard do paciente, bem como todas as classes de componentes
que compõem o dashboard.
"""
import customtkinter


class CardInfoPaciente(customtkinter.CTkFrame):
    """Card para exibir as informações demográficas básicas do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        font_normal = customtkinter.CTkFont(family="Segoe UI", size=14)

        self.label_nome = customtkinter.CTkLabel(self, text="Nome: -", font=font_normal, text_color=text_color, anchor="w")
        self.label_nome.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        self.label_idade = customtkinter.CTkLabel(self, text="Idade: -", font=font_normal, text_color=text_color, anchor="w")
        self.label_idade.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.label_sexo = customtkinter.CTkLabel(self, text="Sexo: -", font=font_normal, text_color=text_color, anchor="w")
        self.label_sexo.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        self.label_peso = customtkinter.CTkLabel(self, text="Peso: -", font=font_normal, text_color=text_color, anchor="w")
        self.label_peso.grid(row=3, column=0, padx=15, pady=(5, 10), sticky="ew")

    def atualizar_dados(self, nome, idade, sexo, peso):
        self.label_nome.configure(text=f"Nome: {nome}")
        self.label_idade.configure(text=f"Idade: {idade} anos")
        self.label_sexo.configure(text=f"Sexo: {sexo}")
        self.label_peso.configure(text=f"Peso: {peso} kg")

class CardClassificacaoRisco(customtkinter.CTkFrame):
    """Card para exibir a classificação de risco do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.label_titulo = customtkinter.CTkLabel(self, text="Classificação de Risco", text_color=text_color, font=customtkinter.CTkFont(family="Segoe UI", size=14))
        self.label_titulo.pack(padx=10, pady=(10, 0))
        self.label_valor = customtkinter.CTkLabel(self, text="-", font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"))
        self.label_valor.pack(padx=10, pady=(0, 10))

    def atualizar_risco(self, texto_risco, cor_risco):
        self.label_valor.configure(text=texto_risco, text_color=cor_risco)

class CardAlergia(customtkinter.CTkFrame):
    """Card para exibir as alergias do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.label_titulo = customtkinter.CTkLabel(self, text="Alergia", text_color=text_color, font=customtkinter.CTkFont(family="Segoe UI", size=14))
        self.label_titulo.pack(padx=10, pady=(10, 0))
        self.label_valor = customtkinter.CTkLabel(self, text="-", font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=text_color)
        self.label_valor.pack(padx=10, pady=(0, 10))
    
    def atualizar_alergia(self, texto_alergia):
        self.label_valor.configure(text=texto_alergia)

class CardQueixa(customtkinter.CTkFrame):
    """Card para exibir a queixa principal do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.label_titulo = customtkinter.CTkLabel(self, text="Principal queixa", text_color=text_color, font=customtkinter.CTkFont(family="Segoe UI", size=14))
        self.label_titulo.pack(padx=10, pady=(10, 0))
        self.label_valor = customtkinter.CTkLabel(self, text="-", text_color=text_color, font=customtkinter.CTkFont(family="Segoe UI", size=18, weight="bold"), wraplength=300)
        self.label_valor.pack(padx=10, pady=(0, 10), expand=True, fill="x")

    def atualizar_queixa(self, texto_queixa):
        self.label_valor.configure(text=texto_queixa)

class CardRelatorioPaciente(customtkinter.CTkFrame):
    """Card para exibir a grade completa de sinais vitais."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.titulo_card = customtkinter.CTkLabel(self, text="Relatório médico", font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=text_color)
        self.titulo_card.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))
        self.label_temp_valor = self._criar_dado_medico(1, 0, "Temperatura", "-- °C", text_color)
        self.label_sat_valor = self._criar_dado_medico(1, 1, "Saturação", "-- %", text_color)
        self.label_sat_ar_valor = self._criar_dado_medico(1, 2, "Saturação do ar", "-- %", text_color)
        self.label_fc_valor = self._criar_dado_medico(2, 0, "Frequência cardíaca", "-- bpm", text_color)
        self.label_fr_valor = self._criar_dado_medico(2, 1, "Frequência respiratória", "-- rpm", text_color)
        self.label_dor_valor = self._criar_dado_medico(2, 2, "Dor", "--", text_color)
        self.label_pa_sis_valor = self._criar_dado_medico(3, 0, "Pressão sistólica", "-- mmHg", text_color)
        self.label_pa_dias_valor = self._criar_dado_medico(3, 1, "Pressão diastólica", "-- mmHg", text_color)
        self.label_perfusao_valor = self._criar_dado_medico(3, 2, "Perfusão periférica", "-- s", text_color)

    def _criar_dado_medico(self, row, col, titulo, valor, text_color):
        frame_dado = customtkinter.CTkFrame(self, fg_color="transparent")
        frame_dado.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        customtkinter.CTkLabel(frame_dado, text=titulo, font=customtkinter.CTkFont(family="Segoe UI", size=14), text_color=text_color).pack()
        label_valor = customtkinter.CTkLabel(frame_dado, text=valor, font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=text_color)
        label_valor.pack()
        return label_valor

    def atualizar_dados(self, dados: dict):
        self.label_temp_valor.configure(text=f'{dados.get("temperatura", "--")} °C')
        self.label_sat_valor.configure(text=f'{dados.get("saturacao", "--")} %')
        self.label_sat_ar_valor.configure(text=f'{dados.get("saturacao_ar", "--")} %')
        self.label_fc_valor.configure(text=f'{dados.get("frequencia_cardiaca", "--")} bpm')
        self.label_fr_valor.configure(text=f'{dados.get("frequencia_respiratoria", "--")} rpm')
        self.label_dor_valor.configure(text=f'{dados.get("dor", "--")}')
        self.label_pa_sis_valor.configure(text=f'{dados.get("pressao_sistolica", "--")} mmHg')
        self.label_pa_dias_valor.configure(text=f'{dados.get("pressao_diastolica", "--")} mmHg')
        self.label_perfusao_valor.configure(text=f'{dados.get("perfusao", "--")} s')

class CardPrevisto(customtkinter.CTkFrame):
    """Card para exibir as previsões de desfecho."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.titulo = customtkinter.CTkLabel(self, text="Previsto", font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=text_color)
        self.titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        uti_frame = customtkinter.CTkFrame(self, border_width=5, border_color="#E74C3C")
        uti_frame.grid(row=1, column=0, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(uti_frame, text="UTI").pack(pady=(10, 0))
        self.label_uti_valor = customtkinter.CTkLabel(uti_frame, text="--%", font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.label_uti_valor.pack(pady=(0, 10))

        internacao_frame = customtkinter.CTkFrame(self, border_width=5, border_color="#F39C12")
        internacao_frame.grid(row=1, column=1, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(internacao_frame, text="Internação").pack(pady=(10, 0))
        self.label_internacao_valor = customtkinter.CTkLabel(internacao_frame, text="--%", font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.label_internacao_valor.pack(pady=(0, 10))

        alta_frame = customtkinter.CTkFrame(self, border_width=5, border_color="#2ECC71")
        alta_frame.grid(row=1, column=2, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(alta_frame, text="Alta").pack(pady=(10, 0))
        self.label_alta_valor = customtkinter.CTkLabel(alta_frame, text="--%", font=customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.label_alta_valor.pack(pady=(0, 10))

    def atualizar_dados(self, uti_pct, internacao_pct, alta_pct):
        self.label_uti_valor.configure(text=uti_pct)
        self.label_internacao_valor.configure(text=internacao_pct)
        self.label_alta_valor.configure(text=alta_pct)

class CardSintomas(customtkinter.CTkFrame):
    """Card para listar os sintomas do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.text_color = text_color
        self.titulo = customtkinter.CTkLabel(self, text="Sintomas", font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=self.text_color)
        self.titulo.pack(anchor="w", padx=10, pady=(10, 5))
        self.sintomas_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.sintomas_container.pack(anchor="w", expand=True, fill="x", padx=10, pady=(0, 10))

    def atualizar_sintomas(self, lista_sintomas: list):
        for widget in self.sintomas_container.winfo_children():
            widget.destroy()
        if not lista_sintomas:
            customtkinter.CTkLabel(self.sintomas_container, text="Nenhum sintoma relatado.", font=customtkinter.CTkFont(family="Segoe UI", size=14), text_color="gray").pack(anchor="w")
            return
        for sintoma in lista_sintomas:
            frame = customtkinter.CTkFrame(self.sintomas_container, fg_color="transparent")
            quadrado = customtkinter.CTkFrame(frame, width=10, height=10, fg_color="#2ECC71", corner_radius=3)
            quadrado.pack(side="left", padx=(0, 8), pady=4)
            label = customtkinter.CTkLabel(frame, text=sintoma, font=customtkinter.CTkFont(family="Segoe UI", size=14), text_color=self.text_color)
            label.pack(side="left", anchor="w")
            frame.pack(anchor="w", fill="x")

class CardEvolucao(customtkinter.CTkFrame):
    """Card para exibir a linha de evolução do atendimento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.text_color = text_color
        self.titulo = customtkinter.CTkLabel(self, text="Linha de Evolução", font=customtkinter.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=self.text_color)
        self.titulo.pack(anchor="w", padx=10, pady=(10, 5))
        self.eventos_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.eventos_container.pack(anchor="w", expand=True, fill="both", padx=10, pady=(0, 10))

    def atualizar_evolucao(self, lista_eventos: list):
        for widget in self.eventos_container.winfo_children():
            widget.destroy()
        if not lista_eventos:
            customtkinter.CTkLabel(self.eventos_container, text="Nenhum evento registrado.", font=customtkinter.CTkFont(family="Segoe UI", size=14), text_color="gray").pack(anchor="w")
            return
        for evento in lista_eventos:
            label = customtkinter.CTkLabel(self.eventos_container, text=evento, font=customtkinter.CTkFont(family="Segoe UI", size=14), text_color=self.text_color, anchor="w", justify="left")
            label.pack(anchor="w", fill="x")


class PaginaStatusPaciente(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#F2F2F2", **kwargs)
        
        self.pacientes_db = self._carregar_banco_de_dados()
        self.lista_nomes_pacientes = list(self.pacientes_db.keys())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        customtkinter.CTkLabel(self.header_frame, text="Painel de acompanhamento do Paciente", font=customtkinter.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#2980B9").grid(row=0, column=0, sticky="w")
        
        self.paciente_selecionado_var = customtkinter.StringVar(value=self.lista_nomes_pacientes[0])
        self.menu_pacientes = customtkinter.CTkOptionMenu(self.header_frame, values=self.lista_nomes_pacientes, command=self._paciente_selecionado, variable=self.paciente_selecionado_var, width=250)
        self.menu_pacientes.grid(row=0, column=2, padx=(0, 10))

        self.dashboard_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.dashboard_frame.grid_columnconfigure(0, weight=2)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)

        # -- Coluna Esquerda --
        self.card_info = CardInfoPaciente(self.dashboard_frame, fg_color="white", text_color="black")
        self.card_info.grid(row=0, column=0, padx=10, pady=(10,2), sticky="ew")

        risco_alergia_container = customtkinter.CTkFrame(self.dashboard_frame, fg_color="transparent")
        risco_alergia_container.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        risco_alergia_container.grid_columnconfigure((0, 1), weight=1)
        self.card_risco = CardClassificacaoRisco(risco_alergia_container, fg_color="white")
        self.card_risco.grid(row=0, column=0, padx=10, pady=(0,0), sticky="nsew")
        self.card_alergia = CardAlergia(risco_alergia_container, fg_color="white")
        self.card_alergia.grid(row=0, column=1, padx=10, pady=(0,0), sticky="nsew")

        self.card_queixa = CardQueixa(self.dashboard_frame, fg_color="white")
        self.card_queixa.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.card_relatorio = CardRelatorioPaciente(self.dashboard_frame, fg_color="white")
        self.card_relatorio.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # -- Coluna Direita --
        self.card_previsto = CardPrevisto(self.dashboard_frame, fg_color="white")
        self.card_previsto.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_sintomas = CardSintomas(self.dashboard_frame, fg_color="white")
        self.card_sintomas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_evolucao = CardEvolucao(self.dashboard_frame, fg_color="white")
        self.card_evolucao.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.dashboard_frame.grid_rowconfigure(3, weight=1)
        self.carregar_dados_paciente(self.pacientes_db[self.lista_nomes_pacientes[0]])

    def _carregar_banco_de_dados(self):
        return {
            "Joana Martins (8 anos)": {
                "info": {"nome": "Joana Martins", "idade": 8, "sexo": "Feminino", "peso": 25},
                "triagem": {"risco": "Amarelo (Urgente)", "cor": "#F1C40F", "alergia": "Nenhuma", "queixa": "Febre e dor de cabeça há 1 dia."},
                "relatorio": {"temperatura": 38.8, "saturacao": 98, "saturacao_ar": 99, "frequencia_cardiaca": 125, "frequencia_respiratoria": 26, "dor": "6/10", "pressao_sistolica": 105, "pressao_diastolica": 65, "perfusao": 1},
                "previsao": {"uti": "1.5%", "internacao": "15.0%", "alta": "83.5%"},
                "sintomas": ["Febre", "Dor de cabeça"],
                "evolucao": ["02/10/2025 10:00 - Entrada na pediatria", "02/10/2025 10:10 - Triagem pediátrica completa", "02/10/2025 10:45 - Aguardando avaliação médica"]
            },
            "Lucas Pereira (2 anos)": {
                "info": {"nome": "Lucas Pereira", "idade": 2, "sexo": "Masculino", "peso": 12.5},
                "triagem": {"risco": "Laranja (Preferencial)", "cor": "#E67E22", "alergia": "Nenhuma", "queixa": "Dificuldade para respirar e chiado no peito.", "dor": "Não informado"},
                "relatorio": {"temperatura": 37.9, "saturacao": 93, "saturacao_ar": 94, "frequencia_cardiaca": 145, "frequencia_respiratoria": 45, "dor": "N/A", "pressao_sistolica": 95, "pressao_diastolica": 60, "perfusao": 1},
                "previsao": {"uti": "18.0%", "internacao": "75.0%", "alta": "7.0%"},
                "sintomas": ["Tosse", "Chiado"],
                "evolucao": ["02/10/2025 11:30 - Chegada com desconforto respiratório", "02/10/2025 11:32 - Triagem e encaminhamento para sala de emergência", "02/10/2025 11:40 - Iniciado oxigênio e medicação inalatória"]
            },
            "Sofia Ribeiro (5 anos)": {
                "info": {"nome": "Sofia Ribeiro", "idade": 5, "sexo": "Feminino", "peso": 18},
                "triagem": {"risco": "Verde (Pouco Urgente)", "cor": "#2ECC71", "alergia": "Amoxicilina", "queixa": "Corte pequeno no joelho após queda no parque."},
                "relatorio": {"temperatura": 36.7, "saturacao": 99, "saturacao_ar": 99, "frequencia_cardiaca": 95, "frequencia_respiratoria": 22, "dor": "2/10", "pressao_sistolica": 100, "pressao_diastolica": 62, "perfusao": 1},
                "previsao": {"uti": "0.1%", "internacao": "1.0%", "alta": "98.9%"},
                "sintomas": ["Escoriação", "Sangramento leve contido"],
                "evolucao": ["02/10/2025 12:05 - Chegada para sutura", "02/10/2025 12:15 - Triagem realizada", "02/10/2025 12:20 - Aguardando procedimento ambulatorial"]
            }
        }

    def _paciente_selecionado(self, nome_do_paciente: str):
        dados_do_paciente = self.pacientes_db[nome_do_paciente]
        self.carregar_dados_paciente(dados_do_paciente)

    def carregar_dados_paciente(self, dados: dict):
        info = dados.get("info", {})
        self.card_info.atualizar_dados(nome=info.get("nome", "-"), idade=info.get("idade", "-"), sexo=info.get("sexo", "-"), peso=info.get("peso", "-"))

        triagem = dados.get("triagem", {})
        self.card_risco.atualizar_risco(texto_risco=triagem.get("risco", "-"), cor_risco=triagem.get("cor", "gray"))
        self.card_alergia.atualizar_alergia(texto_alergia=triagem.get("alergia", "-"))
        self.card_queixa.atualizar_queixa(texto_queixa=triagem.get("queixa", "-"))
        
        relatorio = dados.get("relatorio", {})
        self.card_relatorio.atualizar_dados(relatorio)

        previsao = dados.get("previsao", {})
        self.card_previsto.atualizar_dados(uti_pct=previsao.get("uti", "-"), internacao_pct=previsao.get("internacao", "-"), alta_pct=previsao.get("alta", "-"))

        sintomas = dados.get("sintomas", [])
        self.card_sintomas.atualizar_sintomas(sintomas)

        evolucao = dados.get("evolucao", [])
        self.card_evolucao.atualizar_evolucao(evolucao)