import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict
from utils import probs


# pacientes
class Paciente:
    """
    Representa um único paciente com seus dados e probabilidades de destino.
    """
    def __init__(self, id_paciente: int, hora_chegada: datetime, prob_uti: float, prob_internacao: float, prob_alta: float):
        # validando probs
        if not (0.0 <= prob_uti <= 1.0 and 0.0 <= prob_internacao <= 1.0 and 0.0 <= prob_alta <= 1.0):
            raise ValueError("As probabilidades devem estar entre 0 e 1.")

        self.id_paciente = id_paciente
        self.hora_chegada = hora_chegada
        self.prob_uti = prob_uti
        self.prob_internacao = prob_internacao
        self.prob_alta = prob_alta

    def __repr__(self):
        return f"<Paciente id={self.id_paciente}, chegada={self.hora_chegada.strftime('%Y-%m-%d %H:%M')}>"


# fila
class FilaAtendimento:
    """
    gerencia a lista de pacientes que estão atualmente na fila.
    """
    def __init__(self):
        # Inicializa a fila como uma lista vazia.
        self.pacientes_na_fila: List[Paciente] = []
    
    def adicionar_paciente(self, paciente: Paciente):
        """Adiciona um objeto Paciente à lista da fila."""
        self.pacientes_na_fila.append(paciente)

    def get_pacientes_atuais(self) -> List[Paciente]:
        """Retorna a lista completa de pacientes que estão na fila."""
        return self.pacientes_na_fila

    def limpar_fila(self):
        """Esvazia a fila, removendo todos os pacientes."""
        self.pacientes_na_fila.clear()

    def __len__(self):
        """Permite usar len(fila) para saber o número de pacientes."""
        return len(self.pacientes_na_fila)

# simulação fila
class SimuladorFila:
    def __init__(self):
        self.todos_os_pacientes: List[Paciente] = []
        self.fila = FilaAtendimento()
        self.hora_atual: datetime = None

    def carregar_pacientes(self, caminho_arquivo: str):
        try:
            # --- CORREÇÃO PRINCIPAL ---
            # Definindo os nomes exatos das colunas do seu arquivo CSV
            COLUNA_HORA = 'TA_DH_PRE_ATENDIMENTO'
            COLUNA_PROB_ALTA = 'prediction_prob_alta'
            COLUNA_PROB_UI = 'prediction_prob_ui'  # UI = Unidade de Internação
            COLUNA_PROB_UTI = 'prediction_prob_uti'

            # Ao ler o CSV, informamos qual coluna deve ser tratada como data
            # O parâmetro dayfirst=True ajuda o pandas a entender o formato DD/MM/YYYY
            df = pd.read_csv(caminho_arquivo, parse_dates=[COLUNA_HORA], dayfirst=True)

            self.todos_os_pacientes = [] # Limpa a lista antes de carregar
            
            for index, row in df.iterrows():
                paciente = Paciente(
                    id_paciente=index,
                    hora_chegada=row[COLUNA_HORA],
                    prob_alta=row[COLUNA_PROB_ALTA],
                    prob_internacao=row[COLUNA_PROB_UI],
                    prob_uti=row[COLUNA_PROB_UTI]
                )
                self.todos_os_pacientes.append(paciente)
                    
                print(f"Sucesso! {len(self.todos_os_pacientes)} pacientes carregados do arquivo.", icon="✅")

        except FileNotFoundError:
            print(f"Arquivo não encontrado em '{caminho_arquivo}'. Verifique o caminho.")
        except KeyError as e:
            print(f"Erro de coluna: A coluna {e} não foi encontrada no CSV. Verifique o cabeçalho do arquivo.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
            
    def atualizar_fila_para_horario(self, novo_horario: datetime):
        """
        Atualiza o estado da simulação para um horário específico.
        """
        self.hora_atual = novo_horario
        
        self.fila.limpar_fila()
        
        for paciente in self.todos_os_pacientes:
            if paciente.hora_chegada <= self.hora_atual:
                self.fila.adicionar_paciente(paciente)

    def calcular_previsoes(self) -> Dict[str, float]:
        pacientes_na_fila = self.fila.get_pacientes_atuais()

        if not pacientes_na_fila:
            return {'uti': np.array([1.]), 'internacao': np.array([1.]), 'alta': np.array([1.])}

        pacientes_array = np.array([
            [p.prob_uti, p.prob_internacao, p.prob_alta]
            for p in pacientes_na_fila
        ])

        
        # Vetores de probabilidades
        probs_utis = pacientes_array[:, 0]
        probs_internacao = pacientes_array[:, 1]
        probs_altas = pacientes_array[:, 2]
        
        #Histogramas
        dist_uti = np.array([1 - probs_utis[0], probs_utis[0]])
        for p in probs_utis[1:]:
            dist_uti = np.convolve(dist_uti, [1 - p, p])

        dist_internacao = np.array([1 - probs_internacao[0], probs_internacao[0]])
        for p in probs_internacao[1:]:
            dist_internacao = np.convolve(dist_internacao, [1 - p, p])

        
        dist_altas = np.array([1 - probs_altas[0], probs_altas[0]])
        for p in probs_altas[1:]:
            dist_altas = np.convolve(dist_altas, [1 - p, p])

        #cumulativas
        dist_uti_cumulativa = np.cumsum(dist_uti[::-1])[::-1]
        dist_internacao_cumulativa = np.cumsum(dist_internacao[::-1])[::-1]
        dist_altas_cumulativa = np.cumsum(dist_altas[::-1])[::-1]

        
        return {
            'uti': dist_uti_cumulativa,
            'internacao': dist_internacao_cumulativa,
            'alta': dist_altas_cumulativa
        }

# interface streamlit
class PaginaFila:
    def __init__(self, caminho_dados_pacientes: str):
        self.simulador = SimuladorFila()
        self.simulador.carregar_pacientes_do_excel(caminho_dados_pacientes)

    def obter_estado_da_fila(self, horario_desejado: datetime) -> Dict:
        """
        faz as chamadas ao simulador e retorna um dicionário 
        com todos os dados prontos para serem exibidos.
        """
        self.simulador.atualizar_fila_para_horario(horario_desejado)

        distribuicoes = self.simulador.calcular_distribuicao_convolucao()


        num_pacientes_fila = len(self.simulador.fila)

        return {
            "num_pacientes": num_pacientes_fila,
            "dist_uti": distribuicoes['uti'],
            "dist_internacao": distribuicoes['internacao'],
            "dist_alta": distribuicoes['alta'],
        }


if __name__ == "__main__":
    simulador = SimuladorFila()
    caminho_do_seu_arquivo = 'files/data/probabilidades.csv' 
    simulador.carregar_pacientes_do_csv(caminho_do_seu_arquivo)