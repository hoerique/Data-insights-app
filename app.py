import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Meta ADS", layout="wide")
st.title("📊 Dashboard De Tráfego Pago")

# Layout do cabeçalho
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.text("👋 Olá, seja bem-vindo!")
with col2:
    st.markdown(
        """
        <div style='text-align: right;'>
            <a href='https://www.linkedin.com/in/erique-ferreira-6451382a2' target='_blank'>
                <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='25'> LinkedIn
            </a>  
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para carregar os dados
@st.cache_data
def load_data():
    try:
        url = "https://raw.githubusercontent.com/hoerique/Data-insights-app/main/campanhas_Meta_ads.xlsx"
        data = pd.read_excel(url, decimal=",")
        data["data_inicio"] = pd.to_datetime(data["data_inicio"], errors="coerce")
        data.rename(columns={"impressões": "impressoes"}, inplace=True)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None  # Retorna None para evitar erros ao acessar 'data'

# Carregar os dados
data = load_data()

# Verificar se os dados foram carregados corretamente
if data is not None and not data.empty:
    # Barra lateral - Filtros
    st.sidebar.header("🎯 Filtros")
    
    campanha_selecionada = st.sidebar.selectbox("📌 Selecione a Campanha", ["Todas"] + data["nome_campanha"].dropna().unique().tolist())
    tipo_selecionado = st.sidebar.selectbox("📊 Tipo de Campanha", ["Todos"] + data["tipo_campanha"].dropna().unique().tolist())
    
    data_inicio, data_final = data["data_inicio"].min(), data["data_inicio"].max()
    data_selecionada = st.sidebar.date_input("📅 Período", [data_inicio, data_final])
    
    # Aplicação de filtros
    dados_filtrados = data.copy()
    if campanha_selecionada != "Todas":
        dados_filtrados = dados_filtrados[dados_filtrados["nome_campanha"] == campanha_selecionada]
    if tipo_selecionado != "Todos":
        dados_filtrados = dados_filtrados[dados_filtrados["tipo_campanha"] == tipo_selecionado]
    if len(data_selecionada) == 2:
        dados_filtrados = dados_filtrados[
            (dados_filtrados["data_inicio"] >= pd.to_datetime(data_selecionada[0])) & 
            (dados_filtrados["data_inicio"] <= pd.to_datetime(data_selecionada[1]))
        ]

    # Função para calcular métricas
    def calcular_metricas(df):
        return {
            "Impressões": df["impressoes"].sum(),
            "Cliques": df["cliques"].sum(),
            "CTR (%)": (df["cliques"].sum() / df["impressoes"].sum()) * 100 if df["impressoes"].sum() > 0 else 0,
            "Investimento Total": df["investimento"].sum(),
            "CPC Médio": df["CPC"].mean(),
            "CPM Médio": df["CPM"].mean(),
        }

    # Calcular métricas e exibir
    metricas = calcular_metricas(dados_filtrados)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("📢 Impressões", f"{metricas['Impressões']:,}".replace(",", "."))
    col2.metric("🖱️ Cliques", f"{metricas['Cliques']:,}".replace(",", "."))
    col3.metric("📊 CTR", f"{metricas['CTR (%)']:.2f}%")
    col4.metric("💰 Investimento", f"R$ {metricas['Investimento Total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col5.metric("⚡ CPC", f"R$ {metricas['CPC Médio']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col6.metric("📈 CPM", f"R$ {metricas['CPM Médio']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Exibir tabela de dados filtrados
    st.subheader("📋 Dados das Campanhas")
    st.dataframe(dados_filtrados)

    # Gráfico de barras - Criativos com maior investimento e impressões
    with st.sidebar.expander("📌 Filtro por Criativos", expanded=False):
        campanhas_selecionadas = st.multiselect("Selecione Campanhas", data["nome_campanha"].unique(), default=data["nome_campanha"].unique())
    
    if campanhas_selecionadas:
        df_filtrado = data[data["nome_campanha"].isin(campanhas_selecionadas)]
        df_melted = df_filtrado.melt(id_vars=["nome_campanha"], value_vars=["investimento", "impressoes"], var_name="Métrica", value_name="Valor")
        
        fig = px.bar(df_melted, x="Valor", y="nome_campanha", color="Métrica", orientation="h", barmode="group")
        fig.update_layout(title="💡 Criativos com Maior Investimento e Impressões", xaxis_title="Valor", yaxis_title="Campanha")
        st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("⚠️ Nenhum dado foi carregado. Verifique a fonte de dados e tente novamente.")


