import streamlit as st
import google.generativeai as genai
import os


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')
SYSTEM_PROMPT = (
    "Você é um assistente útil, educado e responde em português e só sabe de matemática. "
    "Seja claro e objetivo. Se não souber a resposta, admita."
)

def build_prompt(history, user_message):
    parts = [SYSTEM_PROMPT]
    for role, text in history:
        if role == "user":
            parts.append(f"Usuário: {text}")
        else:
            parts.append(f"Assistente: {text}")
    parts.append(f"Usuário: {user_message}")
    return "\n".join(parts)

# --- AQUI COMEÇA A INTERFACE STREAMLIT ---

st.title("Chatbot Gemini de Matemática")
st.markdown("Bem-vindo! Digite suas perguntas sobre matemática abaixo.")

# Inicializa o histórico do chat na sessão do Streamlitim
# Usamos st.session_state para manter o histórico entre as interações
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Pergunte-me algo..."):
    # Adiciona a mensagem do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # O seu prompt original é construído aqui
                full_prompt = build_prompt(st.session_state.messages, prompt)
                response = model.generate_content(contents=full_prompt)

                # Exibe a resposta
                st.markdown(response.text)

                # Adiciona a resposta da IA ao histórico
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na chamada à API: {e}")