import streamlit as st
import pandas as pd
from connection_mongo import vagas
from bson import ObjectId

# ----------------------------
# Botão voltar para a home
# ----------------------------
if st.button("⬅️ Voltar para a Home"):
    st.switch_page("app.py")


st.title("💼 Lista de Vagas (MongoDB)")

# ---------------------------
# LISTA AS VAGAS DO BANCO
# ---------------------------
try:
    documentos = list(vagas.find())
except Exception as e:
    st.error(f"Erro ao buscar vagas: {e}")
    st.stop()

if not documentos:
    st.info("Nenhuma vaga encontrada no banco.")
    st.stop()

# Criar DataFrame
df = pd.DataFrame(documentos)

# Mostrar tabela com o ID visível
df["_id"] = df["_id"].astype(str)
st.dataframe(df)

st.divider()

# ---------------------------
# ÁREA DE EXCLUSÃO
# ---------------------------

st.subheader("🗑️ Excluir Vaga")

opcoes = {
    f"{d['titulo']} - {d['empresa']} ({d['_id']})": d["_id"]
    for d in documentos
}

escolhida = st.selectbox(
    "Selecione a vaga que deseja excluir:",
    list(opcoes.keys())
)

if st.button("❌ Apagar vaga"):
    try:
        vagas.delete_one({"_id": ObjectId(opcoes[escolhida])})
        st.success("Vaga apagada com sucesso! 💥")
        st.rerun()  # recarrega página atualizando a tabela
    except Exception as e:
        st.error(f"Erro ao apagar vaga: {e}")
