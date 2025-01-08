import streamlit as st
import requests

# Título e descrição
st.title("💬 PostgreSQL + OpenAI Chatbot")
st.write(
    "Este é um agente que utiliza OpenAI e PostgreSQL para interagir com bancos de dados. "
    "Forneça a chave da OpenAI e as credenciais do banco de dados para começar."
)

# Coleta das credenciais do usuário
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
db_host = st.text_input("🗄️ Database Host")
db_name = st.text_input("📂 Database Name")
db_user = st.text_input("👤 Database User")
db_password = st.text_input("🔒 Database Password", type="password")
db_port = st.text_input("🌐 Database Port (default: 5432)", value="5432")

# Checa se todas as credenciais foram preenchidas
if not openai_api_key or not db_host or not db_name or not db_user or not db_password:
    st.info("Insira todas as credenciais para continuar.", icon="ℹ️")
else:
    # Inicializa o chat somente após as credenciais serem fornecidas
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens existentes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input de mensagem do usuário
    if user_input := st.chat_input("Digite sua mensagem aqui..."):
        # Armazena e exibe a mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Faz a requisição para o backend (FastAPI)
        payload = {
            "input": user_input,
            "db_credentials": {
                "host": db_host,
                "database": db_name,
                "user": db_user,
                "password": db_password,
                "port": db_port
            }
        }
        # Manda a chave no cabeçalho "Authorization: Bearer <chave>"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        response = requests.post("http://127.0.0.1:8000/query", json=payload, headers=headers)

        # Verifica a resposta
        if response.status_code == 200:
            assistant_response = response.json().get("response", "Sem resposta.")
        else:
            assistant_response = f"Erro: {response.status_code} - {response.text}"

        # Armazena e exibe a resposta do assistente
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
