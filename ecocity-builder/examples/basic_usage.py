"""
Exemplo básico de uso das classes do EcoCity Builder
"""

from src.models.base import Recurso

def demonstrar_recursos():
    """Demonstra o funcionamento básico do sistema de recursos"""
    print("=== Demonstração EcoCity Builder ===\n")
    
    # Criar recursos iniciais
    recursos = Recurso(dinheiro=1500, emissao_carbono=45.5, satisfacao=80)
    print("Recursos iniciais:")
    print(recursos)
    print()
    
    # Simular algumas ações
    print("Ações do jogador:")
    
    # Construir usina solar (custo: 500)
    if recursos.verificar_recursos_suficientes(500):
        recursos.dinheiro -= 500
        recursos.emissao_carbono -= 10.0
        recursos.satisfacao_populacional += 5
        print("✅ Usina Solar construída! (-10 CO₂, +5% satisfação)")
    
    print(recursos)
    print()
    
    # Evento climático
    print("🌪️  Evento climático: Tempestade!")
    recursos.dinheiro -= 100
    recursos.satisfacao_populacional -= 8
    print(recursos)

if __name__ == "__main__":
    demonstrar_recursos()