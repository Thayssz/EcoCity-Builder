# [file name]: src/ui/menu_principal.py
# [file content begin]
import pygame
from .botoes import Botao

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = screen.get_size()
        
        # Primeiro inicializar as fontes
        self.fonte_titulo = pygame.font.Font(None, 74)
        self.fonte_subtitulo = pygame.font.Font(None, 36)
        self.fonte_botoes = pygame.font.Font(None, 32)
        
        # Depois criar os botões (que usam as fontes)
        self.botoes = self.criar_botoes()
        
    def criar_botoes(self):
        centro_x = self.largura // 2
        botoes = [
            Botao("Novo Jogo", centro_x, 300, 300, 60, (46, 204, 113), fonte=self.fonte_botoes),
            Botao("Carregar Jogo", centro_x, 380, 300, 60, (52, 152, 219), fonte=self.fonte_botoes),
            Botao("Configurações", centro_x, 460, 300, 60, (241, 196, 15), fonte=self.fonte_botoes),
            Botao("Sair", centro_x, 540, 300, 60, (231, 76, 60), fonte=self.fonte_botoes)
        ]
        return botoes
        
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.atualizar(pos_mouse)
        
    def desenhar(self):
        # Fundo gradiente azul
        self.screen.fill((25, 42, 86))
        
        # Título principal
        titulo = self.fonte_titulo.render("EcoCity Builder", True, (46, 204, 113))
        subtitulo = self.fonte_subtitulo.render("ODS 13 - Ação Contra Mudanças Climáticas", True, (52, 152, 219))
        
        self.screen.blit(titulo, (self.largura//2 - titulo.get_width()//2, 150))
        self.screen.blit(subtitulo, (self.largura//2 - subtitulo.get_width()//2, 220))
        
        # Botões
        for botao in self.botoes:
            botao.desenhar(self.screen)
            
        # Rodapé com instruções
        fonte_pequena = pygame.font.Font(None, 20)
        instrucoes = fonte_pequena.render("Use o mouse para navegar | ESC para sair", True, (200, 200, 200))
        self.screen.blit(instrucoes, (20, self.altura - 30))
            
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for botao in self.botoes:
                if botao.esta_clicado(event.pos):
                    return botao.texto
        return None
# [file content end]