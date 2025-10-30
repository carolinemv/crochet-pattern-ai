import os
from typing import Dict, List, Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from models import ConversationState, CrochetPattern, PieceType, Size

class CrochetConversationalAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Estados possíveis da conversa
        self.conversation_states = {
            "greeting": "Cumprimentar e perguntar que tipo de peça quer fazer",
            "piece_type": "Identificar o tipo de peça (colete, blusa, etc.)",
            "size": "Perguntar sobre o tamanho",
            "color": "Perguntar sobre a cor",
            "yarn_preferences": "Perguntar sobre preferências de fio",
            "style_details": "Perguntar detalhes específicos (manga, decote, etc.)",
            "pattern_generation": "Gerar o pattern final"
        }
        
        # Template do sistema para o agente
        self.system_prompt = """
        Você é um assistente especializado em crochê que ajuda pessoas a criar patterns personalizados.
        
        Sua missão é fazer perguntas específicas e relevantes para coletar informações necessárias
        para gerar um pattern de crochê personalizado.
        
        IMPORTANTE:
        - Seja conversacional e amigável
        - Faça uma pergunta por vez
        - Adapte suas perguntas baseado no que a pessoa já respondeu
        - Se a pessoa mencionar detalhes específicos (como "manga bufante"), pergunte sobre eles
        - Mantenha o foco em crochê e seja específico sobre técnicas e materiais
        
        Informações que você precisa coletar:
        1. Tipo de peça (colete, blusa, chapeu, etc.)
        2. Tamanho (XS, S, M, L, XL, XXL ou medidas personalizadas)
        3. Cor preferida
        4. Tipo de fio (algodão, lã, acrílico, etc.)
        5. Peso do fio (fino, médio, grosso)
        6. Detalhes específicos da peça (tipo de manga, decote, comprimento, etc.)
        7. Nível de dificuldade desejado
        8. Tempo estimado disponível
        
        Quando tiver todas as informações necessárias, informe que vai gerar o pattern.
        O foco da conversa é somente crochê, caso o usuário fale sobre outros assuntos, retorne que você é um assistente de crochê e que o foco da conversa é somente crochê.
        """
    
    def get_next_question(self, state: ConversationState, user_message: str) -> str:
        """Determina a próxima pergunta baseada no estado atual e na mensagem do usuário"""
        
        # Atualiza o histórico da conversa
        state.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Extrai informações da mensagem do usuário
        self._extract_information(state, user_message)
        
        # Determina o próximo passo
        next_step = self._determine_next_step(state)
        
        # Gera a pergunta apropriada
        question = self._generate_question(state, next_step)
        
        # Atualiza o estado
        state.current_step = next_step
        state.conversation_history.append({
            "role": "assistant", 
            "content": question
        })
        
        return question
    
    def _extract_information(self, state: ConversationState, message: str):
        """Extrai informações relevantes da mensagem do usuário"""
        message_lower = message.lower()
        
        # Identifica tipo de peça
        piece_types = {
            "colete": "colete", "blusa": "blusa", "chapeu": "chapeu", 
            "cachecol": "cachecol", "luvas": "luvas", "meias": "meias",
            "cobertor": "cobertor", "bolsa": "bolsa"
        }
        
        for keyword, piece_type in piece_types.items():
            if keyword in message_lower:
                state.collected_data["piece_type"] = piece_type
                break
        
        # Identifica tamanho
        sizes = ["xs", "s", "m", "l", "xl", "xxl", "pequeno", "médio", "grande"]
        for size in sizes:
            if size in message_lower:
                state.collected_data["size"] = size.upper() if size in ["xs", "s", "m", "l", "xl", "xxl"] else size
                break
        
        # Identifica cor
        colors = ["azul", "vermelho", "verde", "amarelo", "preto", "branco", "rosa", "roxo", "cinza", "marrom"]
        for color in colors:
            if color in message_lower:
                state.collected_data["color"] = color
                break
        
        # Identifica detalhes específicos
        if "manga" in message_lower:
            if "bufante" in message_lower or "bufê" in message_lower:
                state.collected_data["sleeve_type"] = "bufante"
            elif "justa" in message_lower:
                state.collected_data["sleeve_type"] = "justa"
            elif "sem manga" in message_lower:
                state.collected_data["sleeve_type"] = "sem manga"
    
    def _determine_next_step(self, state: ConversationState) -> str:
        """Determina qual deve ser o próximo passo da conversa"""
        
        data = state.collected_data
        
        if not data.get("piece_type"):
            return "piece_type"
        elif not data.get("size"):
            return "size"
        elif not data.get("color"):
            return "color"
        elif not data.get("yarn_type"):
            return "yarn_preferences"
        elif not data.get("yarn_weight"):
            return "yarn_preferences"
        elif not data.get("style_details"):
            return "style_details"
        else:
            return "pattern_generation"
    
    def _generate_question(self, state: ConversationState, step: str) -> str:
        """Gera a pergunta apropriada para cada passo"""
        
        data = state.collected_data
        
        if step == "greeting":
            return "Olá! Que prazer te ajudar a criar um pattern de crochê personalizado! Que tipo de peça você gostaria de fazer hoje?"
        
        elif step == "piece_type":
            return "Que tipo de peça você quer fazer? Pode ser um colete, blusa, chapeu, cachecol, luvas, meias, cobertor ou bolsa?"
        
        elif step == "size":
            piece = data.get("piece_type", "peça")
            return f"Perfeito! Um(a) {piece}. Qual tamanho você precisa? (XS, S, M, L, XL, XXL ou tem alguma medida específica?)"
        
        elif step == "color":
            return "Que cor você gostaria? Pode me dizer sua cor preferida ou se tem alguma paleta específica em mente?"
        
        elif step == "yarn_preferences":
            return "Que tipo de fio você prefere trabalhar? E qual peso? (Por exemplo: algodão fino, lã média, acrílico grosso, etc.)"
        
        elif step == "style_details":
            piece = data.get("piece_type", "")
            if piece in ["colete", "blusa"]:
                return "Que tipo de detalhes você gostaria? Por exemplo: tipo de manga (bufante, justa, sem manga), decote, comprimento, etc."
            else:
                return "Tem algum detalhe específico que você gostaria de incluir nesta peça?"
        
        elif step == "pattern_generation":
            return "Perfeito! Tenho todas as informações que preciso. Vou gerar seu pattern personalizado agora!"
        
        return "Como posso te ajudar com seu pattern de crochê?"
    
    def generate_pattern(self, state: ConversationState) -> CrochetPattern:
        """Gera o pattern de crochê baseado nas informações coletadas"""
        
        data = state.collected_data
        
        # Prompt para geração do pattern
        pattern_prompt = f"""
        Gere um pattern de crochê completo e detalhado baseado nas seguintes informações:
        
        Tipo de peça: {data.get('piece_type', 'não especificado')}
        Tamanho: {data.get('size', 'não especificado')}
        Cor: {data.get('color', 'não especificada')}
        Tipo de fio: {data.get('yarn_type', 'não especificado')}
        Peso do fio: {data.get('yarn_weight', 'não especificado')}
        Detalhes específicos: {data.get('style_details', 'não especificados')}
        
        O pattern deve incluir:
        1. Lista de materiais necessários
        2. Tamanho do gancho recomendado
        3. Medida da amostra (gauge)
        4. Instruções passo a passo detalhadas
        5. Pontos utilizados
        6. Nível de dificuldade
        7. Notas especiais
        
        Seja específico e técnico, mas mantenha as instruções claras para crocheteiros de nível intermediário.
        """
        
        messages = [
            SystemMessage(content="Você é um especialista em crochê que cria patterns detalhados e profissionais."),
            HumanMessage(content=pattern_prompt)
        ]
        
        response = self.llm(messages)
        pattern_text = response.content
        
        # Aqui você pode processar a resposta para extrair informações estruturadas
        # Por enquanto, vou retornar um pattern básico estruturado
        
        return CrochetPattern(
            piece_type=data.get('piece_type', ''),
            size=data.get('size', ''),
            color=data.get('color', ''),
            yarn_weight=data.get('yarn_weight', ''),
            hook_size="5.0mm",  # Seria extraído da resposta do LLM
            gauge="18 pontos x 20 carreiras = 10cm",
            materials=["Fio de algodão", "Gancho 5.0mm", "Tesoura", "Agulha de tapeçaria"],
            instructions=pattern_text.split('\n'),
            special_notes=["Ajuste o tamanho conforme necessário"],
            difficulty_level="Intermediário"
        )
    
    def _create_initial_state(self) -> ConversationState:
        """Cria um estado inicial para uma nova conversa"""
        return ConversationState(
            current_step="greeting",
            collected_data={},
            missing_information=[],
            conversation_history=[]
        )
