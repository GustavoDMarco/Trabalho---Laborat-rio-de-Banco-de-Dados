import streamlit as st
from connection_mongo import vagas, curriculos
from pymongo import TEXT

# ===============================
# CRIAÇÃO DOS ÍNDICES DE TEXTO
# ===============================
# Só cria se ainda não existir
try:
    vagas.create_index([("titulo", TEXT), ("descricao", TEXT), ("requisitos", TEXT)])
    curriculos.create_index([("nome", TEXT), ("experiencia", TEXT),
                             ("formacao", TEXT), ("resumo", TEXT),
                             ("idiomas", TEXT), ("habilidades", TEXT)])
except:
    pass

# ===============================
# BOTÃO VOLTAR
# ===============================
def voltar_home():
    if st.button("⬅️ Voltar para a Home"):
        st.switch_page("app.py")

# ===============================
# PÁGINA DE RECOMENDAÇÃO
# ===============================
def mostrar_recomendacao():

    st.title("🔍 Recomendação Automática de Candidatos para Vagas")
    voltar_home()

    st.write("Selecione uma vaga para visualizar os melhores currículos:")

    # Buscar vagas
    lista_vagas = list(vagas.find({}))

    if not lista_vagas:
        st.warning("Nenhuma vaga cadastrada.")
        return

    # Mostrar apenas o título
    vaga_titulos = {vaga["titulo"]: vaga for vaga in lista_vagas}

    titulo_selecionado = st.selectbox("Escolha a vaga:", vaga_titulos.keys())

    if not titulo_selecionado:
        return

    vaga_escolhida = vaga_titulos[titulo_selecionado]

    st.subheader(f"📌 Vaga selecionada: **{vaga_escolhida['titulo']}**")

    # ======================================================
    # FULL TEXT SEARCH NO MONGO
    # ======================================================

    texto_busca = f"{vaga_escolhida.get('descricao', '')} {vaga_escolhida.get('requisitos', '')} {vaga_escolhida.get('skills', '')}"

    resultados = list(curriculos.aggregate([
        {
            "$match": {
                "$text": {"$search": texto_busca}
            }
        },
        {
            "$addFields": {
                "score": {"$meta": "textScore"}
            }
        },
        {
            "$sort": {"score": -1}
        }
    ]))

    st.write("---")
    st.subheader("👤 Melhores candidatos")

    if not resultados:
        st.info("Nenhum candidato com match para esta vaga.")
        return

    # Exibir resultado
    for c in resultados:
        st.markdown(f"""
        ### {c.get('nome', 'Sem nome')}
        **Score:** {round(c.get('score', 0), 4)}

        **Experiência:** {c.get('experiencia', 'Não informado')}
        
        **Formação:** {c.get('formacao', 'Não informado')}

        **Idiomas:** {c.get('idiomas', 'Não informado')}
        """)


# ===============================
# EXECUÇÃO
# ===============================
mostrar_recomendacao()
