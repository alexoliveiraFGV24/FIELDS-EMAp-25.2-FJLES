import pandas as pd
import numpy as np
from enum import Enum
from datetime import datetime


class Prioridade(Enum):
    UTI = 1
    INTERNACAO = 2
    ALTA = 3


class Paciente:
    def __init__(self, nome, idade, prioridade=0, chegada=None):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade 
        self.chegada = chegada or datetime.now()
        self.prob_uti = None
        self.prob_internacao = None
        self.prob_alta = None
        self.estado = None
        self.chamado = None  
    
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

