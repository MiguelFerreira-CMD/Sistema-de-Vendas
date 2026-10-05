# Titulo - Sistema de Vendas
# Cadastrar Vendas
    # Campo Data
    # Campo Produto -Note, cel e fone
    # Campo Vendedor  - Ana, Bruno e Carla
    # Campo Quantidade 
    # Campo Valor
    # Botão Cadastrar Venda
        # Quando clicar no botão -> Addiconar a venda na tabela, atualizando o dashboard tmb!
# Vendas Cadastradas
    # Tabela com as Vendas
# dashboard
    # Card/Métrica -> Faturamento Total e Produto mais Vendido
    # Gráfico de Barra/Coluna -> Venda por vendedor
    # Grafico de Pizza -> Venda por produto 
    # Grafico de Barra -> Quantidade vendida por produto

# Ferramentas:
    # streamlit, pandas e plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar  a base de Vendas:
tabela_vendas = pd.read_csv("vendas.csv")

st.set_page_config( # .set_page_config -> Troca o titulo da pagina
    page_title="Sistemas de Vendas"
)

# Titulo
st.write("# Sistema de Vendas")

# Seção de Cadstro de Vendas:
st.sidebar.write("## Cadastrar Vendas")
data = st.sidebar.date_input("Data")
vendedor = st.sidebar.selectbox("Vendedor", ["Ana", "Bruno", "Carla"])
produto = st.sidebar.selectbox("Produto", ["Notebook", "Celular", "Fone"])
quantidade = st.sidebar.number_input("Quantidade", step = 1)
valor =  st.sidebar.number_input("Valor")
botao_cadastrar = st.sidebar.button("Cadastrar Venda")

# Logica de Cadastro:
if botao_cadastrar:
    if valor  <= 0 or quantidade <= 0:
        st.warning("Não foi possível cadastrar a venda. Verifique o valor e a quantidade informados.")
    else:
        nova_venda = [str(data), vendedor, produto, quantidade, valor]
        ultima_linha = len(tabela_vendas) # len() -> fala o tamanho da tabela(121 linhas)
        tabela_vendas.loc[ultima_linha] = nova_venda # loc[] -> locaçiza
        tabela_vendas.to_csv("vendas.csv", index = False)
        st.success("Venda cadastrada com sucesso!")

# Seção de Visualizar Vendas
st.divider()
st.write("## Vendas Cadastradas")
st.dataframe(tabela_vendas) 

# Seção de Dashboard
st.divider()
st.write("## Dashboard")

# Card/Métrica -> Faturamento Total:
faturamento = tabela_vendas["valor"].sum() # .sum() -> soma todos o valores da tabela

# Produto mais vendido:
produto_mais_vendido = tabela_vendas["produto"].value_counts().idxmax()
coluna1, coluna2 = st.columns(2)

# Colunas -> Faturamento Total e Produto mais Vendido:
with coluna1: st.metric("Faturamento Total:", f"R$ {faturamento}")
with coluna2: st.metric("Produto Mais Vendido:", produto_mais_vendido)

cores_produtos = { # deixando as cores  pre-definidas nos gráficos
    "Notebook": "#3B82F6",
    "Celular": "#10B981",
    "Fone": "#F59E0B"
}

# Gráfico de Barra/Coluna -> Venda por vendedor:
st.divider()
st.write("#### Venda por vendedor:")
grafico1 = px.bar(tabela_vendas, x  = "vendedor", y = "valor", color = "produto", color_discrete_map=cores_produtos) # color_discrete_map -> pre-define a cor
st.plotly_chart(grafico1)

# Grafico de Pizza -> Venda por produto:
st.divider()
st.write("#### Venda por produto:")
grafico2 = px.pie(tabela_vendas, names = "produto", values = "valor", color = "produto", color_discrete_map=cores_produtos) # color_discrete_map -> pre-define a cor
st.plotly_chart(grafico2)

# Gráfico de Barra -> Quantidade vendida por produto:
st.divider()
st.write("#### Quantidade vendida por produto:")
quantidade_por_produto = tabela_vendas.groupby("produto", as_index=False)["quantidade"].sum()
grafico3 = px.bar(quantidade_por_produto, x="produto", y="quantidade", color="produto", color_discrete_map=cores_produtos) # color_discrete_map -> pre-define a cor
st.plotly_chart(grafico3)