import pandas as pd
import numpy as np
from enum import Enum
from datetime import datetime


class Prioridade(Enum):
    UTI = 1
    INTERNACAO = 2
    ALTA = 3


class Paciente:
    def __init__(self, dados):
        self.nome = dados.get('nome', "NOME GENÉRICO PACIENTE")
        self.idade = dados.get('FN_NVL_IDADE_PACIENTE_AMD') # Idade do paciente
        self.hora_chegada = dados.get('TA_DH_PRE_ATENDIMENTO', datetime.now()) # Data e hora do pré-atendimento (Classificação de risco)
        self.classificacao = dados.get('TA_CD_CLASSIFICACAO') # Identificador da categoria de classificação de risco
        self.observacao_enfermeiro = dados.get('TA_DS_OBSERVACAO') # Observações sobre o paciente que foram registradas pelo enfermeiro
        self.especialidade_medica = dados.get('E_DS_ESPECIALID') # Especialidade para qual o paciente foi encaminhado
        self.alergia = dados.get('TA_DS_ALERGIA') # Descrição das alergias registradas na abordagem inicial
        self.queixa_principal = dados.get('TA_DS_QUEIXA_PRINCIPAL') # Descrição da queixa principal relatada pelo responsável pelo paciente
        
        self.prob_uti = None
        self.prob_internacao = None
        self.prob_alta = None

        self.dados = dados
    
    def atualizar_estado(self, novo_estado):
        if not isinstance(novo_estado, Prioridade):
            raise ValueError("novo_estado deve ser um objeto do Prioridade")
        self.estado = novo_estado

    
class Fila:
    def __init__(self):
        self.quantidade_pacientes = 0
        self.pacientes = []  
        
    def adicionar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def tamanho(self):
        return len(self.pacientes)
    
    def predicao_uti(self):
        pass
    
    def predicao_internacao(self):
        pass

    def predicao_alta(self):
        pass

