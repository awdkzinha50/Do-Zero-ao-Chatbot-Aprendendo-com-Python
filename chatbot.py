from google import genai # chamada da biblioteca google - importação da ferramenta genai 

client = genai.Client() # inicialização do cliente genai
MODEL = "gemini-2.5-flash"  # Definição do modelo Gemini 2.5-flash

SYSTEM_PROMPT = (
    "Você é um assistente útil, educado e responde em português e só sabe de matemática. " # inicialização do prompt do sistema (Chatbot responderá de acordo com as informações impressas no prompy)
    "Seja claro e objetivo. Se não souber a resposta, admita."
)

history = []   # Inicialização da lista de histórico de conversas
print("Chatbot Gemini (simples). Digite 'sair' para encerrar.\n") # Mensagem de inicialização do prompt do chatbot
while True: # Loop principal do chatbot
    user_input = input("Você: ").strip() # Captura de mensagem fornecida pelo usuário
    if not user_input: # Se a entrada do usuário estiver vazia, Continua:
        continue # Chamada de continuação do loop 
    if user_input.lower() in ("sair", "exit", "quit"): # opera a função saída do chatbot (LEVA EM CONSIDERAÇÃO SOMENTE A FRASE ESCRITA EM MINÚSCULO)
        print("Encerrando chatbot. Até mais!") # Mensagem de encerramento
        break # Comando de saída do loop

    parts = [SYSTEM_PROMPT, ""] # Construção do prompt completo com o histórico da conversa (Parte importante a ser implementada)
    for role, text in history: # Loop para adicionar mensagens anteriores ao prompt
        if role == "user": # Se a mensagem for do usuário, adiciona "Usuário:" antes do texto
            parts.append(f"Usuário: {text}") # Adiciona a mensagem do usuário ao prompt
        else: # Se a mensagem for do assistente, adiciona "Assistente:" antes do texto
            parts.append(f"Assistente: {text}") # Adiciona a mensagem do assistente ao prompt
    parts.append(f"Usuário: {user_input}") # Adiciona a mensagem atual do usuário ao prompt
    parts.append("Assistente:") # Adiciona o marcador para a resposta do assistente
    prompt = "\n".join(parts) # Junta todas as partes do prompt em uma única string

    try: # Chamada da API para gerar a resposta do modelo (Inicializar na variável de ambiente) (opcional)
        response = client.models.generate_content(  #resposta do modelo recebe a chamada da API
            model=MODEL, #modelo definido anteriormente
            contents=prompt #conteúdo do prompt construído anteriormente
        )
    except Exception as e: # Tratamento de exceção para erros na chamada da API
        print("Erro na chamada à API:", e) # Mensagem de erro
        break # Comando de saída do loop em caso de erro

    bot_text = response.text # Extrai o texto da resposta do modelo
    print("Bot:", bot_text, "\n") # Exibe a resposta do bot

    history.append(("user", user_input)) # Adiciona a mensagem do usuário ao histórico
    history.append(("assistant", bot_text)) # Adiciona a resposta do assistente ao histórico

    if len(history) > 12: # Limita o histórico para as últimas 12 mensagens (6 pares de perguntas e respostas)
        history = history[-12:] # Mantém apenas as últimas 12 mensagens no histórico