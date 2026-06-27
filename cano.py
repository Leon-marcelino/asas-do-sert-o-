import pygame
import random
from config import VERDE_CANO, PRETO

class Cano:
    def __init__(self, largura, altura, velocidade_base, espaco_vertical, img_base=None):
        self.largura_tela = largura
        self.altura_tela = altura
        self.x = largura
        self.largura_cano = int(largura * 0.16)
        
        self.espaco = espaco_vertical
        self.altura_minima = int(altura * 0.1)
        self.altura_maxima = int(altura * 0.5)
        self.topo = random.randint(self.altura_minima, self.altura_maxima)
        self.base = self.topo + self.espaco
        
        self.velocidade = velocidade_base
        self.passou = False

        # Configuração das imagens do obstáculo
        self.usar_imagem = False
        if img_base:
            try:
                # Cano Inferior: Redimensiona a imagem para preencher do vão até o chão
                altura_inf = self.altura_tela - self.base
                self.img_inf = pygame.transform.scale(img_base, (self.largura_cano, altura_inf))
                
                # Cano Superior: Vira de ponta-cabeça e redimensiona do teto até o vão
                img_invertida = pygame.transform.flip(img_base, False, True)
                self.img_sup = pygame.transform.scale(img_invertida, (self.largura_cano, self.topo))
                
                self.usar_imagem = True
            except Exception:
                self.usar_imagem = False

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        if self.usar_imagem:
            # Desenha as imagens dos obstáculos
            tela.blit(self.img_sup, (self.x, 0))
            tela.blit(self.img_inf, (self.x, self.base))
        else:
            # Sistema de segurança: Desenha os retângulos caso o arquivo falte
            pygame.draw.rect(tela, VERDE_CANO, (self.x, 0, self.largura_cano, self.topo))
            pygame.draw.rect(tela, PRETO, (self.x, 0, self.largura_cano, self.topo), 2)
            
            altura_inferior = self.altura_tela - self.base
            pygame.draw.rect(tela, VERDE_CANO, (self.x, self.base, self.largura_cano, altura_inferior))
            pygame.draw.rect(tela, PRETO, (self.x, self.base, self.largura_cano, altura_inferior), 2)
