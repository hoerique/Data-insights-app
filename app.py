import pandas as pd 
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Ola mundo",layout="wide")
st.title("Meu nome erique ferreira dias")


import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/hoerique/Data-insights-app/main/campanhas_Meta_ads.csv",
    parse_dates=["data_inicio", "data_fim"]
)


# Sidebar - Menu de Filtros
st.sidebar.header("🔎 Filtros")

# Filtro por campanha (selectbox)
campanha_selecionada = st.sidebar.selectbox(
    "Selecione uma Campanha",
    options=["Todas"] + list(df["nome_campanha"].unique())
)

# Filtro por tipo de campanha (radio)
tipo_selecionado = st.sidebar.radio(
    "Tipo de Campanha",
    options=["Todas"] + list(df["tipo_campanha"].unique())
)

# Filtro por data (date_input)
min_data = df["data_inicio"].min()
max_data = df["data_fim"].max()
data_inicio, data_fim = st.sidebar.date_input("Período", [min_data, max_data])

# Aplica os filtros
df_filtrado = df.copy()

if campanha_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["nome_campanha"] == campanha_selecionada]

if tipo_selecionado != "Todas":
    df_filtrado = df_filtrado[df_filtrado["tipo_campanha"] == tipo_selecionado]

df_filtrado = df_filtrado[
    (df_filtrado["data_inicio"] >= pd.to_datetime(data_inicio)) &
    (df_filtrado["data_fim"] <= pd.to_datetime(data_fim))
]



# Cálculos
total_impressões = df["impressões"].sum()
total_cliques = df["cliques"].sum()
ctr_medio = df["CTR"].mean() * 100
investimento_total = df["investimento"].sum()
cpc_medio = df["CPC"].mean()
cpm_medio = df["CPM"].mean()

# Agrupar os dados
interacoes = {
    "Salvaram": df["salvaram"].sum(),
    "Compartilharam": df["compartilharam"].sum(),
    "Comentaram": df["comentaram"].sum()
}



# Exibindo as métricas
st.text("📊 Métricas de Campanhas Publicitárias")

col1,col2,col3 =st.columns(3)
with col1:
    st.metric("👁️ Impressões", f"{total_impressões:,}")
    st.metric("💰 Investimento Total", f"R$ {investimento_total:,.2f}")
   

with col2:
    st.metric("🖱️ Cliques", f"{total_cliques:,}")
    st.metric("💸 CPC Médio", f"R$ {cpc_medio:.2f}")


with col3:
    st.metric("📈 CTR Médio", f"{ctr_medio:.2f}%")
    st.metric("📊 CPM Médio", f"R$ {cpm_medio:.2f}")
    



# Gráfico de barras duplas horizontais - Investimento vs Impressões por Campanha
st.subheader("📊 Comparativo: Investimento vs Impressões por Campanha (Horizontal)")

# Agrupa os dados filtrados por campanha
df_agrupado = df_filtrado.groupby("nome_campanha")[["investimento", "impressões"]].sum().reset_index()

# Transforma para formato 'long' para o gráfico
df_long = df_agrupado.melt(
    id_vars="nome_campanha",
    value_vars=["investimento", "impressões"],
    var_name="Métrica",
    value_name="Valor"
)

# Cria gráfico horizontal
fig_barras_horizontais = px.bar(
    df_long,
    x="Valor",
    y="nome_campanha",
    color="Métrica",
    orientation="h",
    barmode="group",
    title="💡 Investimento e Impressões por Campanha (Horizontal)",
    labels={"nome_campanha": "Campanha", "Valor": "Valor"}
)

# Exibe no Streamlit
st.plotly_chart(fig_barras_horizontais, use_container_width=True)


# Criar DataFrame de interações com os dados filtrados
dados_interacoes = pd.DataFrame({
    "Interações": ["Salvaram", "Compartilharam", "Comentaram"],
    "Quantidade": [
        df_filtrado["salvaram"].sum(),
        df_filtrado["compartilharam"].sum(),
        df_filtrado["comentaram"].sum()
    ]
})

# Criar DataFrame de interações com os dados filtrados
dados_interacoes = pd.DataFrame({
    "Interações": ["Salvaram", "Compartilharam", "Comentaram"],
    "Quantidade": [
        df_filtrado["salvaram"].sum(),
        df_filtrado["compartilharam"].sum(),
        df_filtrado["comentaram"].sum()
    ]
})

# Criar gráfico de barras verticais
fig_interacoes = px.bar(
    dados_interacoes,
    x="Interações",
    y="Quantidade",
    color="Interações",
    title="📌 Total de Interações: Salvaram, Compartilharam e Comentaram",
    labels={"Interações": "Tipo de Interação", "Quantidade": "Total"},
    text="Quantidade"
)

# Exibe no app
st.plotly_chart(fig_interacoes, use_container_width=True)

