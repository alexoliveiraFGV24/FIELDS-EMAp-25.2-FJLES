import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import gui.config as config



class CardPrevisto(customtkinter.CTkFrame):
    """Um widget customizado para o card 'Previsto'."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.titulo = customtkinter.CTkLabel(self, text="Previsto")
        self.titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")# Sub-card UTI
        uti_frame = customtkinter.CTkFrame(self, border_width=2, border_color="#E74C3C")
        uti_frame.grid(row=1, column=0, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(uti_frame, text="UTI").pack(pady=(10, 0))
        self.label_uti_valor = customtkinter.CTkLabel(uti_frame, text="0,00%", font=("", 18, "bold"))
        self.label_uti_valor.pack(pady=(0, 10))
        # Sub-card Internação
        internacao_frame = customtkinter.CTkFrame(self, border_width=2, border_color="#F39C12")
        internacao_frame.grid(row=1, column=1, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(internacao_frame, text="Internação").pack(pady=(10, 0))
        self.label_internacao_valor = customtkinter.CTkLabel(internacao_frame, text="0,00%", font=("", 18, "bold"))
        self.label_internacao_valor.pack(pady=(0, 10))
        # Sub-card Alta
        alta_frame = customtkinter.CTkFrame(self, border_width=2, border_color="#2ECC71")
        alta_frame.grid(row=1, column=2, padx=7, pady=10, sticky="nsew")
        customtkinter.CTkLabel(alta_frame, text="Alta").pack(pady=(10, 0))
        self.label_alta_valor = customtkinter.CTkLabel(alta_frame, text="0,00%", font=("", 18, "bold"))
        self.label_alta_valor.pack(pady=(0, 10))

    def atualizar_dados(self, uti_pct, internacao_pct, alta_pct):
        self.label_uti_valor.configure(text=uti_pct)
        self.label_internacao_valor.configure(text=internacao_pct)
        self.label_alta_valor.configure(text=alta_pct)

class CardInfoPaciente(customtkinter.CTkFrame):
    """Um widget customizado para o card de informações do paciente."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.label_nome = customtkinter.CTkLabel(self, text="Nome: -")
        self.label_nome.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")
        self.label_idade = customtkinter.CTkLabel(self, text="Idade: -")
        self.label_idade.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.label_sexo = customtkinter.CTkLabel(self, text="Sexo: -")
        self.label_sexo.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.label_peso = customtkinter.CTkLabel(self, text="Peso: -")
        self.label_peso.grid(row=3, column=0, padx=15, pady=(5, 10), sticky="w")

    def atualizar_dados(self, nome, idade, sexo, peso):
        self.label_nome.configure(text=f"Nome: {nome}")
        self.label_idade.configure(text=f"Idade: {idade} anos")
        self.label_sexo.configure(text=f"Sexo: {sexo}")
        self.label_peso.configure(text=f"Peso: {peso} kg")

class CardClassificacaoRiscoPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        customtkinter.CTkLabel(self, text="Classificação de Risco\nLaranja (Preferencial)").pack(padx=10, pady=10)

class CardAlergiaPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        customtkinter.CTkLabel(self, text="Alergia\nNão").pack(padx=10, pady=10)

class CardQueixaPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        self.texto_queixa = ""
        customtkinter.CTkLabel(self, text=f"Principal Queixa\n{self.texto_queixa}").pack(padx=10, pady=10)

class CardRelatorioPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        customtkinter.CTkLabel(self, text="Relatório Médico (Conteúdo aqui)").pack(padx=10, pady=10)

class CardSintomasPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)
        customtkinter.CTkLabel(self, text="Sintomas (Conteúdo aqui)").pack(padx=10, pady=10)

class CardEvolucaoPaciente(customtkinter.CTkFrame):
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master,  **kwargs)
        customtkinter.CTkLabel(self, text="Linha de Evolução (Conteúdo aqui)").pack(padx=10, pady=10)


class PaginaStatusPaciente(customtkinter.CTkFrame):
    def __init__(self, master,text_color="black", **kwargs):

        super().__init__(master, fg_color="#F2F2F2", **kwargs)

        # ESTRUTURA PRINCIPAL DA PÁGINA 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # CABEÇALHO 
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.header_frame.grid_columnconfigure(0, weight=1) # Título expande
        
        customtkinter.CTkLabel(self.header_frame, text="Painel de acompanhamento do Paciente", font=customtkinter.CTkFont(size=20, weight="bold"), text_color="#2980B9").grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(self.header_frame, text="ID000654", font=customtkinter.CTkFont(size=14)).grid(row=0, column=1, padx=20)
        customtkinter.CTkOptionMenu(self.header_frame, values=["Buscar Paciente..."]).grid(row=0, column=2, padx=(0, 10))



        # FRAME DO DASHBOARD 

        self.dashboard_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.dashboard_frame.grid_columnconfigure(0, weight=2)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)

        self.card_info = CardInfoPaciente(self.dashboard_frame, fg_color="white", text_color="black")
        self.card_info.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        risco_alergia_container = customtkinter.CTkFrame(self.dashboard_frame, fg_color="transparent")
        risco_alergia_container.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        risco_alergia_container.grid_columnconfigure((0, 1), weight=1)
        
        self.card_risco = CardClassificacaoRiscoPaciente(risco_alergia_container, fg_color="white")
        self.card_risco.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.card_alergia = CardAlergiaPaciente(risco_alergia_container, fg_color="white")
        self.card_alergia.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_queixa = CardQueixaPaciente(self.dashboard_frame, fg_color="white")
        self.card_queixa.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.card_relatorio = CardRelatorioPaciente(self.dashboard_frame, fg_color="white")
        self.card_relatorio.grid(row=3, column=0, padx=10, pady=10, sticky="ew")



        self.card_previsto = CardPrevisto(self.dashboard_frame, fg_color="white")
        self.card_previsto.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_sintomas = CardSintomasPaciente(self.dashboard_frame, fg_color="white")
        self.card_sintomas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_evolucao = CardEvolucaoPaciente(self.dashboard_frame, fg_color="white")
        self.card_evolucao.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.dashboard_frame.grid_rowconfigure(3, weight=1)

        # carregando dados iniciais
        self.carregar_dados_paciente()

    def carregar_dados_paciente(self):
        
        self.card_info.atualizar_dados(
            nome="Amélia da Silva Ferreira", idade=42, sexo="Feminino", peso=64
        )
        self.card_previsto.atualizar_dados(
            uti_pct="23,78%", internacao_pct="68,91%", alta_pct="7,31%"
        )