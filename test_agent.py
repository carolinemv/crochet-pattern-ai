#!/usr/bin/env python3
"""
Script de teste para o agente conversacional de crochê
Execute este script para testar o agente sem interface web
"""

import os
from dotenv import load_dotenv
from crochet_agent import CrochetConversationalAgent

def test_conversation():
    """Testa uma conversa completa com o agente"""
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Erro: Chave da OpenAI não encontrada!")
        print("Configure a variável OPENAI_API_KEY no arquivo .env")
        return
    
    # Inicializa o agente
    print("🧶 Inicializando Agente de Crochê...")
    agent = CrochetConversationalAgent()
    
    # Cria um estado inicial
    state = agent._create_initial_state()
    
    print("\n" + "="*50)
    print("CONVERSA DE TESTE COM O AGENTE DE CROCHÊ")
    print("="*50)
    
    # Simula uma conversa
    test_messages = [
        "Olá! Quero fazer um colete",
        "Tamanho M",
        "Azul marinho",
        "Algodão médio",
        "Sem manga, decote em V, comprimento até a cintura"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n👤 Usuário: {message}")
        
        # Processa a mensagem
        response = agent.get_next_question(state, message)
        
        print(f"🤖 Agente: {response}")
        
        # Se chegou na geração do pattern, para aqui
        if state.current_step == "pattern_generation":
            print("\n" + "="*50)
            print("GERANDO PATTERN...")
            print("="*50)
            
            try:
                pattern = agent.generate_pattern(state)
                print(f"\n🧶 PATTERN GERADO:")
                print(f"Peça: {pattern.piece_type}")
                print(f"Tamanho: {pattern.size}")
                print(f"Cor: {pattern.color}")
                print(f"Peso do fio: {pattern.yarn_weight}")
                print(f"Tamanho do gancho: {pattern.hook_size}")
                print(f"Dificuldade: {pattern.difficulty_level}")
                print(f"Tempo estimado: {pattern.estimated_time}")
                print(f"\nMateriais necessários:")
                for material in pattern.materials:
                    print(f"  - {material}")
                print(f"\nInstruções:")
                for instruction in pattern.instructions[:5]:  # Mostra apenas as primeiras 5
                    print(f"  {instruction}")
                if len(pattern.instructions) > 5:
                    print(f"  ... e mais {len(pattern.instructions) - 5} instruções")
                    
            except Exception as e:
                print(f"❌ Erro ao gerar pattern: {e}")
            
            break
    
    print(f"\n📊 DADOS COLETADOS:")
    for key, value in state.collected_data.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ Teste concluído!")

def interactive_test():
    """Teste interativo - você pode conversar com o agente"""
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Erro: Chave da OpenAI não encontrada!")
        print("Configure a variável OPENAI_API_KEY no arquivo .env")
        return
    
    # Inicializa o agente
    print("🧶 Agente de Crochê - Modo Interativo")
    print("Digite 'sair' para encerrar")
    print("-" * 40)
    
    agent = CrochetConversationalAgent()
    state = agent._create_initial_state()
    
    # Mensagem inicial
    response = agent.get_next_question(state, "")
    print(f"🤖 Agente: {response}")
    
    while True:
        try:
            user_input = input("\n👤 Você: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("👋 Até logo!")
                break
            
            if not user_input:
                continue
            
            # Processa a mensagem
            response = agent.get_next_question(state, user_input)
            print(f"🤖 Agente: {response}")
            
            # Se chegou na geração do pattern
            if state.current_step == "pattern_generation":
                print("\n🎉 Gerando seu pattern personalizado...")
                try:
                    pattern = agent.generate_pattern(state)
                    print(f"\n🧶 SEU PATTERN:")
                    print(f"Peça: {pattern.piece_type}")
                    print(f"Tamanho: {pattern.size}")
                    print(f"Cor: {pattern.color}")
                    print(f"Dificuldade: {pattern.difficulty_level}")
                    print(f"Tempo estimado: {pattern.estimated_time}")
                    print("\nInstruções completas foram geradas!")
                except Exception as e:
                    print(f"❌ Erro: {e}")
                break
                
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        test_conversation()
