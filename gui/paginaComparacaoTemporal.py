"""
Módulo da Página de Status do Paciente.

Este arquivo contém a classe principal 'PaginaStatusOperacao' que constrói
e gerencia o dashboard da operação do hospital, bem como todas as classes de componentes
que compõem o dashboard.
"""
import customtkinter


class CardTotalMédicos(customtkinter.CTkFrame):
    """Card para exibir o total de médicos presentes no hospital no momento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)

class CardTotalPacientes(customtkinter.CTkFrame):
    """Card para exibir o total de pacientes no momento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)


class CardPrevisaoUTI(customtkinter.CTkFrame):
    """Card para exibir a previsao de UTIs no momento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)

class CardPrevisaoInternacao(customtkinter.CTkFrame):
    """Card para exibir a previsao de internacoes no momento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)


class CardPrevisaoAlta(customtkinter.CTkFrame):
    """Card para exibir a previsao de altas no momento."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)


class CardDistribuicaoAreas(customtkinter.CTkFrame):
    """Card para exibir a distribuição de ocupação das áreas hospitalares."""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)

class CardVolumeProntoSocorro(customtkinter.CTkFrame):
    """Card para observar o volume do pronto socorro"""
    def __init__(self, master, text_color="black", **kwargs):
        super().__init__(master, **kwargs)


class PaginaComparacaoTemporal(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#F2F2F2", **kwargs)

    def _carregar_banco_de_dados(self):
        return