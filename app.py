import streamlit as st
from connection_mongo import vagas, curriculos

st.set_page_config(page_title="Sistema de Vagas", layout="wide")

# ======= LOGIN DO ADMINISTRADOR =======
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =============== LISTAR VAGAS (VISÍVEL SEM LOGIN) ===============
def mostrar_home():
    st.title("💼 Vagas Disponíveis")

    lista_vagas = list(vagas.find())

    if not lista_vagas:
        st.info("Nenhuma vaga cadastrada ainda.")
        return

    for vaga in lista_vagas:
        with st.container(border=True):
            st.subheader(vaga.get("titulo", "Sem título"))
            st.write(f"**Descricao:** {vaga.get('descricao', 'Não informado')}")
            st.write(f"**Salário:** {vaga.get('salario', 'Não informado')}")
            st.write(f"**Empresa:** {vaga.get('empresa', 'Não informado')}")
            st.write(f"**Cidade:** {vaga.get('cidade', 'Não informado' )} - {vaga.get('estado', 'Não informado' )}")


# =============== TELA DO ADMINISTRADOR ===============
def tela_admin():
    st.title("👋 Bem-vindo, Administrador")

    st.subheader("Menu de Navegação")

    opcao = st.selectbox(
        "Escolha uma funcionalidade:",
        [
            "Início",
            "Cadastrar Vaga",
            "Listar Vagas",
            "Cadastrar Currículo",
            "Listar Currículos",
            "Recomendar Currículos por Vaga",
            "Localização das Vagas",
        ]
    )

    if opcao == "Cadastrar Vaga":
        st.switch_page("pages/cadastro_vaga.py")

    elif opcao == "Listar Vagas":
        st.switch_page("pages/listar_vagas.py")

    elif opcao == "Cadastrar Currículo":
        st.switch_page("pages/cadastro_curriculo.py")

    elif opcao == "Listar Currículos":
        st.switch_page("pages/listar_curriculos.py")

    elif opcao == "Recomendar Currículos por Vaga":
        st.switch_page("pages/recomendacao.py")

    elif opcao == "Localização das Vagas":
        st.switch_page("pages/localiza_cidades.py")  
        
    else:
        st.info("Selecione uma opção no menu para continuar.")


# =============== LOGIN ===============
def mostrar_login():
    st.title("🔐 Login do Administrador")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def botao_voltar_home():
    if st.button("⬅️ Voltar para a Home"):
        st.session_state["menu"] = "🏠 Início"
        st.rerun()



# =============== CONTROLE DE TELA ===============
if st.session_state.logged_in:
    tela_admin()
else:
    mostrar_login()
    st.divider()
    mostrar_home()
