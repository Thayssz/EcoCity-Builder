class Recurso:
    """Classe base para gerenciamento de recursos"""
    
    def __init__(self, dinheiro=1000, emissao_carbono=50, satisfacao=70):
        self.dinheiro = dinheiro
        self.emissao_carbono = emissao_carbono
        self.satisfacao_populacional = satisfacao
    
    def atualizar(self):
        """Atualiza os recursos (método base para sobrescrever)"""
        pass
    
    def verificar_recursos_suficientes(self, custo):
        """Verifica se há recursos suficientes para uma ação"""
        return self.dinheiro >= custo
    
    def __str__(self):
        return f"💰 ${self.dinheiro:.2f} | 🌍 {self.emissao_carbono:.1f}CO₂ | 😊 {self.satisfacao_populacional}%"