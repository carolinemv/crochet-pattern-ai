# 🧶 Crochet Pattern AI

Um agente conversacional inteligente que ajuda a criar patterns de crochê personalizados através de uma conversa natural.

## 🚀 Funcionalidades

- **Conversa Natural**: O agente faz perguntas específicas e relevantes para coletar informações
- **Perguntas Adaptativas**: As perguntas se adaptam baseado nas respostas do usuário
- **Geração de Patterns**: Cria patterns detalhados e personalizados
- **Interface Web**: Interface de chat simples e intuitiva
- **API RESTful**: Backend em Python com FastAPI

## 🛠️ Tecnologias

- **Backend**: Python + FastAPI
- **IA**: OpenAI GPT-4 + LangChain
- **Frontend**: HTML/CSS/JavaScript (interface simples)
- **Modelos**: Pydantic para validação de dados

## 📋 Pré-requisitos

- Python 3.8+
- Chave da API OpenAI
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone <seu-repositorio>
cd crochet-pattern-ai
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure a chave da OpenAI**:
```bash
# Copie o arquivo de exemplo
cp env_example.txt .env

# Edite o arquivo .env e adicione sua chave da OpenAI
OPENAI_API_KEY=sua_chave_aqui
```

## 🚀 Como Executar

1. **Inicie o servidor**:
```bash
python main.py
```

2. **Acesse a aplicação**:
Abra seu navegador em `http://localhost:8000`

## 💬 Como Usar

1. **Inicie uma conversa**: O agente vai te cumprimentar e perguntar que tipo de peça você quer fazer
2. **Responda as perguntas**: O agente fará perguntas específicas sobre:
   - Tipo de peça (colete, blusa, chapeu, etc.)
   - Tamanho
   - Cor
   - Tipo de fio
   - Detalhes específicos (manga, decote, etc.)
3. **Receba seu pattern**: Quando tiver todas as informações, o agente gerará um pattern personalizado

## 🎯 Exemplo de Conversa

```
Agente: Olá! Que prazer te ajudar a criar um pattern de crochê personalizado! Que tipo de peça você gostaria de fazer hoje?

Usuário: Quero fazer um colete

Agente: Perfeito! Um colete. Qual tamanho você precisa? (XS, S, M, L, XL, XXL ou tem alguma medida específica?)

Usuário: M

Agente: Que cor você gostaria? Pode me dizer sua cor preferida ou se tem alguma paleta específica em mente?

Usuário: Azul

Agente: Que tipo de fio você prefere trabalhar? E qual peso? (Por exemplo: algodão fino, lã média, acrílico grosso, etc.)

Usuário: Algodão médio

Agente: Que tipo de detalhes você gostaria? Por exemplo: tipo de manga (bufante, justa, sem manga), decote, comprimento, etc.

Usuário: Sem manga, decote em V

Agente: Perfeito! Tenho todas as informações que preciso. Vou gerar seu pattern personalizado agora!
```

## 📁 Estrutura do Projeto

```
crochet-pattern-ai/
├── main.py                 # API FastAPI principal
├── crochet_agent.py       # Agente conversacional
├── models.py              # Modelos de dados (Pydantic)
├── requirements.txt       # Dependências Python
├── env_example.txt        # Exemplo de variáveis de ambiente
└── README.md             # Este arquivo
```

## 🔌 API Endpoints

- `GET /` - Interface web de chat
- `POST /chat` - Enviar mensagem para o agente
- `GET /conversations/{id}` - Obter histórico de uma conversa
- `GET /health` - Verificar saúde da API

## 🎨 Personalização

O agente pode ser facilmente personalizado editando:

- **Perguntas**: Modifique os templates em `crochet_agent.py`
- **Tipos de peças**: Adicione novos tipos em `models.py`
- **Interface**: Customize o HTML/CSS em `main.py`

## 🚧 Próximos Passos

- [ ] Integração com banco de dados
- [ ] Geração de imagens dos patterns
- [ ] Sistema de tradução
- [ ] Base de conhecimento de técnicas
- [ ] Múltiplos agentes especializados

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Enviar pull requests
4. Melhorar a documentação

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

Feito com ❤️ para a comunidade de crochê!
