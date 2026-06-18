import pygame
from config import AZUL_CEU, BRANCO, PRETO

class InterfaceGrafica:
    def __init__(self, tela, largura, altura, fonte, assets_menu):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.assets_menu = assets_menu
        self.calcular_posicoes_botoes()

    def calcular_posicoes_botoes(self):
        """Define as áreas de clique (hitboxes) dos botões no menu e no game over"""
        largura_btn = int(self.largura * 0.60)
        altura_btn = int(self.altura * 0.11)
        x_centro = (self.largura - largura_btn) // 2
        
        # Hitboxes do Menu Inicial (Mais afastados verticalmente)
        if self.assets_menu['btn_jogar']:
            y_base = int(self.altura * 0.50)
            espacamento = int(self.altura * 0.16)   
            self.rect_jogar = pygame.Rect(x_centro, y_base, largura_btn, altura_btn)
            self.rect_sair = pygame.Rect(x_centro, y_base + espacamento, largura_btn, altura_btn)
        else:
            self.rect_jogar = self.rect_sair = pygame.Rect(0, 0, 0, 0)
            
        # Hitboxes da tela de Game Over
        painel_y = (self.altura - int(self.altura * 0.52)) // 2
        painel_altura = int(self.altura * 0.52)
        
        # Centraliza o botão reiniciar e o botão de voltar (que no seu main.py atua como sair)
        self.rect_reiniciar = pygame.Rect(x_centro, painel_y + int(painel_altura * 0.42), largura_btn, altura_btn)
        self.rect_sair_gameover = pygame.Rect(x_centro, painel_y + int(painel_altura * 0.68), largura_btn, altura_btn)

    def desenhar_texto(self, texto, cor, x, y, centralizado=False):
        superficie_texto = self.fonte.render(texto, True, cor)
        rect_texto = superficie_texto.get_rect()
        if centralizado:
            rect_texto.center = (x, y)
        else:
            rect_texto.topleft = (x, y)
        self.tela.blit(superficie_texto, rect_texto)

    def desenhar_menu(self, high_score):
        if self.assets_menu['fundo']:
            self.tela.blit(self.assets_menu['fundo'], (0, 0))
        else:
            self.tela.fill(AZUL_CEU)
            
        if self.assets_menu['btn_jogar']:
            self.tela.blit(self.assets_menu['btn_jogar'], self.rect_jogar.topleft)
        if self.assets_menu['btn_sair']:
            self.tela.blit(self.assets_menu['btn_sair'], self.rect_sair.topleft)
            
    def desenhar_game_over(self, score, high_score):
        """Desenha a janela de pontuação sobreposta com imagem de título e botões corretos"""
        painel_largura = int(self.largura * 0.85)
        painel_altura = int(self.altura * 0.52)
        painel_x = (self.largura - painel_largura) // 2
        painel_y = (self.altura - painel_altura) // 2
        
        # Painel de fundo semitransparente
        superficie_painel = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)
        superficie_painel.fill((0, 0, 0, 190))
        self.tela.blit(superficie_painel, (painel_x, painel_y))
        pygame.draw.rect(self.tela, PRETO, (painel_x, painel_y, painel_largura, painel_altura), 3)
        
        # Desenha a imagem de Voltar para o Menu no topo do painel
        if self.assets_menu['img_gameover']:
            img_x = (self.largura - self.assets_menu['img_gameover'].get_width()) // 2
            self.tela.blit(self.assets_menu['img_gameover'], (img_x, painel_y + int(painel_altura * 0.05)))
        
        # Estatísticas
        self.desenhar_texto(f"Pontos: {score}  |  Recorde: {high_score}", BRANCO, self.largura // 2, painel_y + int(painel_altura * 0.28), centralizado=True)
        
        # Desenhar os botões clicáveis do Game Over
        if self.assets_menu['btn_reiniciar']:
            self.tela.blit(self.assets_menu['btn_reiniciar'], self.rect_reiniciar.topleft)
        if self.assets_menu['btn_sair']:
            # Desenhando o botão de sair na posição correta
            self.tela.blit(self.assets_menu['btn_sair'], self.rect_sair_gameover.topleft)
