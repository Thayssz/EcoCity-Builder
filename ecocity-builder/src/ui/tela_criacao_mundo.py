# [file name]: src/ui/tela_criacao_mundo.py
# [file content begin]
import pygame
from .botoes import Botao

class TelaCriacaoMundo:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = screen.get_size()
        self.fonte_titulo = pygame.font.Font(None, 64)
        self.fonte_normal = pygame.font.Font(None, 32)
        self.fonte_pequena = pygame.font.Font(None, 24)
        
        # Campos de entrada
        self.nome_cidade = "EcoVille"
        self.dificuldade_selecionada = "Médio"
        self.dificuldades = ["Fácil", "Médio", "Difícil"]
        
        # Botões
        self.botao_confirmar = Botao("Iniciar Jogo", self.largura//2, 500, 250, 60, (46, 204, 113))
        self.botao_voltar = Botao("Voltar", self.largura//2, 580, 250, 60, (231, 76, 60))
        
        # Estado do campo de texto
        self.campo_nome_ativo = False
        
    def desenhar(self):
        # Fundo
        self.screen.fill((25, 42, 86))
        
        # Título
        titulo = self.fonte_titulo.render("Criar Nova Cidade", True, (46, 204, 113))
        self.screen.blit(titulo, (self.largura//2 - titulo.get_width()//2, 80))
        
        # Campo Nome da Cidade
        texto_nome = self.fonte_normal.render("Nome da Cidade:", True, (255, 255, 255))
        self.screen.blit(texto_nome, (self.largura//2 - 200, 180))
        
        # Retângulo do campo de texto
        cor_campo = (52, 152, 219) if self.campo_nome_ativo else (100, 100, 150)
        pygame.draw.rect(self.screen, cor_campo, (self.largura//2 - 150, 210, 300, 50), border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.largura//2 - 150, 210, 300, 50), 2, border_radius=8)
        
        # Texto digitado
        texto_digitado = self.fonte_normal.render(self.nome_cidade, True, (255, 255, 255))
        self.screen.blit(texto_digitado, (self.largura//2 - 140, 225))
        
        # Cursor piscante se ativo
        if self.campo_nome_ativo and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = self.largura//2 - 140 + texto_digitado.get_width()
            pygame.draw.line(self.screen, (255, 255, 255), (cursor_x, 225), (cursor_x, 245), 2)
        
        # Seção Dificuldade
        texto_dificuldade = self.fonte_normal.render("Dificuldade:", True, (255, 255, 255))
        self.screen.blit(texto_dificuldade, (self.largura//2 - 200, 290))
        
        # Botões de dificuldade
        for i, dificuldade in enumerate(self.dificuldades):
            x = self.largura//2 - 150 + i * 100
            cor = (46, 204, 113) if dificuldade == self.dificuldade_selecionada else (100, 100, 150)
            botao_dificuldade = Botao(dificuldade, x, 330, 80, 40, cor, fonte=self.fonte_pequena)
            botao_dificuldade.desenhar(self.screen)
        
        # Informações da dificuldade
        info = self.obter_info_dificuldade()
        y_info = 380
        for linha in info:
            texto_info = self.fonte_pequena.render(linha, True, (200, 200, 200))
            self.screen.blit(texto_info, (self.largura//2 - texto_info.get_width()//2, y_info))
            y_info += 25
        
        # Botões principais
        self.botao_confirmar.desenhar(self.screen)
        self.botao_voltar.desenhar(self.screen)
        
    def obter_info_dificuldade(self):
        """Retorna informações sobre a dificuldade selecionada"""
        if self.dificuldade_selecionada == "Fácil":
            return [
                "💰 Dinheiro inicial: $1500",
                "😊 Satisfação inicial: 80%", 
                "🌍 Emissões moderadas",
                "🎯 Recomendado para iniciantes"
            ]
        elif self.dificuldade_selecionada == "Médio":
            return [
                "💰 Dinheiro inicial: $1000", 
                "😊 Satisfação inicial: 70%",
                "🌍 Emissões normais",
                "🎯 Experiência balanceada"
            ]
        else:  # Difícil
            return [
                "💰 Dinheiro inicial: $700",
                "😊 Satisfação inicial: 60%",
                "🌍 Emissões altas",
                "🎯 Desafio para experts"
            ]
    
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clique no campo de nome
            campo_rect = pygame.Rect(self.largura//2 - 150, 210, 300, 50)
            self.campo_nome_ativo = campo_rect.collidepoint(event.pos)
            
            # Verificar botões de dificuldade
            for i, dificuldade in enumerate(self.dificuldades):
                botao_rect = pygame.Rect(self.largura//2 - 150 + i * 100 - 40, 330 - 20, 80, 40)
                if botao_rect.collidepoint(event.pos):
                    self.dificuldade_selecionada = dificuldade
            
            # Botões principais
            if self.botao_confirmar.esta_clicado(event.pos):
                return "confirmar", self.nome_cidade, self.dificuldade_selecionada
            elif self.botao_voltar.esta_clicado(event.pos):
                return "voltar", None, None
                
        elif event.type == pygame.KEYDOWN and self.campo_nome_ativo:
            if event.key == pygame.K_BACKSPACE:
                self.nome_cidade = self.nome_cidade[:-1]
            elif event.key == pygame.K_RETURN:
                self.campo_nome_ativo = False
            else:
                # Limitar tamanho do nome
                if len(self.nome_cidade) < 20:
                    self.nome_cidade += event.unicode
        
        return None, None, None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_confirmar.atualizar(pos_mouse)
        self.botao_voltar.atualizar(pos_mouse)
# [file content end]