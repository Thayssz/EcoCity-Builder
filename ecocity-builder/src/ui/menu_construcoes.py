# [file name]: src/ui/menu_construcoes.py
# [file content begin]
import pygame
from .botoes import Botao
from models.construcao import CONSTRUCOES_DISPONIVEIS

class MenuConstrucoes:
    def __init__(self, screen, cidade):
        self.screen = screen
        self.cidade = cidade
        self.largura, self.altura = screen.get_size()
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_normal = pygame.font.Font(None, 24)
        self.fonte_pequena = pygame.font.Font(None, 20)
        
        # Botões
        self.botao_fechar = Botao("Fechar", self.largura - 100, 50, 120, 40, (231, 76, 60))
        
        # Paginação
        self.pagina_atual = 0
        self.itens_por_pagina = 6
        self.botao_proxima = Botao("Próxima >", self.largura - 120, self.altura - 50, 100, 30, (52, 152, 219), fonte=self.fonte_pequena)
        self.botao_anterior = Botao("< Anterior", self.largura - 230, self.altura - 50, 100, 30, (52, 152, 219), fonte=self.fonte_pequena)
        
    def desenhar(self):
        # Fundo semi-transparente
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Painel principal
        painel_rect = pygame.Rect(100, 80, self.largura - 200, self.altura - 160)
        pygame.draw.rect(self.screen, (40, 55, 100), painel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), painel_rect, 2, border_radius=15)
        
        # Título
        titulo = self.fonte_titulo.render("Construções Disponíveis", True, (46, 204, 113))
        self.screen.blit(titulo, (painel_rect.centerx - titulo.get_width()//2, painel_rect.y + 20))
        
        # Recursos atuais
        recursos = self.cidade.recursos
        texto_recursos = self.fonte_normal.render(f"Recursos: 💰 ${recursos.dinheiro:.0f} | 🌍 {recursos.emissao_carbono:.1f}CO₂ | 😊 {recursos.satisfacao_populacional}%", 
                                                True, (255, 255, 255))
        self.screen.blit(texto_recursos, (painel_rect.x + 20, painel_rect.y + 70))
        
        # Lista de construções
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        construcoes_pagina = CONSTRUCOES_DISPONIVEIS[inicio:fim]
        
        y_pos = painel_rect.y + 120
        for i, construcao in enumerate(construcoes_pagina):
            self.desenhar_item_construcao(construcao, painel_rect.x + 20, y_pos + i * 80, painel_rect.width - 40)
        
        # Botões de paginação
        total_paginas = (len(CONSTRUCOES_DISPONIVEIS) + self.itens_por_pagina - 1) // self.itens_por_pagina
        if total_paginas > 1:
            texto_pagina = self.fonte_pequena.render(f"Página {self.pagina_atual + 1}/{total_paginas}", True, (200, 200, 200))
            self.screen.blit(texto_pagina, (painel_rect.centerx - texto_pagina.get_width()//2, self.altura - 80))
            
            self.botao_anterior.desenhar(self.screen)
            self.botao_proxima.desenhar(self.screen)
        
        # Botão fechar
        self.botao_fechar.desenhar(self.screen)
    
    def desenhar_item_construcao(self, construcao, x, y, largura):
        """Desenha um item de construção na lista"""
        # Fundo do item
        item_rect = pygame.Rect(x, y, largura, 70)
        pygame.draw.rect(self.screen, (50, 70, 120), item_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), item_rect, 1, border_radius=8)
        
        # Verificar se pode construir
        pode_construir, motivo = construcao.pode_construir(self.cidade.recursos, self.cidade.tecnologias_desbloqueadas)
        cor_texto = (255, 255, 255) if pode_construir else (150, 150, 150)
        
        # Nome e tipo
        texto_nome = self.fonte_normal.render(f"{construcao.nome} - {construcao.tipo.value}", True, cor_texto)
        self.screen.blit(texto_nome, (x + 10, y + 10))
        
        # Estatísticas
        emissao_str = f"+{construcao.impacto_emissao}" if construcao.impacto_emissao >= 0 else f"{construcao.impacto_emissao}"
        stats_text = self.fonte_pequena.render(
            f"Custo: ${construcao.custo} | Emissão: {emissao_str}CO₂ | Satisfação: +{construcao.impacto_satisfacao}%", 
            True, cor_texto
        )
        self.screen.blit(stats_text, (x + 10, y + 35))
        
        # Botão construir
        botao_construir = Botao(
            "Construir" if pode_construir else motivo,
            x + largura - 80, y + 35, 100, 30,
            (46, 204, 113) if pode_construir else (100, 100, 100),
            fonte=self.fonte_pequena
        )
        botao_construir.desenhar(self.screen)
        
        # Armazenar referência para clique
        if not hasattr(self, 'botoes_construir'):
            self.botoes_construir = []
        self.botoes_construir.append((botao_construir, construcao.nome))
    
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão fechar
            if self.botao_fechar.esta_clicado(event.pos):
                return "fechar"
            
            # Botões de paginação
            if self.botao_proxima.esta_clicado(event.pos):
                total_paginas = (len(CONSTRUCOES_DISPONIVEIS) + self.itens_por_pagina - 1) // self.itens_por_pagina
                if self.pagina_atual < total_paginas - 1:
                    self.pagina_atual += 1
                    
            if self.botao_anterior.esta_clicado(event.pos):
                if self.pagina_atual > 0:
                    self.pagina_atual -= 1
            
            # Botões construir
            if hasattr(self, 'botoes_construir'):
                for botao, nome_construcao in self.botoes_construir:
                    if botao.esta_clicado(event.pos):
                        sucesso, mensagem = self.cidade.adicionar_construcao(nome_construcao)
                        print(f"🏗️ {mensagem}")
                        if sucesso:
                            return "construido"
                        return "erro"
        
        # Limpar botoes_construir para próxima renderização
        if hasattr(self, 'botoes_construir'):
            self.botoes_construir.clear()
            
        return None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_fechar.atualizar(pos_mouse)
        self.botao_proxima.atualizar(pos_mouse)
        self.botao_anterior.atualizar(pos_mouse)
# [file content end]