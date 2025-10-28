# RFC: Crochet Pattern Generator with AI

## 1. Summary
Brief description of the project:  
Create an MVP of a website that allows users to generate personalized crochet patterns through a guided conversational agent, with future possibilities for translation, visualizations, and a knowledge base.

## 2. Motivation
- Enable creation of personalized crochet patterns easily.  
- Experiment with integration of multiple AI agents.  
- Create a documented and scalable foundation for product evolution.

## 3. MVP Goals
- Conversational agent to collect user requirements.  
- Generation of basic crochet patterns in text format.  
- Clear data structure (JSON) for patterns.  
- Initial frontend integration (chat interface and pattern download).

## 4. Scope
- Text and JSON outputs only in MVP.  
- No visualizations, translations, or knowledge base integration at this stage.  
- Future versions may include additional agents and features.

## 5. Proposed Architecture
- **Frontend:** React + Tailwind or Lovable  
- **Backend / Orchestrator:** FastAPI + LangChain  
- **Conversational Agent:** GPT-4.1-turbo  
- **Technical Agent:** Text-based pattern generation  
- **Storage:** Supabase / PostgreSQL

```mermaid
graph TD
A[User] -->|Chat| B(Conversational Agent)
B -->|JSON parameters| C(Technical Agent)
C -->|Pattern text| H[Frontend]
