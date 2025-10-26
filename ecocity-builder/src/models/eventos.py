# [file name]: src/models/evento.py
# [file content begin]
import random
from enum import Enum
from datetime import datetime

class TipoEvento(Enum):
    SECA = "Seca"
    INUNDACAO = "Inundação"
    TEMPESTADE = "Tempestade"
    ONDA_CALOR = "Onda de Calor"
    GEADA = "Geada"
    INCENDIO_FLORESTAL = "Incêndio Florestal"

class EventoClimatico:
    def __init__(self, tipo, intensidade=1.0):
        self.tipo = tipo
        self.intensidade = intensidade  # 1.0 = normal, 1.5 = forte, etc.
        self.ativo = False
        self.tempo_inicio = None
        self.duracao = random.randint(20, 60)  # segundos
        self.tempo_restante = self.duracao
        self.resolvido = False
        
        # Configurar efeitos baseado no tipo
        self.configurar_efeitos()
    
    def configurar_efeitos(self):
        """Configura os efeitos do evento baseado no tipo"""
        if self.tipo == TipoEvento.SECA:
            self.efeitos = {
                'dinheiro': -100 * self.intensidade,
                'satisfacao': -15 * self.intensidade,
                'emissao': 5 * self.intensidade,
                'descricao': "Baixa umidade e falta de água afetam a população"
            }
        elif self.tipo == TipoEvento.INUNDACAO:
            self.efeitos = {
                'dinheiro': -200 * self.intensidade,
                'satisfacao': -20 * self.intensidade,
                'emissao': 10 * self.intensidade,
                'descricao': "Chuvas intensas causam inundações"
            }
        elif self.tipo == TipoEvento.TEMPESTADE:
            self.efeitos = {
                'dinheiro': -150 * self.intensidade,
                'satisfacao': -10 * self.intensidade,
                'emissao': 8 * self.intensidade,
                'descricao': "Tempestade com ventos fortes e raios"
            }
        elif self.tipo == TipoEvento.ONDA_CALOR:
            self.efeitos = {
                'dinheiro': -80 * self.intensidade,
                'satisfacao': -12 * self.intensidade,
                'emissao': 15 * self.intensidade,
                'descricao': "Temperaturas extremamente altas"
            }
        elif self.tipo == TipoEvento.GEADA:
            self.efeitos = {
                'dinheiro': -120 * self.intensidade,
                'satisfacao': -8 * self.intensidade,
                'emissao': 3 * self.intensidade,
                'descricao': "Temperaturas congelantes afetam a cidade"
            }
        elif self.tipo == TipoEvento.INCENDIO_FLORESTAL:
            self.efeitos = {
                'dinheiro': -300 * self.intensidade,
                'satisfacao': -25 * self.intensidade,
                'emissao': 50 * self.intensidade,
                'descricao': "Incêndio florestal se aproxima da cidade"
            }
    
    def ativar(self, cidade):
        """Ativa o evento na cidade"""
        self.ativo = True
        self.tempo_inicio = datetime.now()
        self.tempo_restante = self.duracao
        
        # Aplicar efeitos iniciais
        cidade.recursos.dinheiro += self.efeitos['dinheiro']
        cidade.recursos.satisfacao_populacional += self.efeitos['satisfacao']
        cidade.recursos.emissao_carbono += self.efeitos['emissao']
        
        # Garantir limites
        cidade.recursos.satisfacao_populacional = max(0, min(100, cidade.recursos.satisfacao_populacional))
        cidade.recursos.dinheiro = max(0, cidade.recursos.dinheiro)
        
        return f"🌪️ EVENTO: {self.tipo.value} - {self.efeitos['descricao']}"
    
    def atualizar(self, delta_time):
        """Atualiza o tempo restante do evento"""
        if self.ativo and not self.resolvido:
            self.tempo_restante -= delta_time
            if self.tempo_restante <= 0:
                self.resolvido = True
                self.ativo = False
                return "evento_finalizado"
        return "evento_ativo"
    
    def get_info(self):
        """Retorna informações do evento para display"""
        if self.ativo:
            return {
                'tipo': self.tipo.value,
                'tempo_restante': int(self.tempo_restante),
                'descricao': self.efeitos['descricao'],
                'intensidade': self.intensidade
            }
        return None

class GerenteEventos:
    def __init__(self):
        self.evento_atual = None
        self.probabilidade_base = 0.01  # 1% de chance por atualização
        self.tempo_ultimo_evento = 0
        self.tempo_entre_eventos = 120  # segundos mínimos entre eventos
    
    def verificar_evento(self, cidade, tempo_decorrido):
        """Verifica se deve ocorrer um evento"""
        if self.evento_atual and self.evento_atual.ativo:
            return None
        
        # Verificar tempo mínimo entre eventos
        if tempo_decorrido - self.tempo_ultimo_evento < self.tempo_entre_eventos:
            return None
        
        # Aumentar probabilidade baseado em emissões
        probabilidade = self.probabilidade_base
        if cidade.recursos.emissao_carbono > 70:
            probabilidade *= 2
        elif cidade.recursos.emissao_carbono > 100:
            probabilidade *= 3
        
        # Verificar ocorrência
        if random.random() < probabilidade:
            self.tempo_ultimo_evento = tempo_decorrido
            return self.gerar_evento_aleatorio(cidade)
        
        return None
    
    def gerar_evento_aleatorio(self, cidade):
        """Gera um evento climático aleatório"""
        # Eventos mais prováveis com alta emissão
        if cidade.recursos.emissao_carbono > 80:
            tipos = [TipoEvento.SECA, TipoEvento.ONDA_CALOR, TipoEvento.INCENDIO_FLORESTAL, TipoEvento.TEMPESTADE]
        else:
            tipos = list(TipoEvento)
        
        tipo = random.choice(tipos)
        
        # Intensidade baseada em emissões
        intensidade = 1.0
        if cidade.recursos.emissao_carbono > 60:
            intensidade = 1.2
        if cidade.recursos.emissao_carbono > 90:
            intensidade = 1.5
        
        self.evento_atual = EventoClimatico(tipo, intensidade)
        return self.evento_atual
    
    def get_evento_atual(self):
        """Retorna o evento atual se estiver ativo"""
        if self.evento_atual and self.evento_atual.ativo:
            return self.evento_atual
        return None
# [file content end]