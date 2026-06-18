import pygame
import os
import sys
from config import LARGURA_TELA, ALTURA_TELA, FPS, AZUL_CEU, BRANCO, PRETO, CHAO_COR
from passaro import Passaro
from cano import Cano
from recursos import GerenciadorRecursos
from telas import InterfaceGrafica

class Jogo:
    def __init__(self):
        pygame.init()
        
        
        self.largura = LARGURA_TELA
        self.altura = ALTURA_TELA
        
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Asas do Sertão - Carcará")
        
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", int(self.altura * 0.038), bold=True)
        
        self.chao_y = int(self.altura * 0.85)
        self.velocidade_jogo_inicial = int(self.largura * 0.0075)
        self.velocidade_jogo = self.velocidade_jogo_inicial
        self.estado = "MENU"
        
        GerenciadorRecursos.iniciar_musica()
        self.fundo_img = GerenciadorRecursos.carregar_fundo(self.largura, self.altura)
        assets_menu = GerenciadorRecursos.carregar_recursos_menu(self.largura, self.altura)
        
        self.interface = InterfaceGrafica(self.tela, self.largura, self.altura, self.fonte, assets_menu)
        
        self.high_score = self.carregar_high_score()
        self.resetar_jogo()

    def carregar_high_score(self):
        if os.path.exists("highscore.txt"):
            try:
                with open("highscore.txt", "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def salvar_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def resetar_jogo(self):
        self.passaro = Passaro(self.largura, self.altura)
        self.canos = []
        self.score = 0
        self.velocidade_jogo = self.velocidade_jogo_inicial
        self.timer_cano = 0

    def rodar(self):
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                    elif evento.key == pygame.K_SPACE:
                        if self.estado == "JOGANDO":
                            self.passaro.pular()
                            
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = evento.pos
                    
                    if self.estado == "MENU":
                        if self.interface.rect_jogar.collidepoint(pos_mouse):
                            self.resetar_jogo()
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_sair.collidepoint(pos_mouse):
                            rodando = False
                            
                    elif self.estado == "JOGANDO":
                        self.passaro.pular()
                        
                    elif self.estado == "GAME_OVER":
                        # Lógica de cliques ajustada para os novos botões do Game Over
                        if self.interface.rect_reiniciar.collidepoint(pos_mouse):
                            self.resetar_jogo()
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_sair_gameover.collidepoint(pos_mouse):
                            rodando = False

            if self.estado == "JOGANDO":
                self.passaro.atualizar()
                
                self.timer_cano += 1
                if self.timer_cano >= int(FPS * 1.8):
                    self.canos.append(Cano(self.largura, self.altura, self.velocidade_jogo))
                    self.timer_cano = 0
                
                raio_efetivo = self.passaro.raio * 0.85
                
                for cano in self.canos[:]:
                    cano.atualizar()
                    
                    if cano.x < self.passaro.x + raio_efetivo and cano.x + cano.largura_cano > self.passaro.x - raio_efetivo:
                        if self.passaro.y - raio_efetivo < cano.topo or self.passaro.y + raio_efetivo > cano.base:
                            self.estado = "GAME_OVER"
                            self.salvar_high_score()
                    
                    if not cano.passou and cano.x + cano.largura_cano < self.passaro.x:
                        cano.passou = True
                        self.score += 1
                        self.velocidade_jogo += int(self.largura * 0.0008)

                    if cano.x + cano.largura_cano < 0:
                        self.canos.remove(cano)

                if self.passaro.y + self.passaro.raio >= self.chao_y:
                    self.estado = "GAME_OVER"
                    self.salvar_high_score()

            self.desenhar()

        pygame.quit()
        sys.exit()

    def desenhar(self):
        if self.fundo_img: 
            self.tela.blit(self.fundo_img, (0, 0))
        else: 
            self.tela.fill(AZUL_CEU)
            
        if self.estado == "MENU":
            self.interface.desenhar_menu(self.high_score)
        else:
            for cano in self.canos:
                cano.desenhar(self.tela)
                
            if self.interface.assets_menu.get('chao'):
                self.tela.blit(self.interface.assets_menu['chao'], (0, self.chao_y))
            else:
                pygame.draw.rect(self.tela, CHAO_COR, (0, self.chao_y, self.largura, self.altura - self.chao_y))
            
            self.passaro.desenhar(self.tela)
            
            if self.estado == "JOGANDO":
                self.interface.desenhar_texto(f"Score: {self.score}", BRANCO, 20, 20)
            elif self.estado == "GAME_OVER":
                self.interface.desenhar_game_over(self.score, self.high_score)
                
        pygame.display.flip()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()
