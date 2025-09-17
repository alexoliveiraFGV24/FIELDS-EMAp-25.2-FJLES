import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Dashboard Hospitalar")

# --- CSS CUSTOMIZADO PARA AS CAIXAS COLORIDAS ---
# Usamos isso para criar os painéis com bordas coloridas, como na imagem.
st.markdown("""
<style>
.metric-box {
    border: 2px solid;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    margin: 5px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
.metric-box h3 {
    font-size: 18px;
    margin-bottom: 5px;
    color: #555;
}
.metric-box .value {
    font-size: 36px;
    font-weight: bold;
    line-height: 1;
}
.metric-box .unit {
    font-size: 16px;
    color: #777;
}
.red-border { border-color: #ff4b4b; }
.orange-border { border-color: #ff9900; }
.yellow-border { border-color: #ffcc00; }
.blue-border { border-color: #0099ff; }
.green-border { border-color: #28a745; }
</style>
""", unsafe_allow_html=True)


# --- DADOS DE EXEMPLO (MOCK DATA) ---
# No futuro, substituiremos isso pelos seus dados e cálculos reais.

def gerar_dados():
    """Gera todos os dados falsos necessários para o dashboard."""
    # Métrica principal da esquerda
    kpis = {
        "total_pacientes": np.random.randint(40, 60),
        "previsao_alta": np.random.randint(15, 25),
        "previsao_internacao": np.random.randint(15, 25),
        "previsao_uti": np.random.randint(5, 12),
    }

    # Dados para o gráfico de barras de volume
    horas = np.arange(0, 24)
    # Padrão de volume: baixo de madrugada, pico de manhã, vale à tarde, pico à noite
    volume_base = (np.sin(np.linspace(0, 2 * np.pi, 24)) * 3 + 
                   np.sin(np.linspace(0, 4 * np.pi, 24)) * 2 + 6)
    ocorrencias = np.maximum(0, np.round(volume_base + np.random.rand(24) * 2)).astype(int)
    
    # Hora atual para dividir "Passado" e "Futuro"
    hora_atual = datetime.now().hour
    periodo = ['Passado' if h < hora_atual else 'Futuro' for h in horas]
    
    volume_df = pd.DataFrame({
        "Horário do Dia": horas,
        "Ocorrências": ocorrencias,
        "Período": periodo
    })

    # Dados para as caixas de tempo
    tempos = {
        "tratamento": [np.random.randint(25, 35) for _ in range(5)],
        "espera": [np.random.randint(25, 35) for _ in range(5)]
    }
    
    return kpis, volume_df, tempos

# Carrega os dados
kpis, volume_df, tempos = gerar_dados()


# --- LAYOUT DO DASHBOARD ---

# Abas no topo
tab1, tab2 = st.tabs(["Status Fila Hospital", "Pacientes"])

with tab1:
    # Dividindo a página em duas colunas principais: KPIs à esquerda, gráficos à direita
    left_col, main_col = st.columns([1, 3])

    # --- COLUNA DA ESQUERDA (KPIs) ---
    with left_col:
        st.markdown("##### Métricas Gerais")
        st.metric(label="Total de Pacientes", value=kpis["total_pacientes"])
        st.metric(label="Previsão de Alta", value=kpis["previsao_alta"])
        st.metric(label="Previsão de Internação", value=kpis["previsao_internacao"])
        st.metric(label="Previsão de UTI", value=kpis["previsao_uti"])

    # --- COLUNA PRINCIPAL (GRÁFICOS E TEMPOS) ---
    with main_col:
        # Gráfico de Barras
        st.markdown("##### Volume do PS")
        st.bar_chart(
            volume_df,
            x="Horário do Dia",
            y="Ocorrências",
            color="Período",
            color_discrete_map={'Passado': '#808080', 'Futuro': '#28a745'}
        )

        # Divisor
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Função para criar as caixas de tempo coloridas
        def criar_caixas_de_tempo(titulo, dados, key_prefix):
            st.markdown(f"##### {titulo}")
            cols = st.columns(5)
            cores = ["red-border", "orange-border", "yellow-border", "blue-border", "green-border"]
            for i, col in enumerate(cols):
                with col:
                    # O HTML/CSS que definimos no início é usado aqui
                    st.markdown(f"""
                    <div class="metric-box {cores[i]}">
                        <h3>{i+1}</h3>
                        <p class="value">{dados[i]}</p>
                        <p class="unit">min</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Criando as duas fileiras de caixas
        criar_caixas_de_tempo("Tempo Médio de Tratamento", tempos["tratamento"], "trat")
        criar_caixas_de_tempo("Tempo Médio de Espera", tempos["espera"], "esp")

# Aba "Pacientes" (ainda vazia)
with tab2:
    st.header("Detalhes dos Pacientes")
    st.info("Esta página mostrará uma tabela ou lista detalhada dos pacientes na fila.")
    st.dataframe(pd.DataFrame({
        'ID Paciente': [f'ID-{100+i}' for i in range(15)],
        'Classificação': np.random.randint(1, 6, 15),
        'Tempo de Espera (min)': np.random.randint(5, 90, 15),
        'Localização': ['Espera'] * 15
    }))