import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Análise Avançada - Feminicídio MT", 
    page_icon="", 
    layout="wide"
)

st.title(" Análise Avançada de Violência de Gênero em MT")
st.markdown("Filtre e cruze dados reais e consolidados por municípios e perfil das vítimas ao longo dos últimos 10 anos.")

# 2. Função otimizada para ler o ficheiro CSV
@st.cache_data
def carregar_dados_detalhados():
    try:
        df = pd.read_csv("dados_feminicidio_detalhado_mt.csv")
        return df
    except FileNotFoundError:
        st.error("O ficheiro 'dados_feminicidio_detalhado_mt.csv' não foi encontrado na pasta.")
        return None

df = carregar_dados_detalhados()

if df is not None:
    # --- BARRA LATERAL DE FILTROS (SIDEBAR) ---
    st.sidebar.header("Filtros de Pesquisa")

    # Filtro de Ano (Aproveitando os 10 anos de histórico)
    ano_min = int(df['Ano'].min())
    ano_max = int(df['Ano'].max())
    anos_selecionados = st.sidebar.slider(
        "Selecione o Período (Anos):",
        min_value=ano_min,
        max_value=ano_max,
        value=(ano_min, ano_max)
    )

    # Filtros de Texto
    todas_cidades = ["Todas"] + sorted(df['Cidade'].unique().tolist())
    cidade_selecionada = st.sidebar.selectbox("Selecione a Cidade:", todas_cidades)

    todas_faixas = ["Todas"] + sorted(df['Faixa_Etaria'].unique().tolist())
    faixa_selecionada = st.sidebar.selectbox("Faixa Etária da Vítima:", todas_faixas)

    # Aplicando filtros aplicados consecutivamente
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[(df_filtrado['Ano'] >= anos_selecionados[0]) & (df_filtrado['Ano'] <= anos_selecionados[1])]
    
    if cidade_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade_selecionada]
    if faixa_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Faixa_Etaria'] == faixa_selecionada]

    # --- NOVO GRÁFICO: LINHA DO TEMPO (OCUPA A LARGURA TODA) ---
    st.subheader(" Evolução Temporal dos Casos (Série Histórica)")
    casos_por_ano = df_filtrado['Ano'].value_counts().reset_index()
    casos_por_ano.columns = ['Ano', 'Total de Casos']
    casos_por_ano = casos_por_ano.sort_values(by='Ano')

    fig_linha = px.line(
        casos_por_ano,
        x='Ano',
        y='Total de Casos',
        markers=True,
        color_discrete_sequence=['#e63946']
    )
    # Garante que o eixo X exiba os anos corretamente sem quebrar em decimais
    fig_linha.update_layout(xaxis=dict(tickmode='linear'))
    st.plotly_chart(fig_linha, width="stretch")

    st.markdown("---")

    # --- APRESENTAÇÃO DOS GRÁFICOS SECUNDÁRIOS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Ocorrências por Município")
        casos_cidade = df_filtrado['Cidade'].value_counts().reset_index()
        casos_cidade.columns = ['Cidade', 'Total de Casos']
        
        fig_cidade = px.bar(
            casos_cidade, 
            x='Total de Casos', 
            y='Cidade', 
            orientation='h',
            color='Total de Casos',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_cidade, width="stretch")

    with col2:
        st.subheader(" Distribuição por Faixa Etária")
        fig_idade = px.pie(
            df_filtrado, 
            names='Faixa_Etaria', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.OrRd[::-1]
        )
        st.plotly_chart(fig_idade, width="stretch")

    st.markdown("---")

    col3, col4 = st.columns(2)

    if 'Meio_Utilizado' in df_filtrado.columns:
        with col3:
            st.subheader(" Meio Utilizado nos Crimes")
            fig_meio = px.histogram(df_filtrado, x='Meio_Utilizado', color='Meio_Utilizado', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_meio, width="stretch")

    if 'Raca_Cor' in df_filtrado.columns:
        with col4:
            st.subheader(" Distribuição por Raça/Cor")
            casos_raca = df_filtrado['Raca_Cor'].value_counts().reset_index()
            casos_raca.columns = ['Raça/Cor', 'Casos']
            fig_raca = px.bar(casos_raca, x='Raça/Cor', y='Casos', color='Raça/Cor')
            st.plotly_chart(fig_raca, width="stretch")

    # Tabela dinâmica final
    st.subheader(" Registros Filtrados em Tempo Real")
    st.dataframe(df_filtrado, width="stretch")