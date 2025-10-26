# [file name]: src/models/tecnologia.py
# [file content begin]
from enum import Enum

class TipoTecnologia(Enum):
    ENERGIA = "Energia Limpa"
    TRANSPORTE = "Transporte Sustentável"
    AGRICULTURA = "Agricultura Sustentável"
    CONSTRUCAO = "Construção Verde"
    TECNOLOGIA = "Tecnologia Avançada"

class Tecnologia:
    def __init__(self, nome, tipo, custo, tempo_pesquisa, requisitos=None, beneficios=None):
        self.nome = nome
        self.tipo = tipo
        self.custo = custo
        self.tempo_pesquisa = tempo_pesquisa  # em ciclos
        self.tempo_restante = tempo_pesquisa
        self.pesquisando = False
        self.desbloqueada = False
        self.requisitos = requisitos or []
        self.beneficios = beneficios or {}
        
    def iniciar_pesquisa(self, cidade):
        """Inicia a pesquisa desta tecnologia"""
        if self.desbloqueada:
            return False, "Tecnologia já desbloqueada"
        
        if self.pesquisando:
            return False, "Tecnologia já em pesquisa"
        
        # Verificar requisitos
        for req in self.requisitos:
            if req not in [t.nome for t in cidade.tecnologias_desbloqueadas]:
                return False, f"Requisito não atendido: {req}"
        
        # Verificar recursos
        if cidade.recursos.dinheiro < self.custo:
            return False, "Recursos insuficientes"
        
        # Deduzir custo e iniciar pesquisa
        cidade.recursos.dinheiro -= self.custo
        self.pesquisando = True
        self.tempo_restante = self.tempo_pesquisa
        
        return True, f"Pesquisa de {self.nome} iniciada!"
    
    def atualizar_pesquisa(self):
        """Atualiza o progresso da pesquisa"""
        if self.pesquisando and not self.desbloqueada:
            self.tempo_restante -= 1
            if self.tempo_restante <= 0:
                self.pesquisando = False
                self.desbloqueada = True
                return True  # Pesquisa concluída
        return False
    
    def get_progresso(self):
        """Retorna o progresso da pesquisa em porcentagem"""
        if self.desbloqueada:
            return 100
        if not self.pesquisando:
            return 0
        return ((self.tempo_pesquisa - self.tempo_restante) / self.tempo_pesquisa) * 100
    
    def aplicar_beneficios(self, cidade):
        """Aplica os benefícios da tecnologia à cidade"""
        if not self.desbloqueada:
            return
        
        for recurso, valor in self.beneficios.items():
            if recurso == 'eficiencia_energia':
                # Aumenta eficiência de construções de energia
                pass
            elif recurso == 'reducao_emissao':
                cidade.recursos.emissao_carbono += valor
            elif recurso == 'bonus_satisfacao':
                cidade.recursos.satisfacao_populacional += valor
    
    def get_info(self):
        """Retorna informações da tecnologia para display"""
        return {
            'nome': self.nome,
            'tipo': self.tipo.value,
            'custo': self.custo,
            'tempo_pesquisa': self.tempo_pesquisa,
            'desbloqueada': self.desbloqueada,
            'pesquisando': self.pesquisando,
            'progresso': self.get_progresso(),
            'requisitos': self.requisitos,
            'beneficios': self.beneficios
        }

# Tecnologias disponíveis no jogo
TECNOLOGIAS_DISPONIVEIS = [
    Tecnologia(
        "Energia Solar Avançada",
        TipoTecnologia.ENERGIA,
        800,
        10,
        beneficios={'reducao_emissao': -10, 'bonus_satisfacao': 5}
    ),
    Tecnologia(
        "Veículos Elétricos",
        TipoTecnologia.TRANSPORTE,
        1200,
        15,
        requisitos=["Energia Solar Avançada"],
        beneficios={'reducao_emissao': -15}
    ),
    Tecnologia(
        "Agricultura Vertical",
        TipoTecnologia.AGRICULTURA,
        600,
        8,
        beneficios={'bonus_satisfacao': 8}
    ),
    Tecnologia(
        "Materiais Sustentáveis",
        TipoTecnologia.CONSTRUCAO,
        900,
        12,
        beneficios={'reducao_emissao': -8, 'bonus_satisfacao': 3}
    ),
    Tecnologia(
        "Smart Grid",
        TipoTecnologia.TECNOLOGIA,
        1500,
        20,
        requisitos=["Energia Solar Avançada", "Materiais Sustentáveis"],
        beneficios={'reducao_emissao': -20, 'bonus_satisfacao': 10}
    ),
    Tecnologia(
        "Captura de Carbono",
        TipoTecnologia.TECNOLOGIA,
        2000,
        25,
        requisitos=["Smart Grid"],
        beneficios={'reducao_emissao': -30}
    )
]
# [file content end]