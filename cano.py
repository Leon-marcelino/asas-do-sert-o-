import pygame
import random
from config import VERDE_CANO, PRETO

class Cano:
    def __init__(self, largura, altura, velocidade_base):
        self.largura_tela = largura
        self.altura_tela = altura
        self.x = largura
        self.largura_cano = int(largura * 0.16)
        
        # Espaço vertical entre os canos adaptável
        self.espaco = int(altura * 0.25)
        
        self.altura_minima = int(altura * 0.1)
        self.altura_maxima = int(altura * 0.5)
        self.topo = random.randint(self.altura_minima, self.altura_maxima)
        self.base = self.topo + self.espaco
        
        self.velocidade = velocidade_base
        self.passou = False

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        # Cano Superior
        pygame.draw.rect(tela, VERDE_CANO, (self.x, 0, self.largura_cano, self.topo))
        pygame.draw.rect(tela, PRETO, (self.x, 0, self.largura_cano, self.topo), 2)
        
        # Cano Inferior
        altura_inferior = self.altura_tela - self.base
        pygame.draw.rect(tela, VERDE_CANO, (self.x, self.base, self.largura_cano, altura_inferior))
        pygame.draw.rect(tela, PRETO, (self.x, self.base, self.largura_cano, altura_inferior), 2)
