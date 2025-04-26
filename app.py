import streamlit as st
from main import executar_automacao

st.title("Automação de requerimentos de certificação no SIGA2")
st.write("Essa automação irá atender os requerimentos de certificação com base na situação financeira do cliente.")
st.write("Se o cliente tiver alguma inadimplência, o requerimento será colocado 'Em espera'.")
st.write("Caso o cliente não possuir inadimplência, a automação irá deferir o requerimento.")

st.divider()

st.markdown("### 1. Coloque seu usuário e senha do SIGA2")
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

st.write("")

st.markdown("### 2. Selecione os perfis que devem ser considerados na automação")

opcoes_perfis = st.multiselect(
    "Selecione no campo abaixo:",
    ["FGV SP - Faria Lima", "FGV SP - Paulista", "FGV SP - Berrini",
     "FGV RJ - Tijuca", "FGV RJ - Candelária",
     "FGV Campinas", "FGV BH"],
     placeholder="",
)

opcoes_selecionadas = opcoes_perfis

st.write("")

if st.button("Executar automação", icon="🚀"):
    with st.spinner("A automação está em execução..."):
        try:
            for perfil in opcoes_selecionadas:
                executar_automacao(usuario, senha, perfil)
            st.success("A automação foi executada com sucesso!")
        except Exception as e:
            st.error(f'Ocorreu um erro na execução: {e}')



