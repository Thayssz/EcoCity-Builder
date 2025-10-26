# [file name]: src/models/cidade.py
# [file content begin]
from .base import Recurso
from .construcao import Construcao, CONSTRUCOES_DISPONIVEIS

class Cidade:
    def __init__(self, nome, dificuldade="Médio"):
        self.nome = nome
        self.dificuldade = dificuldade
        self.populacao = 100
        self.recursos = Recurso()
        self.construcoes = []
        self.tecnologias_desbloqueadas = []
        self.tempo_jogo = 0  # em ciclos
        
        # Ajusta recursos baseado na dificuldade
        self._ajustar_dificuldade()
        
    def _ajustar_dificuldade(self):
        """Ajusta recursos iniciais baseado na dificuldade"""
        if self.dificuldade == "Fácil":
            self.recursos.dinheiro = 1500
            self.recursos.satisfacao_populacional = 80
        elif self.dificuldade == "Difícil":
            self.recursos.dinheiro = 700
            self.recursos.emissao_carbono = 60
            self.recursos.satisfacao_populacional = 60
            
    def adicionar_construcao(self, construcao_nome):
        """Adiciona uma construção à cidade"""
        construcao = next((c for c in CONSTRUCOES_DISPONIVEIS if c.nome == construcao_nome), None)
        
        if not construcao:
            return False, "Construção não encontrada"
            
        pode_construir, mensagem = construcao.pode_construir(self.recursos, self.tecnologias_desbloqueadas)
        
        if pode_construir:
            # Cria uma cópia da construção
            nova_construcao = Construcao(
                construcao.nome, 
                construcao.tipo, 
                construcao.custo,
                construcao.impacto_emissao,
                construcao.impacto_satisfacao,
                construcao.requisitos
            )
            
            self.recursos.dinheiro -= nova_construcao.custo
            self.construcoes.append(nova_construcao)
            self.aplicar_beneficios_construcao(nova_construcao)
            return True, f"{construcao.nome} construída com sucesso!"
        else:
            return False, mensagem
    
    def aplicar_beneficios_construcao(self, construcao):
        """Aplica os benefícios de uma construção aos recursos"""
        self.recursos.emissao_carbono += construcao.impacto_emissao
        self.recursos.satisfacao_populacional += construcao.impacto_satisfacao
        
        # Limita satisfação entre 0-100
        self.recursos.satisfacao_populacional = max(0, min(100, self.recursos.satisfacao_populacional))
        
    def atualizar_estado(self):
        """Atualiza o estado da cidade a cada ciclo de jogo"""
        self.tempo_jogo += 1
        
        # Crescimento populacional baseado na satisfação
        if self.recursos.satisfacao_populacional > 70:
            self.populacao = int(self.populacao * 1.01)  # 1% de crescimento
        elif self.recursos.satisfacao_populacional < 40:
            self.populacao = int(self.populacao * 0.99)  # 1% de redução
            
        # Geração de renda baseada em construções e população
        renda_base = self.populacao * 0.5
        renda_construcoes = len(self.construcoes) * 25
        self.recursos.dinheiro += renda_base + renda_construcoes
        
        # Emissões base aumentam com população
        self.recursos.emissao_carbono += self.populacao * 0.01
        
    def get_estatisticas(self):
        """Retorna estatísticas da cidade"""
        return {
            'nome': self.nome,
            'dificuldade': self.dificuldade,
            'populacao': self.populacao,
            'tempo_jogo': self.tempo_jogo,
            'total_construcoes': len(self.construcoes),
            'recursos': self.recursos.to_dict()
        }
        
    def __str__(self):
        stats = self.get_estatisticas()
        return (f"🏙️ {self.nome} | 👥 {self.populacao} | "
                f"⏱️ {self.tempo_jogo}c | 🏗️ {len(self.construcoes)} construções")
# [file content end]