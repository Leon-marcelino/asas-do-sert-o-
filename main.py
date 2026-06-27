import pygame
import os
import sys
from config import *
from passaro import Passaro
from cano import Cano
from recursos import GerenciadorRecursos
from telas import InterfaceGrafica
import traceback

class Jogo:
    def __init__(self):
        pygame.init()
        
        self.largura = LARGURA_TELA
        self.altura = ALTURA_TELA
        
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Asas do Sertão")
        
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", int(self.altura * 0.038), bold=True)
        
        self.chao_y = int(self.altura * 0.85)
        self.estado = "MENU"
        
        GerenciadorRecursos.tocar_musica(1)
        
        assets_menu = GerenciadorRecursos.carregar_recursos_menu(self.largura, self.altura)
        self.interface = InterfaceGrafica(self.tela, self.largura, self.altura, self.fonte, assets_menu)
        
        self.fundo_atual = None
        self.chao_atual = None
        self.obstaculo_img_atual = None
        self.nivel_atual = 1
        
        self.espaco_canos_atual = int(self.altura * 0.25)
        self.frequencia_canos = int(FPS * 1.8)
        
        self.high_score = self.carregar_high_score()
        self.resetar_jogo(nivel=1)

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

    def resetar_jogo(self, nivel):
        self.nivel_atual = nivel
        
        if nivel == 1:
            img_p1, img_p2 = ARQUIVO_PASSARO1_N1, ARQUIVO_PASSARO2_N1
            self.velocidade_jogo = int(self.largura * 0.0075)
            self.espaco_canos_atual = int(self.altura * 0.26)
            self.frequencia_canos = int(FPS * 1.9)
        elif nivel == 2:
            img_p1, img_p2 = ARQUIVO_PASSARO1_N2, ARQUIVO_PASSARO2_N2
            self.velocidade_jogo = int(self.largura * 0.009)
            self.espaco_canos_atual = int(self.altura * 0.23)
            self.frequencia_canos = int(FPS * 1.7)
        elif nivel == 3:
            img_p1, img_p2 = ARQUIVO_PASSARO1_N3, ARQUIVO_PASSARO2_N3
            self.velocidade_jogo = int(self.largura * 0.0105)
            self.espaco_canos_atual = int(self.altura * 0.21)
            self.frequencia_canos = int(FPS * 1.5)
        else:
            img_p1, img_p2 = ARQUIVO_PASSARO1_N4, ARQUIVO_PASSARO2_N4
            self.velocidade_jogo = int(self.largura * 0.0125)
            self.espaco_canos_atual = int(self.altura * 0.19)
            self.frequencia_canos = int(FPS * 1.2)
            
        self.passaro = Passaro(self.largura, self.altura, img_p1, img_p2)
        
        GerenciadorRecursos.tocar_musica(nivel)
        self.fundo_atual = GerenciadorRecursos.carregar_fundo_nivel(self.largura, self.altura, nivel)
        self.chao_atual = GerenciadorRecursos.carregar_chao_nivel(self.largura, self.altura, nivel)
        self.obstaculo_img_atual = GerenciadorRecursos.carregar_obstaculo_nivel(nivel)
        
        self.canos = []
        self.score = 0
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
                            self.estado = "NIVEIS"
                        elif self.interface.rect_sair.collidepoint(pos_mouse):
                            rodando = False
                            
                    elif self.estado == "NIVEIS":
                        if self.interface.rect_btn1.collidepoint(pos_mouse):
                            self.resetar_jogo(nivel=1)
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_btn2.collidepoint(pos_mouse):
                            self.resetar_jogo(nivel=2)
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_btn3.collidepoint(pos_mouse):
                            self.resetar_jogo(nivel=3)
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_btn4.collidepoint(pos_mouse):
                            self.resetar_jogo(nivel=4)
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                            
                    elif self.estado == "JOGANDO":
                        self.passaro.pular()
                        
                    elif self.estado == "GAME_OVER":
                        if self.interface.rect_reiniciar.collidepoint(pos_mouse):
                            self.resetar_jogo(self.nivel_atual)
                            self.estado = "JOGANDO"
                            self.passaro.pular()
                        elif self.interface.rect_sair_gameover.collidepoint(pos_mouse):
                            self.estado = "MENU"
                            GerenciadorRecursos.tocar_musica(1)

            if self.estado == "JOGANDO":
                self.passaro.atualizar()
                
                self.timer_cano += 1
                if self.timer_cano >= self.frequencia_canos:
                    # Agora passamos a imagem do obstáculo carregada para o Cano!
                    self.canos.append(Cano(self.largura, self.altura, self.velocidade_jogo, self.espaco_canos_atual, self.obstaculo_img_atual))
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
        if self.estado == "MENU":
            self.interface.desenhar_menu(self.high_score)
        elif self.estado == "NIVEIS":
            self.interface.desenhar_niveis()
        else:
            if self.fundo_atual: 
                self.tela.blit(self.fundo_atual, (0, 0))
            else: 
                self.tela.fill(AZUL_CEU)
                
            for cano in self.canos:
                cano.desenhar(self.tela)
                
            if self.chao_atual:
                self.tela.blit(self.chao_atual, (0, self.chao_y))
            else:
                pygame.draw.rect(self.tela, CHAO_COR, (0, self.chao_y, self.largura, self.altura - self.chao_y))
            
            self.passaro.desenhar(self.tela)
            
            if self.estado == "JOGANDO":
                self.interface.desenhar_texto(f"Score: {self.score}", BRANCO, 20, 20)
            elif self.estado == "GAME_OVER":
                self.interface.desenhar_game_over(self.score, self.high_score)
                
        pygame.display.flip()

if __name__ == "__main__":
    try:
        jogo = Jogo()
        jogo.rodar()
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
        print("O jogo travou! Verifique o arquivo 'crash_log.txt' para ver os detalhes do erro.")
