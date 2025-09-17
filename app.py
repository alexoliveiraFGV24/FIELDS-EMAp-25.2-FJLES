import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

# Assumindo que seu arquivo com as classes (SimuladorFila, etc.) está em gui/classes_streamlit.py
# Este import funcionará se você executar 'streamlit run app.py' da pasta raiz do projeto.
from gui import classes_streamlit 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Simulador de Fila Hospitalar")
st.title("Dashboard de Simulação de Fila Hospitalar")

# --- INICIALIZAÇÃO DO SIMULADOR (COM CACHE) ---
@st.cache_resource
def inicializar_simulador():
    """Cria e carrega o simulador, usando o cache para rodar apenas uma vez."""
    simulador = classes_streamlit.SimuladorFila()
    
    # CORREÇÃO: Usando o nome correto do método que definimos para carregar os dados
    simulador.carregar_pacientes("files/data/probabilidades.csv")
    return simulador

simulador = inicializar_simulador()

# --- BARRA LATERAL COM CONTROLES ---
st.sidebar.header("Controles da Simulação")
horario_selecionado = st.sidebar.slider(
    "Selecione o horário:",
    min_value=time(7, 0), 
    max_value=time(22, 0),
    value=time(14, 0), 
    step=timedelta(minutes=15),
    format="HH:mm"
)
# Usa a data atual para a simulação
data_hora_completa = datetime.combine(datetime.now().date(), horario_selecionado)
st.sidebar.info(f"Simulando para **{data_hora_completa.strftime('%d/%m/%Y %H:%M')}**.")

# LÓGICA PRINCIPAL DA PÁGINA 
simulador.atualizar_fila_para_horario(data_hora_completa)
distribuicoes = simulador.calcular_previsoes()
num_pacientes_fila = len(simulador.fila)

# --- RESULTADOS ---
st.metric(label="Total de Pacientes na Fila", value=f"{num_pacientes_fila} pacientes")
st.markdown("---")
st.subheader("Análise de Risco de Ocupação: P(Demanda ≥ k)")

col1, col2, col3 = st.columns(3)

# função auxiliar para criar os blocos de análise
def criar_bloco_analise(coluna, titulo, dist, default_k, key):
    with coluna:
        st.subheader(titulo)
        
        # CORREÇÃO: Lógica que evita o erro 'StreamlitValueAboveMaxError'
        max_k = max(1, len(dist) - 1)
        valor_padrao_seguro = min(default_k, max_k)
        
        k = st.number_input(
            "Verificar P(Demanda ≥ k)",
            min_value=1,
            max_value=max_k,
            value=valor_padrao_seguro, # Usa o valor padrão seguro e dinâmico
            key=key
        )
        
        if k < len(dist):
            probabilidade = dist[k]
            st.metric(
                label=f"Prob. de precisar de {k} ou mais leitos",
                value=f"{probabilidade:.2%}"
            )

# Criando os blocos para cada destino de forma limpa e segura
criar_bloco_analise(col1, "🏥 UTI", distribuicoes.get('uti', []), 5, "uti")
criar_bloco_analise(col2, "🛌 Internação", distribuicoes.get('internacao', []), 10, "internacao")
criar_bloco_analise(col3, "🏠 Alta", distribuicoes.get('alta', []), 15, "alta")


# --- GRÁFICO DA DISTRIBUIÇÃO COMPLETA ---
st.markdown("---")
st.subheader("Curvas de Probabilidade de Ocupação")

df_chart = pd.DataFrame({
    'UTI': pd.Series(distribuicoes.get('uti')),
    'Internação': pd.Series(distribuicoes.get('internacao')),
    'Alta': pd.Series(distribuicoes.get('alta'))
}).fillna(0)

st.line_chart(df_chart)
st.caption("O eixo X representa o número de leitos/altas (k), e o eixo Y representa a probabilidade P(X ≥ k).")