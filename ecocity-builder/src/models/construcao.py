# [file name]: src/models/construcao.py
# [file content begin]
from enum import Enum

class TipoConstrucao(Enum):
    ENERGIA = "Energia Limpa"
    TRANSPORTE = "Transporte Sustentável"
    AMBIENTAL = "Proteção Ambiental"
    SOCIAL = "Infraestrutura Social"

class Construcao:
    def __init__(self, nome, tipo, custo, impacto_emissao, impacto_satisfacao, requisitos=None):
        self.nome = nome
        self.tipo = tipo
        self.custo = custo
        self.impacto_emissao = impacto_emissao  # Negativo = reduz emissão
        self.impacto_satisfacao = impacto_satisfacao  # Positivo = aumenta satisfação
        self.nivel = 1
        self.requisitos = requisitos or []
        
    def pode_construir(self, recursos, tecnologias_desbloqueadas=[]):
        """Verifica se pode construir baseado em recursos e tecnologias"""
        if not recursos.verificar_recursos_suficientes(self.custo):
            return False, "Recursos insuficientes"
            
        for req in self.requisitos:
            if req not in tecnologias_desbloqueadas:
                return False, f"Tecnologia {req} necessária"
                
        return True, "Pode construir"
        
    def melhorar(self):
        """Melhora a construção para o próximo nível"""
        if self.nivel < 3:  # Máximo 3 níveis
            self.nivel += 1
            self.custo = int(self.custo * 1.5)
            self.impacto_emissao *= 1.3  # 30% mais eficiente
            self.impacto_satisfacao *= 1.2  # 20% mais satisfação
            return True
        return False
        
    def get_beneficios(self):
        return {
            'nome': self.nome,
            'tipo': self.tipo.value,
            'custo': self.custo,
            'impacto_emissao': self.impacto_emissao,
            'impacto_satisfacao': self.impacto_satisfacao,
            'nivel': self.nivel
        }
        
    def __str__(self):
        emissao_str = f"+{self.impacto_emissao}" if self.impacto_emissao >= 0 else f"{self.impacto_emissao}"
        return f"{self.nome} (Nv.{self.nivel}) | ${self.custo} | {emissao_str}CO₂ | +{self.impacto_satisfacao}% satisfação"

# Construções predefinidas
CONSTRUCOES_DISPONIVEIS = [
    Construcao("Painel Solar", TipoConstrucao.ENERGIA, 300, -8, 2),
    Construcao("Parque Eólico", TipoConstrucao.ENERGIA, 500, -12, 3),
    Construcao("Usina Reciclagem", TipoConstrucao.AMBIENTAL, 400, -6, 5),
    Construcao("Parque Público", TipoConstrucao.SOCIAL, 200, -3, 8),
    Construcao("Ciclovia", TipoConstrucao.TRANSPORTE, 150, -4, 4),
    Construcao("Transporte Elétrico", TipoConstrucao.TRANSPORTE, 600, -15, 6, ["Eletrificação"]),
]
# [file content end]