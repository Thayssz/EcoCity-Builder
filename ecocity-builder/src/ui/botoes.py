# [file name]: src/ui/botoes.py
# [file content begin]
import pygame

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor, cor_texto=(255, 255, 255), fonte=None):
        self.texto = texto
        self.rect = pygame.Rect(x - largura//2, y - altura//2, largura, altura)
        self.cor = cor
        self.cor_texto = cor_texto
        self.fonte = fonte or pygame.font.Font(None, 32)
        self.cor_hover = self._clarear_cor(cor, 30)
        self.esta_sobre = False
        
    def _clarear_cor(self, cor, valor):
        return tuple(min(255, c + valor) for c in cor)
        
    def desenhar(self, tela):
        cor = self.cor_hover if self.esta_sobre else self.cor
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)
        pygame.draw.rect(tela, self.cor_texto, self.rect, 2, border_radius=12)
        
        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
        
    def esta_clicado(self, pos):
        return self.rect.collidepoint(pos)
        
    def atualizar(self, pos_mouse):
        self.esta_sobre = self.rect.collidepoint(pos_mouse)
# [file content end]