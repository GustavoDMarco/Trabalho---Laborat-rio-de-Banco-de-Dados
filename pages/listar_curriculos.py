import streamlit as st
import pandas as pd
from connection_mongo import curriculos
from bson import ObjectId

# ----------------------------
# Botão voltar para a home
# ----------------------------
if st.button("⬅️ Voltar para a Home"):
    st.switch_page("app.py")


st.title("📄 Lista de Currículos (MongoDB)")

# ---------------------------
# LISTA OS CURRÍCULOS DO BANCO
# ---------------------------
try:
    documentos = list(curriculos.find())
except Exception as e:
    st.error(f"Erro ao buscar currículos: {e}")
    st.stop()

if not documentos:
    st.info("Nenhum currículo encontrado no banco.")
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

st.subheader("🗑️ Excluir Currículo")

opcoes = {
    f"{d['nome']} - {d['email']} ({d['_id']})": d["_id"]
    for d in documentos
}

escolhido = st.selectbox(
    "Selecione o currículo que deseja excluir:",
    list(opcoes.keys())
)

if st.button("❌ Apagar currículo"):
    try:
        curriculos.delete_one({"_id": ObjectId(opcoes[escolhido])})
        st.success("Currículo apagado com sucesso! 💥")
        st.rerun()  # recarrega página atualizando a tabela
    except Exception as e:
        st.error(f"Erro ao apagar currículo: {e}")

