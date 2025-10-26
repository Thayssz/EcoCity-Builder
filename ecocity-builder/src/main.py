# [file name]: main.py
# [file content begin]
#!/usr/bin/env python3
"""
EcoCity Builder - Jogo educativo sobre ODS 13
Versão Completa 5.0 - Com pesquisas e estatísticas
"""
import pygame
import sys
import os
import time
import json
from datetime import datetime

# Configuração de paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

# Importações com fallback
try:
    from models.base import Recurso
    from models.cidade import Cidade
    from models.construcao import CONSTRUCOES_DISPONIVEIS
    print("✅ Modelos importados com sucesso")
except ImportError as e:
    print(f"❌ Erro importando modelos: {e}")
    # Definir classes básicas como fallback
    class Recurso:
        def __init__(self, dinheiro=1000, emissao_carbono=50, satisfacao=70):
            self.dinheiro = dinheiro
            self.emissao_carbono = emissao_carbono
            self.satisfacao_populacional = satisfacao
        def __str__(self):
            return f"💰 ${self.dinheiro:.0f} | 🌍 {self.emissao_carbono}CO₂ | 😊 {self.satisfacao_populacional}%"
        def to_dict(self):
            return {
                'dinheiro': self.dinheiro,
                'emissao_carbono': self.emissao_carbono,
                'satisfacao_populacional': self.satisfacao_populacional
            }
        @classmethod
        def from_dict(cls, data):
            return cls(
                data.get('dinheiro', 1000),
                data.get('emissao_carbono', 50),
                data.get('satisfacao_populacional', 70)
            )
    
    class Cidade:
        def __init__(self, nome, dificuldade="Médio"):
            self.nome = nome
            self.dificuldade = dificuldade
            self.populacao = 100
            self.recursos = Recurso()
            self.construcoes = []
            self.tecnologias_desbloqueadas = []
            self.tempo_jogo = 0
            
            # Ajustar dificuldade
            if dificuldade == "Fácil":
                self.recursos.dinheiro = 1500
                self.recursos.satisfacao_populacional = 80
            elif dificuldade == "Difícil":
                self.recursos.dinheiro = 700
                self.recursos.emissao_carbono = 60
                self.recursos.satisfacao_populacional = 60
                
        def atualizar_estado(self):
            self.tempo_jogo += 1
            # Simulação básica de crescimento
            if self.recursos.satisfacao_populacional > 70:
                self.populacao = int(self.populacao * 1.01)
            elif self.recursos.satisfacao_populacional < 40:
                self.populacao = int(self.populacao * 0.99)
                
            # Geração de renda
            renda_base = self.populacao * 0.5
            renda_construcoes = len(self.construcoes) * 25
            self.recursos.dinheiro += renda_base + renda_construcoes
            
        def adicionar_construcao(self, nome_construcao):
            # Simulação básica de construção
            construcoes_demo = {
                "Painel Solar": {"custo": 300, "emissao": -8, "satisfacao": 2},
                "Parque Eólico": {"custo": 500, "emissao": -12, "satisfacao": 3},
                "Usina Reciclagem": {"custo": 400, "emissao": -6, "satisfacao": 5},
                "Parque Público": {"custo": 200, "emissao": -3, "satisfacao": 8},
            }
            
            if nome_construcao in construcoes_demo:
                construcao = construcoes_demo[nome_construcao]
                if self.recursos.dinheiro >= construcao["custo"]:
                    self.recursos.dinheiro -= construcao["custo"]
                    self.recursos.emissao_carbono += construcao["emissao"]
                    self.recursos.satisfacao_populacional += construcao["satisfacao"]
                    self.construcoes.append(nome_construcao)
                    return True, f"{nome_construcao} construída com sucesso!"
                else:
                    return False, "Recursos insuficientes"
            return False, "Construção não encontrada"
            
        def __str__(self):
            return f"🏙️ {self.nome} | 👥 {self.populacao} | ⏱️ {self.tempo_jogo}c"

