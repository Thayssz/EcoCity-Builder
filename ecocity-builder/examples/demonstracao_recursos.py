"""
Demonstração do sistema de recursos do EcoCity Builder
"""

import sys
import os
sys.path.append('src')

from models.base import Recurso

def demonstrar_sistema_recursos():
    print("🎮 ECOCITY BUILDER - Sistema de Recursos")
    print("=" * 50)
    
    # 1. Início do jogo
    print("\n1. 🏁 INÍCIO DO JOGO")
    recursos = Recurso(dinheiro=1500, emissao_carbono=60, satisfacao=75)
    print(f"   Estado inicial: {recursos}")
    
    # 2. Menu de construções
    print("\n2. 🏗️  MENU DE CONSTRUÇÕES")
    construcoes = [
        {"nome": "💡 Painel Solar", "custo": 300, "impacto": -8, "satisfacao": 2},
        {"nome": "🌬️ Parque Eólico", "custo": 500, "impacto": -12, "satisfacao": 3},
        {"nome": "♻️ Usina Reciclagem", "custo": 400, "impacto": -6, "satisfacao": 5},
        {"nome": "🌳 Parque Público", "custo": 200, "impacto": -3, "satisfacao": 8}
    ]
    
    for i, construcao in enumerate(construcoes, 1):
        pode_construir = recursos.verificar_recursos_suficientes(construcao["custo"])
        status = "✅ Disponível" if pode_construir else "❌ Recursos insuficientes"
        print(f"   {i}. {construcao['nome']}")
        print(f"      Custo: ${construcao['custo']} | Emissão: {construcao['impacto']}CO₂ | Satisfação: +{construcao['satisfacao']}%")
        print(f"      Status: {status}")
    
    # 3. Jogador constrói
    print("\n3. 🔨 AÇÃO DO JOGADOR")
    escolha = construcoes[0]  # Painel Solar
    if recursos.verificar_recursos_suficientes(escolha["custo"]):
        recursos.dinheiro -= escolha["custo"]
        recursos.emissao_carbono += escolha["impacto"]
        recursos.satisfacao_populacional += escolha["satisfacao"]
        print(f"   ✅ {escolha['nome']} construído com sucesso!")
        print(f"   📊 Novo estado: {recursos}")
    else:
        print(f"   ❌ Não foi possível construir {escolha['nome']}")
    
    # 4. Evento climático
    print("\n4. 🌪️  EVENTO CLIMÁTICO")
    print("   Tempestade severa atingiu a cidade!")
    recursos.dinheiro -= 150
    recursos.satisfacao_populacional -= 10
    print(f"   📊 Estado pós-evento: {recursos}")
    
    # 5. Verificação de recursos críticos
    print("\n5. 📈 ANÁLISE DE RECURSOS")
    if recursos.satisfacao_populacional < 60:
        print("   ⚠️  ALERTA: Satisfação populacional baixa!")
    if recursos.emissao_carbono > 70:
        print("   ⚠️  ALERTA: Emissões de carbono muito altas!")
    if recursos.dinheiro < 200:
        print("   ⚠️  ALERTA: Recursos financeiros críticos!")
    
    print(f"\n🎯 Estado final: {recursos}")
    print("\n✨ Demonstração concluída! O sistema de recursos está funcionando perfeitamente.")

if __name__ == "__main__":
    demonstrar_sistema_recursos()