# [file name]: src/ui/menu_pesquisas.py
# [file content begin]
import pygame
from .botoes import Botao
from models.tecnologia import TECNOLOGIAS_DISPONIVEIS

class MenuPesquisas:
    def __init__(self, screen, cidade):
        self.screen = screen
        self.cidade = cidade
        self.largura, self.altura = screen.get_size()
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_normal = pygame.font.Font(None, 24)
        self.fonte_pequena = pygame.font.Font(None, 20)
        
        # Botões
        self.botao_fechar = Botao("Fechar", self.largura - 100, 50, 120, 40, (231, 76, 60))
        
        # Categorias
        self.categorias = list(set([tech.tipo for tech in TECNOLOGIAS_DISPONIVEIS]))
        self.categoria_selecionada = None
        
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
        titulo = self.fonte_titulo.render("Árvore de Tecnologias", True, (46, 204, 113))
        self.screen.blit(titulo, (painel_rect.centerx - titulo.get_width()//2, painel_rect.y + 20))
        
        # Recursos atuais
        recursos = self.cidade.recursos
        texto_recursos = self.fonte_normal.render(f"Recursos: 💰 ${recursos.dinheiro:.0f}", True, (255, 255, 255))
        self.screen.blit(texto_recursos, (painel_rect.x + 20, painel_rect.y + 70))
        
        # Tecnologias desbloqueadas
        techs_desbloqueadas = len([t for t in TECNOLOGIAS_DISPONIVEIS if t.desbloqueada])
        texto_desbloqueadas = self.fonte_normal.render(f"Tecnologias Desbloqueadas: {techs_desbloqueadas}/{len(TECNOLOGIAS_DISPONIVEIS)}", True, (255, 255, 255))
        self.screen.blit(texto_desbloqueadas, (painel_rect.x + 20, painel_rect.y + 100))
        
        # Lista de tecnologias
        y_pos = painel_rect.y + 140
        for tecnologia in TECNOLOGIAS_DISPONIVEIS:
            if self.categoria_selecionada is None or tecnologia.tipo == self.categoria_selecionada:
                self.desenhar_item_tecnologia(tecnologia, painel_rect.x + 20, y_pos, painel_rect.width - 40)
                y_pos += 90
        
        # Botão fechar
        self.botao_fechar.desenhar(self.screen)
        
        # Instruções
        instrucoes = self.fonte_pequena.render("Clique em uma tecnologia para pesquisar", True, (200, 200, 200))
        self.screen.blit(instrucoes, (painel_rect.centerx - instrucoes.get_width()//2, self.altura - 40))
    
    def desenhar_item_tecnologia(self, tecnologia, x, y, largura):
        """Desenha um item de tecnologia na lista"""
        # Fundo do item
        item_rect = pygame.Rect(x, y, largura, 80)
        cor_fundo = (60, 80, 140) if tecnologia.desbloqueada else (50, 70, 120)
        pygame.draw.rect(self.screen, cor_fundo, item_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), item_rect, 1, border_radius=8)
        
        # Status da tecnologia
        if tecnologia.desbloqueada:
            status = "✅ DESBLOQUEADA"
            cor_status = (46, 204, 113)
        elif tecnologia.pesquisando:
            progresso = tecnologia.get_progresso()
            status = f"🔬 PESQUISANDO... {progresso:.0f}%"
            cor_status = (241, 196, 15)
        else:
            status = "🔒 BLOQUEADA"
            cor_status = (150, 150, 150)
        
        # Nome e tipo
        texto_nome = self.fonte_normal.render(f"{tecnologia.nome} - {tecnologia.tipo.value}", True, (255, 255, 255))
        self.screen.blit(texto_nome, (x + 10, y + 10))
        
        # Status
        texto_status = self.fonte_pequena.render(status, True, cor_status)
        self.screen.blit(texto_status, (x + 10, y + 35))
        
        # Custo e tempo
        info_text = self.fonte_pequena.render(f"Custo: ${tecnologia.custo} | Tempo: {tecnologia.tempo_pesquisa}s", True, (200, 200, 200))
        self.screen.blit(info_text, (x + 10, y + 55))
        
        # Botão pesquisar (se disponível)
        pode_pesquisar = (not tecnologia.desbloqueada and 
                         not tecnologia.pesquisando and
                         self.cidade.recursos.dinheiro >= tecnologia.custo and
                         all(req in [t.nome for t in self.cidade.tecnologias_desbloqueadas] for req in tecnologia.requisitos))
        
        if pode_pesquisar:
            botao_pesquisar = Botao(
                "Pesquisar",
                x + largura - 60, y + 40, 100, 30,
                (52, 152, 219),
                fonte=self.fonte_pequena
            )
            botao_pesquisar.desenhar(self.screen)
            
            # Armazenar referência para clique
            if not hasattr(self, 'botoes_pesquisar'):
                self.botoes_pesquisar = []
            self.botoes_pesquisar.append((botao_pesquisar, tecnologia))
        
        # Requisitos (se houver)
        if tecnologia.requisitos and not tecnologia.desbloqueada:
            req_text = f"Requisitos: {', '.join(tecnologia.requisitos)}"
            texto_req = self.fonte_pequena.render(req_text, True, (200, 150, 150))
            self.screen.blit(texto_req, (x + largura - 250, y + 55))
    
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão fechar
            if self.botao_fechar.esta_clicado(event.pos):
                return "fechar"
            
            # Botões pesquisar
            if hasattr(self, 'botoes_pesquisar'):
                for botao, tecnologia in self.botoes_pesquisar:
                    if botao.esta_clicado(event.pos):
                        sucesso, mensagem = tecnologia.iniciar_pesquisa(self.cidade)
                        if sucesso:
                            self.cidade.tecnologias_desbloqueadas.append(tecnologia)
                            print(f"🔬 {mensagem}")
                            return "pesquisa_iniciada"
                        else:
                            print(f"❌ {mensagem}")
                            return "erro_pesquisa"
        
        # Limpar botoes_pesquisar para próxima renderização
        if hasattr(self, 'botoes_pesquisar'):
            self.botoes_pesquisar.clear()
            
        return None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_fechar.atualizar(pos_mouse)
# [file content end]