# Classe Botao
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
        pygame.draw.rect(tela, cor, self.rect, border_radius=8)
        pygame.draw.rect(tela, self.cor_texto, self.rect, 2, border_radius=8)
        
        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
        
    def esta_clicado(self, pos):
        return self.rect.collidepoint(pos)
        
    def atualizar(self, pos_mouse):
        self.esta_sobre = self.rect.collidepoint(pos_mouse)

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
        
        # Lista de construções (simplificada para demo)
        construcoes_demo = [
            {"nome": "Painel Solar", "custo": 300, "impacto_emissao": -8, "impacto_satisfacao": 2},
            {"nome": "Parque Eólico", "custo": 500, "impacto_emissao": -12, "impacto_satisfacao": 3},
            {"nome": "Usina Reciclagem", "custo": 400, "impacto_emissao": -6, "impacto_satisfacao": 5},
            {"nome": "Parque Público", "custo": 200, "impacto_emissao": -3, "impacto_satisfacao": 8},
            {"nome": "Ciclovia", "custo": 150, "impacto_emissao": -4, "impacto_satisfacao": 4},
            {"nome": "Transporte Elétrico", "custo": 600, "impacto_emissao": -15, "impacto_satisfacao": 6},
        ]
        
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        construcoes_pagina = construcoes_demo[inicio:fim]
        
        y_pos = painel_rect.y + 120
        for i, construcao in enumerate(construcoes_pagina):
            self.desenhar_item_construcao(construcao, painel_rect.x + 20, y_pos + i * 80, painel_rect.width - 40)
        
        # Botão fechar
        self.botao_fechar.desenhar(self.screen)
        
        # Instruções
        instrucoes = self.fonte_pequena.render("Clique em uma construção para construir", True, (200, 200, 200))
        self.screen.blit(instrucoes, (painel_rect.centerx - instrucoes.get_width()//2, self.altura - 40))
    
    def desenhar_item_construcao(self, construcao, x, y, largura):
        """Desenha um item de construção na lista"""
        # Fundo do item
        item_rect = pygame.Rect(x, y, largura, 70)
        pygame.draw.rect(self.screen, (50, 70, 120), item_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), item_rect, 1, border_radius=8)
        
        # Verificar se pode construir
        pode_construir = self.cidade.recursos.dinheiro >= construcao["custo"]
        cor_texto = (255, 255, 255) if pode_construir else (150, 150, 150)
        
        # Nome
        texto_nome = self.fonte_normal.render(f"{construcao['nome']}", True, cor_texto)
        self.screen.blit(texto_nome, (x + 10, y + 10))
        
        # Estatísticas
        emissao_str = f"+{construcao['impacto_emissao']}" if construcao['impacto_emissao'] >= 0 else f"{construcao['impacto_emissao']}"
        stats_text = self.fonte_pequena.render(
            f"Custo: ${construcao['custo']} | Emissão: {emissao_str}CO₂ | Satisfação: +{construcao['impacto_satisfacao']}%", 
            True, cor_texto
        )
        self.screen.blit(stats_text, (x + 10, y + 35))
        
        # Botão construir
        botao_construir = Botao(
            "Construir" if pode_construir else "Sem recursos",
            x + largura - 80, y + 35, 100, 30,
            (46, 204, 113) if pode_construir else (100, 100, 100),
            fonte=self.fonte_pequena
        )
        botao_construir.desenhar(self.screen)
        
        # Armazenar referência para clique
        if not hasattr(self, 'botoes_construir'):
            self.botoes_construir = []
        self.botoes_construir.append((botao_construir, construcao))
    
    def processar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão fechar
            if self.botao_fechar.esta_clicado(event.pos):
                return "fechar"
            
            # Botões construir
            if hasattr(self, 'botoes_construir'):
                for botao, construcao in self.botoes_construir:
                    if botao.esta_clicado(event.pos) and self.cidade.recursos.dinheiro >= construcao["custo"]:
                        # Simular construção
                        self.cidade.recursos.dinheiro -= construcao["custo"]
                        self.cidade.recursos.emissao_carbono += construcao["impacto_emissao"]
                        self.cidade.recursos.satisfacao_populacional += construcao["impacto_satisfacao"]
                        self.cidade.construcoes.append(construcao["nome"])
                        return "construido"
        
        # Limpar botoes_construir para próxima renderização
        if hasattr(self, 'botoes_construir'):
            self.botoes_construir.clear()
            
        return None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_fechar.atualizar(pos_mouse)

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
        
        # Tecnologias de demonstração
        self.tecnologias_demo = [
            {"nome": "Energia Solar Avançada", "custo": 800, "tempo": 10, "desbloqueada": False, "pesquisando": False, "requisitos": []},
            {"nome": "Veículos Elétricos", "custo": 1200, "tempo": 15, "desbloqueada": False, "pesquisando": False, "requisitos": ["Energia Solar Avançada"]},
            {"nome": "Agricultura Vertical", "custo": 600, "tempo": 8, "desbloqueada": False, "pesquisando": False, "requisitos": []},
        ]
        
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
        techs_desbloqueadas = len([t for t in self.tecnologias_demo if t["desbloqueada"]])
        texto_desbloqueadas = self.fonte_normal.render(f"Tecnologias Desbloqueadas: {techs_desbloqueadas}/{len(self.tecnologias_demo)}", True, (255, 255, 255))
        self.screen.blit(texto_desbloqueadas, (painel_rect.x + 20, painel_rect.y + 100))
        
        # Lista de tecnologias
        y_pos = painel_rect.y + 140
        for tecnologia in self.tecnologias_demo:
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
        cor_fundo = (60, 80, 140) if tecnologia["desbloqueada"] else (50, 70, 120)
        pygame.draw.rect(self.screen, cor_fundo, item_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), item_rect, 1, border_radius=8)
        
        # Status da tecnologia
        if tecnologia["desbloqueada"]:
            status = "✅ DESBLOQUEADA"
            cor_status = (46, 204, 113)
        elif tecnologia["pesquisando"]:
            status = "🔬 PESQUISANDO..."
            cor_status = (241, 196, 15)
        else:
            status = "🔒 BLOQUEADA"
            cor_status = (150, 150, 150)
        
        # Nome
        texto_nome = self.fonte_normal.render(tecnologia["nome"], True, (255, 255, 255))
        self.screen.blit(texto_nome, (x + 10, y + 10))
        
        # Status
        texto_status = self.fonte_pequena.render(status, True, cor_status)
        self.screen.blit(texto_status, (x + 10, y + 35))
        
        # Custo e tempo
        info_text = self.fonte_pequena.render(f"Custo: ${tecnologia['custo']} | Tempo: {tecnologia['tempo']}s", True, (200, 200, 200))
        self.screen.blit(info_text, (x + 10, y + 55))
        
        # Botão pesquisar (se disponível)
        pode_pesquisar = (not tecnologia["desbloqueada"] and 
                         not tecnologia["pesquisando"] and
                         self.cidade.recursos.dinheiro >= tecnologia["custo"] and
                         all(req in [t["nome"] for t in self.tecnologias_demo if t["desbloqueada"]] for req in tecnologia["requisitos"]))
        
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
        if tecnologia["requisitos"] and not tecnologia["desbloqueada"]:
            req_text = f"Requisitos: {', '.join(tecnologia['requisitos'])}"
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
                        # Simular pesquisa
                        if self.cidade.recursos.dinheiro >= tecnologia["custo"]:
                            self.cidade.recursos.dinheiro -= tecnologia["custo"]
                            tecnologia["pesquisando"] = True
                            # Simular conclusão após tempo
                            print(f"🔬 Pesquisa de {tecnologia['nome']} iniciada!")
                            return "pesquisa_iniciada"
        
        # Limpar botoes_pesquisar para próxima renderização
        if hasattr(self, 'botoes_pesquisar'):
            self.botoes_pesquisar.clear()
            
        return None
    
    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.botao_fechar.atualizar(pos_mouse)

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
        self.desenhar_secao_resumo(painel_rect.x + 20, painel_rect.y + 80, 400, 200)
        self.desenhar_secao_impacto(painel_rect.x + 440, painel_rect.y + 80, 400, 200)
        self.desenhar_secao_graficos(painel_rect.x + 20, painel_rect.y + 300, painel_rect.width - 40, 200)
        
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
            f"🔬 Tecnologias: {len([t for t in self.cidade.tecnologias_desbloqueadas])}"
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
        emissao_inicial = 50
        reducao_emissao = emissao_inicial - emissao_atual
        
        satisfacao_atual = self.cidade.recursos.satisfacao_populacional
        satisfacao_inicial = 70
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
                cor = (46, 204, 113)
            elif "Redução" in dado and reducao_emissao < 0:
                cor = (231, 76, 60)
                
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

