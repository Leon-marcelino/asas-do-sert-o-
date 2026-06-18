import pygame
from config import AMARELO_PASSARO, PRETO

class Passaro:
    def __init__(self, largura, altura):
        self.x = int(largura * 0.15)  # Movido ligeiramente para a frente para melhor visibilidade
        self.y = altura // 2
        self.raio = int(altura * 0.045)  # Ajuste fino no raio
        
        self.gravidade = altura * 0.00075
        self.impulso = -altura * 0.0125
        self.velocidade = 0

        tamanho_imagem = self.raio * 2
        try:
            self.img1 = pygame.image.load("16514-removebg-preview.png").convert_alpha()
            self.img1 = pygame.transform.scale(self.img1, (tamanho_imagem, tamanho_imagem))
            
            self.img2 = pygame.image.load("16516-removebg-preview.png").convert_alpha()
            self.img2 = pygame.transform.scale(self.img2, (tamanho_imagem, tamanho_imagem))
            
            self.usar_imagens = True
        except pygame.error:
            print("Aviso: Imagens do pássaro não encontradas. Usando modelo padrão quadrado/circular.")
            self.usar_imagens = False

        self.tempo_animacao = 0

    def pular(self):
        self.velocidade = self.impulso

    def atualizar(self):
        self.velocidade += self.gravidade
        self.y += int(self.velocidade)
        
        if self.y - self.raio < 0:
            self.y = self.raio
            self.velocidade = 0
            
        self.tempo_animacao += 1

    def desenhar(self, tela):
        if self.usar_imagens:
            if (self.tempo_animacao // 8) % 2 == 0:  # Batida de asas ligeiramente mais rápida
                imagem_atual = self.img1
            else:
                imagem_atual = self.img2
                
            pos_x = self.x - self.raio
            pos_y = self.y - self.raio
            tela.blit(imagem_atual, (pos_x, pos_y))
        else:
            pygame.draw.circle(tela, AMARELO_PASSARO, (self.x, self.y), self.raio)
            pygame.draw.circle(tela, PRETO, (self.x, self.y), self.raio, 2)
