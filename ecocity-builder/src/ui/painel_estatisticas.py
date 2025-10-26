# [file name]: src/ui/painel_estatisticas.py
# [file content begin]
import pygame
from .botoes import Botao
from datetime import datetime

class PainelEstatisticas:
    def __init__(self, screen, cidade):
        self.screen = screen
        self.cidade = cidade
        self.largura, self.altura = screen.get_size()
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_subtitulo = pygame.font.Font(None, 32)
        self.fonte_normal = pygame.font.Font(None, 24)
        self.fonte_pequena = pygame.font.Font(None, 20)
        
        # Botões
        self.botao_fechar = Botao("Fechar", self.largura - 100, 50, 120, 40, (231, 76, 60))
        
        # Histórico de dados (simulado)
        self.historico_emissao = [50, 48, 45, 42, 40, 38, 35]
        self.historico_satisfacao = [70, 72, 75, 78, 80, 82, 85]
        self.historico_populacao = [100, 105, 110, 115, 120, 125, 130]
    
    def desenhar(self):
        # Fundo semi-transparente
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Painel principal
        painel_rect = pygame.Rect(80, 60, self.largura - 160, self.altura - 120)
        pygame.draw.rect(self.screen, (40, 55, 100), painel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), painel_rect, 2, border_radius=15)
        
        # Título
        titulo = self.fonte_titulo.render("Painel de Estatísticas", True, (46, 204, 113))
        self.screen.blit(titulo, (painel_rect.centerx - titulo.get_width()//2, painel_rect.y + 20))
        
        # Seções
        secoes = [
            self.desenhar_secao_resumo(painel_rect.x + 20, painel_rect.y + 80, 400, 200),
            self.desenhar_secao_impacto(painel_rect.x + 440, painel_rect.y + 80, 400, 200),
            self.desenhar_secao_graficos(painel_rect.x + 20, painel_rect.y + 300, painel_rect.width - 40, 200)
        ]
        
        # Botão fechar
        self.botao_fechar.desenhar(self.screen)
    
    def desenhar_secao_resumo(self, x, y, largura, altura):
        """Desenha a seção de resumo da cidade"""
        secao_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.screen, (50, 70, 120), secao_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), secao_rect, 1, border_radius=10)
        
        # Título da seção
        titulo = self.fonte_subtitulo.render("Resumo da Cidade", True, (241, 196, 15))
        self.screen.blit(titulo, (x + 10, y + 10))
        
        # Dados da cidade
        dados = [
            f"🏙️ Nome: {self.cidade.nome}",
            f"🎯 Dificuldade: {self.cidade.dificuldade}",
            f"⏱️ Tempo de Jogo: {self.cidade.tempo_jogo} ciclos",
            f"👥 População: {self.cidade.populacao} habitantes",
            f"🏗️ Construções: {len(self.cidade.construcoes)}",
            f"🔬 Tecnologias: {len([t for t in self.cidade.tecnologias_desbloqueadas if t.desbloqueada])}"
        ]
        
        for i, dado in enumerate(dados):
            texto = self.fonte_normal.render(dado, True, (255, 255, 255))
            self.screen.blit(texto, (x + 20, y + 50 + i * 25))
    
    def desenhar_secao_impacto(self, x, y, largura, altura):
        """Desenha a seção de impacto ambiental"""
        secao_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.screen, (50, 70, 120), secao_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), secao_rect, 1, border_radius=10)
        
        # Título da seção
        titulo = self.fonte_subtitulo.render("Impacto Ambiental", True, (46, 204, 113))
        self.screen.blit(titulo, (x + 10, y + 10))
        
        # Cálculos de impacto
        emissao_atual = self.cidade.recursos.emissao_carbono
        emissao_inicial = 50  # Valor inicial padrão
        reducao_emissao = emissao_inicial - emissao_atual
        
        satisfacao_atual = self.cidade.recursos.satisfacao_populacional
        satisfacao_inicial = 70  # Valor inicial padrão
        aumento_satisfacao = satisfacao_atual - satisfacao_inicial
        
        dados_impacto = [
            f"🌍 Emissão Atual: {emissao_atual:.1f} CO₂",
            f"📉 Redução de Emissão: {reducao_emissao:+.1f} CO₂",
            f"😊 Satisfação Atual: {satisfacao_atual}%",
            f"📈 Aumento Satisfação: {aumento_satisfacao:+d}%",
            f"💰 Investimento Total: ${self.calcular_investimento_total():.0f}",
            f"🌱 Eficiência: {self.calcular_eficiencia():.1f}%"
        ]
        
        for i, dado in enumerate(dados_impacto):
            cor = (255, 255, 255)
            if "Redução" in dado and reducao_emissao > 0:
                cor = (46, 204, 113)  # Verde para positivo
            elif "Redução" in dado and reducao_emissao < 0:
                cor = (231, 76, 60)   # Vermelho para negativo
                
            if "Aumento" in dado and aumento_satisfacao > 0:
                cor = (46, 204, 113)
            elif "Aumento" in dado and aumento_satisfacao < 0:
                cor = (231, 76, 60)
                
            texto = self.fonte_normal.render(dado, True, cor)
            self.screen.blit(texto, (x + 20, y + 50 + i * 25))
    
    def desenhar_secao_graficos(self, x, y, largura, altura):
        """Desenha a seção com gráficos simplificados"""
        secao_rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.screen, (50, 70, 120), secao_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), secao_rect, 1, border_radius=10)
        
        # Título da seção
        titulo = self.fonte_subtitulo.render("Evolução Temporal", True, (52, 152, 219))
        self.screen.blit(titulo, (x + 10, y + 10))
        
        # Gráfico de emissões
        texto_emissao = self.fonte_pequena.render("Emissões de CO₂:", True, (255, 255, 255))
        self.screen.blit(texto_emissao, (x + 20, y + 50))
        self.desenhar_grafico_simples(self.historico_emissao, x + 20, y + 70, 250, 60, (231, 76, 60))
        
        # Gráfico de satisfação
        texto_satisfacao = self.fonte_pequena.render("Satisfação Populacional:", True, (255, 255, 255))
        self.screen.blit(texto_satisfacao, (x + 300, y + 50))
        self.desenhar_grafico_simples(self.historico_satisfacao, x + 300, y + 70, 250, 60, (46, 204, 113))
        
        # Gráfico de população
        texto_populacao = self.fonte_pequena.render("População:", True, (255, 255, 255))
        self.screen.blit(texto_populacao, (x + 580, y + 50))
        self.desenhar_grafico_simples(self.historico_populacao, x + 580, y + 70, 250, 60, (241, 196, 15))
    
    def desenhar_grafico_simples(self, dados, x, y, largura, altura, cor):
        """Desenha um gráfico de linha simplificado"""
        if len(dados) < 2:
            return
            
        # Encontrar valores máximo e mínimo para escala
        max_val = max(dados)
        min_val = min(dados)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Desenhar eixo
        pygame.draw.line(self.screen, (200, 200, 200), (x, y + altura), (x + largura, y + altura), 2)
        
        # Desenhar linhas do gráfico
        pontos = []
        for i, valor in enumerate(dados):
            x_pos = x + (i / (len(dados) - 1)) * largura
            y_pos = y + altura - ((valor - min_val) / range_val) * altura
            pontos.append((x_pos, y_pos))
        
        if len(pontos) > 1:
            pygame.draw.lines(self.screen, cor, False, pontos, 3)
            
        # Desenhar pontos
        for ponto in pontos:
            pygame.draw.circle(self.screen, cor, (int(ponto[0]), int(ponto[1])), 4)
    
    def calcular_investimento_total(self):
        """Calcula o investimento total em construções e pesquisas"""
        # Simulação - na implementação real somaria custos reais
        return len(self.cidade.construcoes) * 300 + len(self.cidade.tecnologias_desbloqueadas) * 800
    
    def calcular_eficiencia(self):
        """Calcula uma métrica de eficiência geral"""
        if self.cidade.recursos.emissao_carbono <= 0:
            return 100.0
        
        eficiencia = (50 / self.cidade.recursos.emissao_carbono) * 100
        return min(eficiencia, 100.0)
    
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_fechar.esta_clicado(event.pos):
                return "fechar"
        return None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_fechar.atualizar(pos_mouse)
# [file content end]