class GerenciadorSalvamento:
    def __init__(self, pasta_saves="saves"):
        self.pasta_saves = pasta_saves
        self.criar_pasta_saves()
    
    def criar_pasta_saves(self):
        if not os.path.exists(self.pasta_saves):
            os.makedirs(self.pasta_saves)
    
    def salvar_jogo(self, cidade, nome_arquivo=None):
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{cidade.nome}_{timestamp}.json"
        
        caminho_save = os.path.join(self.pasta_saves, nome_arquivo)
        
        dados_save = {
            'cidade': {
                'nome': cidade.nome,
                'dificuldade': cidade.dificuldade,
                'populacao': cidade.populacao,
                'tempo_jogo': cidade.tempo_jogo,
                'construcoes': cidade.construcoes,
            },
            'recursos': cidade.recursos.to_dict(),
            'metadata': {
                'data_salvamento': datetime.now().isoformat(),
                'versao_jogo': '1.0'
            }
        }
        
        try:
            with open(caminho_save, 'w', encoding='utf-8') as f:
                json.dump(dados_save, f, indent=2, ensure_ascii=False)
            return True, f"Jogo salvo em {nome_arquivo}"
        except Exception as e:
            return False, f"Erro ao salvar: {e}"

class EcoCityBuilder:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Configurações da janela
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("EcoCity Builder - ODS 13")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Estados do jogo
        self.estados = {
            "MENU_PRINCIPAL": "menu_principal",
            "CRIAR_MUNDO": "criar_mundo", 
            "JOGANDO": "jogando",
            "PAUSADO": "pausado",
            "MENU_CONSTRUCOES": "menu_construcoes",
            "MENU_PESQUISAS": "menu_pesquisas",
            "PAINEL_ESTATISTICAS": "painel_estatisticas"
        }
        self.estado_atual = self.estados["MENU_PRINCIPAL"]
        
        # Componentes do jogo
        self.menu_principal = MenuPrincipal(self.screen)
        self.tela_criacao = None
        self.menu_construcoes = None
        self.menu_pesquisas = None
        self.painel_estatisticas = None
        self.cidade = None
        
        # Sistemas
        self.gerenciador_salvamento = GerenciadorSalvamento()
        
        # Temporizadores
        self.ultima_atualizacao = 0
        self.intervalo_atualizacao = 1000  # 1 segundo
        self.ultimo_salvamento_auto = 0
        self.intervalo_salvamento_auto = 30000  # 30 segundos
        
        # Botões da tela de jogo
        self.botoes_jogo = self.criar_botoes_jogo()
        
        # Alertas
        self.mostrar_alerta = False
        self.tempo_alerta = 0
        self.mensagem_alerta = ""
        
        # Fontes
        self.fontes = {
            'titulo': pygame.font.Font(None, 64),
            'subtitulo': pygame.font.Font(None, 36),
            'normal': pygame.font.Font(None, 24),
            'pequena': pygame.font.Font(None, 18)
        }
        
        # Cores
        self.cores = {
            'fundo': (25, 42, 86),
            'primaria': (46, 204, 113),
            'secundaria': (52, 152, 219),
            'destaque': (241, 196, 15),
            'perigo': (231, 76, 60),
            'texto': (255, 255, 255)
        }
        
        print("✅ EcoCity Builder inicializado!")
    
    def criar_botoes_jogo(self):
        return [
            Botao("🏗️ Construções", 150, 120, 200, 40, (46, 204, 113)),
            Botao("🔬 Pesquisas", 370, 120, 150, 40, (52, 152, 219)),
            Botao("📊 Estatísticas", 540, 120, 150, 40, (241, 196, 15)),
            Botao("💾 Salvar", 710, 120, 120, 40, (231, 76, 60))
        ]
    
    def lidar_com_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return self.processar_escape()
                elif evento.key == pygame.K_c and self.estado_atual == self.estados["JOGANDO"]:
                    self.abrir_menu_construcoes()
                elif evento.key == pygame.K_p and self.estado_atual == self.estados["JOGANDO"]:
                    self.abrir_menu_pesquisas()
                elif evento.key == pygame.K_e and self.estado_atual == self.estados["JOGANDO"]:
                    self.abrir_painel_estatisticas()
                elif evento.key == pygame.K_s and self.estado_atual == self.estados["JOGANDO"]:
                    self.salvar_jogo()
            
            resultado = self.processar_eventos_estado(evento)
            if resultado == "sair":
                return False
                    
        return True
    
    def processar_escape(self):
        if self.estado_atual == self.estados["JOGANDO"]:
            self.estado_atual = self.estados["PAUSADO"]
        elif self.estado_atual == self.estados["PAUSADO"]:
            self.estado_atual = self.estados["JOGANDO"]
        elif self.estado_atual == self.estados["MENU_CONSTRUCOES"]:
            self.estado_atual = self.estados["JOGANDO"]
        elif self.estado_atual == self.estados["MENU_PESQUISAS"]:
            self.estado_atual = self.estados["JOGANDO"]
        elif self.estado_atual == self.estados["PAINEL_ESTATISTICAS"]:
            self.estado_atual = self.estados["JOGANDO"]
        elif self.estado_atual == self.estados["CRIAR_MUNDO"]:
            self.estado_atual = self.estados["MENU_PRINCIPAL"]
        else:
            return False
        return True
    
    def processar_eventos_estado(self, evento):
        if self.estado_atual == self.estados["MENU_PRINCIPAL"]:
            acao = self.menu_principal.processar_eventos(evento)
            if acao:
                self.processar_acao_menu(acao)
                
        elif self.estado_atual == self.estados["CRIAR_MUNDO"] and self.tela_criacao:
            acao, nome, dificuldade = self.tela_criacao.processar_eventos(evento)
            if acao == "confirmar":
                self.iniciar_novo_jogo(nome, dificuldade)
            elif acao == "voltar":
                self.estado_atual = self.estados["MENU_PRINCIPAL"]
                
        elif self.estado_atual == self.estados["JOGANDO"]:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in self.botoes_jogo:
                    if botao.esta_clicado(evento.pos):
                        if botao.texto == "🏗️ Construções":
                            self.abrir_menu_construcoes()
                        elif botao.texto == "🔬 Pesquisas":
                            self.abrir_menu_pesquisas()
                        elif botao.texto == "📊 Estatísticas":
                            self.abrir_painel_estatisticas()
                        elif botao.texto == "💾 Salvar":
                            self.salvar_jogo()
                
        elif self.estado_atual == self.estados["MENU_CONSTRUCOES"] and self.menu_construcoes:
            resultado = self.menu_construcoes.processar_eventos(evento)
            if resultado == "fechar":
                self.estado_atual = self.estados["JOGANDO"]
                
        elif self.estado_atual == self.estados["MENU_PESQUISAS"] and self.menu_pesquisas:
            resultado = self.menu_pesquisas.processar_eventos(evento)
            if resultado == "fechar":
                self.estado_atual = self.estados["JOGANDO"]
                
        elif self.estado_atual == self.estados["PAINEL_ESTATISTICAS"] and self.painel_estatisticas:
            resultado = self.painel_estatisticas.processar_eventos(evento)
            if resultado == "fechar":
                self.estado_atual = self.estados["JOGANDO"]
        return None
    
    def processar_acao_menu(self, acao):
        print(f"🎯 Ação do menu: {acao}")
        
        if acao == "Novo Jogo":
            self.tela_criacao = TelaCriacaoMundo(self.screen)
            self.estado_atual = self.estados["CRIAR_MUNDO"]
        elif acao == "Carregar Jogo":
            print("📂 Carregar jogo (em desenvolvimento)")
        elif acao == "Configurações":
            print("⚙️ Configurações (em desenvolvimento)")
        elif acao == "Sair":
            pygame.quit()
            sys.exit()
    
    def iniciar_novo_jogo(self, nome_cidade, dificuldade):
        print(f"🆕 Iniciando novo jogo: {nome_cidade} ({dificuldade})")
        self.cidade = Cidade(nome_cidade, dificuldade)
        self.estado_atual = self.estados["JOGANDO"]
        print(f"🏙️ Nova cidade criada: {self.cidade}")
    
    def abrir_menu_construcoes(self):
        if self.cidade:
            self.menu_construcoes = MenuConstrucoes(self.screen, self.cidade)
            self.estado_atual = self.estados["MENU_CONSTRUCOES"]
    
    def abrir_menu_pesquisas(self):
        if self.cidade:
            self.menu_pesquisas = MenuPesquisas(self.screen, self.cidade)
            self.estado_atual = self.estados["MENU_PESQUISAS"]
    
    def abrir_painel_estatisticas(self):
        if self.cidade:
            self.painel_estatisticas = PainelEstatisticas(self.screen, self.cidade)
            self.estado_atual = self.estados["PAINEL_ESTATISTICAS"]
    
    def salvar_jogo(self):
        if self.cidade:
            sucesso, mensagem = self.gerenciador_salvamento.salvar_jogo(self.cidade)
            print(f"💾 {mensagem}")
            self.mostrar_alerta = True
            self.tempo_alerta = time.time()
            self.mensagem_alerta = "Jogo Salvo!"
    
    def atualizar(self):
        tempo_atual = pygame.time.get_ticks()
        
        if self.estado_atual == self.estados["MENU_PRINCIPAL"]:
            self.menu_principal.atualizar()
            
        elif self.estado_atual == self.estados["CRIAR_MUNDO"] and self.tela_criacao:
            self.tela_criacao.atualizar()
            
        elif self.estado_atual == self.estados["JOGANDO"] and self.cidade:
            # Atualização periódica da cidade
            if tempo_atual - self.ultima_atualizacao > self.intervalo_atualizacao:
                self.cidade.atualizar_estado()
                self.ultima_atualizacao = tempo_atual
            
            # Salvamento automático
            if tempo_atual - self.ultimo_salvamento_auto > self.intervalo_salvamento_auto:
                self.salvar_jogo()
                self.ultimo_salvamento_auto = tempo_atual
            
            # Atualizar botões
            for botao in self.botoes_jogo:
                botao.atualizar(pygame.mouse.get_pos())
                
        elif self.estado_atual == self.estados["MENU_CONSTRUCOES"] and self.menu_construcoes:
            self.menu_construcoes.atualizar()
            
        elif self.estado_atual == self.estados["MENU_PESQUISAS"] and self.menu_pesquisas:
            self.menu_pesquisas.atualizar()
            
        elif self.estado_atual == self.estados["PAINEL_ESTATISTICAS"] and self.painel_estatisticas:
            self.painel_estatisticas.atualizar()
        
        # Atualizar alertas
        if self.mostrar_alerta and time.time() - self.tempo_alerta > 3:
            self.mostrar_alerta = False
    
    def desenhar(self):
        self.screen.fill(self.cores['fundo'])
        
        if self.estado_atual == self.estados["MENU_PRINCIPAL"]:
            self.menu_principal.desenhar()
            
        elif self.estado_atual == self.estados["CRIAR_MUNDO"] and self.tela_criacao:
            self.tela_criacao.desenhar()
            
        elif self.estado_atual == self.estados["JOGANDO"]:
            self.desenhar_tela_jogo()
            
        elif self.estado_atual == self.estados["PAUSADO"]:
            self.desenhar_tela_jogo()
            self.desenhar_tela_pausa()
            
        elif self.estado_atual == self.estados["MENU_CONSTRUCOES"] and self.menu_construcoes:
            self.desenhar_tela_jogo()
            self.menu_construcoes.desenhar()
            
        elif self.estado_atual == self.estados["MENU_PESQUISAS"] and self.menu_pesquisas:
            self.desenhar_tela_jogo()
            self.menu_pesquisas.desenhar()
            
        elif self.estado_atual == self.estados["PAINEL_ESTATISTICAS"] and self.painel_estatisticas:
            self.desenhar_tela_jogo()
            self.painel_estatisticas.desenhar()
        
        # Desenhar alertas
        if self.mostrar_alerta:
            self.desenhar_alerta()
        
        pygame.display.flip()
    
    def desenhar_tela_jogo(self):
        if not self.cidade:
            return
            
        # Painel de recursos
        self.desenhar_painel_recursos()
        
        # Botões de ação
        for botao in self.botoes_jogo:
            botao.desenhar(self.screen)
        
        # Área principal do jogo
        area_jogo = pygame.Rect(50, 150, self.screen_width - 100, self.screen_height - 200)
        pygame.draw.rect(self.screen, (40, 55, 100), area_jogo, border_radius=10)
        
        # Informações da cidade
        info_cidade = self.fontes['subtitulo'].render(str(self.cidade), True, self.cores['texto'])
        self.screen.blit(info_cidade, (area_jogo.centerx - info_cidade.get_width()//2, area_jogo.y + 20))
        
        # Lista de construções
        const_text = self.fontes['normal'].render(f"Construções: {len(self.cidade.construcoes)}", True, self.cores['texto'])
        self.screen.blit(const_text, (area_jogo.x + 20, area_jogo.y + 60))
        
        for i, construcao in enumerate(self.cidade.construcoes[:8]):
            const_info = self.fontes['pequena'].render(f"• {construcao}", True, self.cores['texto'])
            self.screen.blit(const_info, (area_jogo.x + 20, area_jogo.y + 90 + i * 25))
        
        # Instruções
        instrucoes = self.fontes['pequena'].render("C: Construções | P: Pesquisas | E: Estatísticas | S: Salvar | ESC: Pausar", True, self.cores['texto'])
        self.screen.blit(instrucoes, (20, self.screen_height - 30))
    
    def desenhar_painel_recursos(self):
        painel = pygame.Rect(0, 0, self.screen_width, 100)
        pygame.draw.rect(self.screen, (35, 47, 75), painel)
        
        if self.cidade:
            recursos = self.cidade.recursos
            textos = [
                f"💰 ${recursos.dinheiro:.0f}",
                f"🌍 {recursos.emissao_carbono:.1f} CO₂",
                f"👥 {self.cidade.populacao}",
                f"😊 {recursos.satisfacao_populacional}%"
            ]
            
            for i, texto in enumerate(textos):
                surf = self.fontes['normal'].render(texto, True, self.cores['texto'])
                self.screen.blit(surf, (20 + i * 250, 40))
    
    def desenhar_tela_pausa(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pausa_text = self.fontes['titulo'].render("JOGO PAUSADO", True, self.cores['primaria'])
        instrucao = self.fontes['normal'].render("Pressione ESC para continuar", True, self.cores['texto'])
        
        self.screen.blit(pausa_text, (self.screen_width//2 - pausa_text.get_width()//2, self.screen_height//2 - 50))
        self.screen.blit(instrucao, (self.screen_width//2 - instrucao.get_width()//2, self.screen_height//2 + 20))
    
    def desenhar_alerta(self):
        alerta_rect = pygame.Rect(self.screen_width//2 - 200, 50, 400, 60)
        pygame.draw.rect(self.screen, (241, 196, 15), alerta_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), alerta_rect, 2, border_radius=10)
        
        texto_alerta = self.fontes['normal'].render(self.mensagem_alerta, True, (44, 62, 80))
        self.screen.blit(texto_alerta, (alerta_rect.centerx - texto_alerta.get_width()//2, alerta_rect.centery - texto_alerta.get_height()//2))
    
    def executar(self):
        print("🎮 Iniciando EcoCity Builder...")
        print("📍 Controles:")
        print("- ESC: Navegar entre telas")
        print("- C: Construções | P: Pesquisas | E: Estatísticas | S: Salvar")
        print("- Mouse: Navegar e interagir")
        
        while True:
            if not self.lidar_com_eventos():
                break
                
            self.atualizar()
            self.desenhar()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

def main():
    try:
        jogo = EcoCityBuilder()
        jogo.executar()
    except Exception as e:
        print(f"❌ Erro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
# [file content end]