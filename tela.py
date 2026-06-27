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
        """Define as áreas de clique (hitboxes) de todos os botões do sistema"""
        largura_btn = int(self.largura * 0.60)
        altura_btn = int(self.altura * 0.11)
        x_centro = (self.largura - largura_btn) // 2
        
        # Hitboxes do Menu Inicial
        if self.assets_menu['btn_jogar']:
            y_base = int(self.altura * 0.50)
            espacamento = int(self.altura * 0.16)   
            self.rect_jogar = pygame.Rect(x_centro, y_base, largura_btn, altura_btn)
            self.rect_sair = pygame.Rect(x_centro, y_base + espacamento, largura_btn, altura_btn)
        else:
            self.rect_jogar = self.rect_sair = pygame.Rect(0, 0, 0, 0)
            
        # Hitboxes da tela de Níveis (Grade 2x2 simétrica)
        tamanho_btn = int(self.largura * 0.25)
        x_esquerda = int(self.largura * 0.18)
        x_direita = int(self.largura * 0.57)
        y_linha1 = int(self.altura * 0.35)
        y_linha2 = int(self.altura * 0.55)
        
        self.rect_btn1 = pygame.Rect(x_esquerda, y_linha1, tamanho_btn, tamanho_btn)
        self.rect_btn2 = pygame.Rect(x_direita, y_linha1, tamanho_btn, tamanho_btn)
        self.rect_btn3 = pygame.Rect(x_esquerda, y_linha2, tamanho_btn, tamanho_btn)
        self.rect_btn4 = pygame.Rect(x_direita, y_linha2, tamanho_btn, tamanho_btn)
            
        # Hitboxes da tela de Game Over
        painel_y = (self.altura - int(self.altura * 0.52)) // 2
        painel_altura = int(self.altura * 0.52)
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

    def desenhar_niveis(self):
        """Desenha a tela de seleção de níveis com os 4 botões inseridos"""
        if self.assets_menu.get('fundo_niveis'):
            self.tela.blit(self.assets_menu['fundo_niveis'], (0, 0))
        else:
            self.tela.fill(AZUL_CEU)
            
        # Desenha os botões numéricos na grade correspondente
        if self.assets_menu.get('btn_1'):
            self.tela.blit(self.assets_menu['btn_1'], self.rect_btn1.topleft)
        if self.assets_menu.get('btn_2'):
            self.tela.blit(self.assets_menu['btn_2'], self.rect_btn2.topleft)
        if self.assets_menu.get('btn_3'):
            self.tela.blit(self.assets_menu['btn_3'], self.rect_btn3.topleft)
        if self.assets_menu.get('btn_4'):
            self.tela.blit(self.assets_menu['btn_4'], self.rect_btn4.topleft)
            
    def desenhar_game_over(self, score, high_score):
        painel_largura = int(self.largura * 0.85)
        painel_altura = int(self.altura * 0.52)
        painel_x = (self.largura - painel_largura) // 2
        painel_y = (self.altura - painel_altura) // 2
        
        superficie_painel = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)
        superficie_painel.fill((0, 0, 0, 190))
        self.tela.blit(superficie_painel, (painel_x, painel_y))
        pygame.draw.rect(self.tela, PRETO, (painel_x, painel_y, painel_largura, painel_altura), 3)
        
        if self.assets_menu['img_gameover']:
            img_x = (self.largura - self.assets_menu['img_gameover'].get_width()) // 2
            self.tela.blit(self.assets_menu['img_gameover'], (img_x, painel_y + int(painel_altura * 0.05)))
        
        self.desenhar_texto(f"Pontos: {score}  |  Recorde: {high_score}", BRANCO, self.largura // 2, painel_y + int(painel_altura * 0.28), centralizado=True)
        
        if self.assets_menu['btn_reiniciar']:
            self.tela.blit(self.assets_menu['btn_reiniciar'], self.rect_reiniciar.topleft)
        if self.assets_menu['btn_sair']:
            self.tela.blit(self.assets_menu['btn_sair'], self.rect_sair_gameover.topleft)
