from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from typing import Dict
import uuid
from datetime import datetime

from models import ChatMessage, PatternRequest, CrochetPattern
from crochet_agent import CrochetConversationalAgent

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI(title="Crochet Pattern AI", version="1.0.0")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o agente conversacional
agent = CrochetConversationalAgent()

# Armazena conversas ativas (em produção, use um banco de dados)
conversations: Dict[str, Dict] = {}

@app.get("/")
async def root():
    """Página inicial com interface de chat"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crochet Pattern AI</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .chat-container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                height: 500px;
                display: flex;
                flex-direction: column;
            }
            .chat-header {
                background: #6B73FF;
                color: white;
                padding: 20px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .message {
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 70%;
                word-wrap: break-word;
            }
            .user-message {
                background: #6B73FF;
                color: white;
                align-self: flex-end;
            }
            .assistant-message {
                background: #f0f0f0;
                color: #333;
                align-self: flex-start;
            }
            .chat-input {
                display: flex;
                padding: 20px;
                border-top: 1px solid #eee;
            }
            .chat-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 20px;
                outline: none;
            }
            .chat-input button {
                margin-left: 10px;
                padding: 10px 20px;
                background: #6B73FF;
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
            }
            .chat-input button:hover {
                background: #5a63e6;
            }
            .pattern-display {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 15px;
                margin: 10px 0;
                white-space: pre-wrap;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🧶 Crochet Pattern AI</h1>
                <p>Converse comigo para criar seu pattern personalizado!</p>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message assistant-message">
                    Olá! Que prazer te ajudar a criar um pattern de crochê personalizado! Que tipo de peça você gostaria de fazer hoje?
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="messageInput" placeholder="Digite sua mensagem..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Enviar</button>
            </div>
        </div>

        <script>
            let conversationId = null;

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;

                // Adiciona mensagem do usuário
                addMessage(message, 'user');
                input.value = '';

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            conversation_id: conversationId
                        })
                    });

                    const data = await response.json();
                    
                    if (data.conversation_id) {
                        conversationId = data.conversation_id;
                    }

                    // Adiciona resposta do assistente
                    addMessage(data.response, 'assistant');

                    // Se for um pattern, exibe de forma especial
                    if (data.pattern) {
                        displayPattern(data.pattern);
                    }

                } catch (error) {
                    console.error('Erro:', error);
                    addMessage('Desculpe, ocorreu um erro. Tente novamente.', 'assistant');
                }
            }

            function addMessage(content, sender) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = content;
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }

            function displayPattern(pattern) {
                const messagesContainer = document.getElementById('chatMessages');
                const patternDiv = document.createElement('div');
                patternDiv.className = 'pattern-display';
                patternDiv.innerHTML = `
                    <h3>🧶 Seu Pattern de Crochê</h3>
                    <p><strong>Peça:</strong> ${pattern.piece_type}</p>
                    <p><strong>Tamanho:</strong> ${pattern.size}</p>
                    <p><strong>Cor:</strong> ${pattern.color}</p>
                    <p><strong>Dificuldade:</strong> ${pattern.difficulty_level}</p>
                    <p><strong>Tempo estimado:</strong> ${pattern.estimated_time}</p>
                    <h4>Instruções:</h4>
                    <div>${pattern.instructions.join('<br>')}</div>
                `;
                messagesContainer.appendChild(patternDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """)

@app.post("/chat")
async def chat(request: PatternRequest):
    """Endpoint principal para conversar com o agente"""
    try:
        # Se não há conversation_id, cria uma nova conversa
        if not request.conversation_id:
            conversation_id = str(uuid.uuid4())
            conversations[conversation_id] = {
                "state": agent._create_initial_state(),
                "created_at": datetime.now()
            }
        else:
            conversation_id = request.conversation_id
            if conversation_id not in conversations:
                raise HTTPException(status_code=404, detail="Conversa não encontrada")
        
        # Obtém o estado da conversa
        state = conversations[conversation_id]["state"]
        
        # Processa a mensagem do usuário
        response = agent.get_next_question(state, request.message)
        
        # Verifica se deve gerar o pattern
        pattern = None
        if state.current_step == "pattern_generation":
            pattern = agent.generate_pattern(state)
            # Converte para dict para serialização JSON
            pattern = pattern.dict()
        
        return {
            "response": response,
            "conversation_id": conversation_id,
            "current_step": state.current_step,
            "collected_data": state.collected_data,
            "pattern": pattern
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Obtém o histórico de uma conversa específica"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    return {
        "conversation_id": conversation_id,
        "history": conversations[conversation_id]["state"].conversation_history,
        "collected_data": conversations[conversation_id]["state"].collected_data,
        "created_at": conversations[conversation_id]["created_at"]
    }

@app.get("/health")
async def health_check():
    """Endpoint de saúde da API"""
    return {"status": "healthy", "message": "Crochet Pattern AI está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
