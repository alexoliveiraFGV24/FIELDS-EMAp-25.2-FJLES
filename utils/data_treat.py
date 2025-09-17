import pandas as pd
import numpy as np
from objects import Paciente
import csv

def carregar_pacientes_csv(file_path) -> list:
    """Lê um arquivo de pacientes e retorna uma lista de objetos Paciente

    Args:
        file_path (string): O caminho do arquivo

    Returns:
        list: lista com os pacientes 
    """

    pacientes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for linha in reader:
                linha['FN_NVL_IDADE_PACIENTE_AMD'] = int(linha['FN_NVL_IDADE_PACIENTE_AMD'])
                linha['TA_CD_CLASSIFICACAO'] = int(linha['TA_CD_CLASSIFICACAO'])

                paciente = Paciente(dados=linha)
                pacientes.append(paciente)

    except FileNotFoundError:
        print(f"O caminho do arquivo {file_path} nao foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None
    
    return pacientes


if __name__ == '__main__':
    pacientes = carregar_pacientes_csv('../files/data/ficticio.csv')
    print(pacientes)
    for p in pacientes:
        print(f"NOME: {p.nome}")
        print(f"IDADE: {p.idade}")
        print(f"QUEIXA PRINCIPAL: {p.queixa_principal}")
        print(f"ALERGIA: {p.alergia}")
        print('_'*50)

