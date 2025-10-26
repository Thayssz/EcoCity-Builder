# [file name]: src/models/base.py
# [file content begin]
class Recurso:
    """Classe para gerenciar os recursos da cidade"""
    
    def __init__(self, dinheiro=1000, emissao_carbono=50, satisfacao=70):
        self.dinheiro = dinheiro
        self.emissao_carbono = emissao_carbono
        self.satisfacao_populacional = satisfacao
        
    def verificar_recursos_suficientes(self, custo):
        """Verifica se há recursos suficientes para uma ação"""
        return self.dinheiro >= custo
        
    def atualizar(self, fator_tempo=1.0):
        """Atualiza recursos baseado no tempo e construções"""
        # Placeholder - será implementado com lógica real
        pass
        
    def __str__(self):
        return f"💰 ${self.dinheiro:.2f} | 🌍 {self.emissao_carbono}CO₂ | 😊 {self.satisfacao_populacional}%"
        
    def to_dict(self):
        """Converte para dicionário para salvamento"""
        return {
            'dinheiro': self.dinheiro,
            'emissao_carbono': self.emissao_carbono,
            'satisfacao_populacional': self.satisfacao_populacional
        }
        
    @classmethod
    def from_dict(cls, data):
        """Cria instância a partir de dicionário"""
        return cls(
            dinheiro=data.get('dinheiro', 1000),
            emissao_carbono=data.get('emissao_carbono', 50),
            satisfacao=data.get('satisfacao_populacional', 70)
        )
# [file content end]