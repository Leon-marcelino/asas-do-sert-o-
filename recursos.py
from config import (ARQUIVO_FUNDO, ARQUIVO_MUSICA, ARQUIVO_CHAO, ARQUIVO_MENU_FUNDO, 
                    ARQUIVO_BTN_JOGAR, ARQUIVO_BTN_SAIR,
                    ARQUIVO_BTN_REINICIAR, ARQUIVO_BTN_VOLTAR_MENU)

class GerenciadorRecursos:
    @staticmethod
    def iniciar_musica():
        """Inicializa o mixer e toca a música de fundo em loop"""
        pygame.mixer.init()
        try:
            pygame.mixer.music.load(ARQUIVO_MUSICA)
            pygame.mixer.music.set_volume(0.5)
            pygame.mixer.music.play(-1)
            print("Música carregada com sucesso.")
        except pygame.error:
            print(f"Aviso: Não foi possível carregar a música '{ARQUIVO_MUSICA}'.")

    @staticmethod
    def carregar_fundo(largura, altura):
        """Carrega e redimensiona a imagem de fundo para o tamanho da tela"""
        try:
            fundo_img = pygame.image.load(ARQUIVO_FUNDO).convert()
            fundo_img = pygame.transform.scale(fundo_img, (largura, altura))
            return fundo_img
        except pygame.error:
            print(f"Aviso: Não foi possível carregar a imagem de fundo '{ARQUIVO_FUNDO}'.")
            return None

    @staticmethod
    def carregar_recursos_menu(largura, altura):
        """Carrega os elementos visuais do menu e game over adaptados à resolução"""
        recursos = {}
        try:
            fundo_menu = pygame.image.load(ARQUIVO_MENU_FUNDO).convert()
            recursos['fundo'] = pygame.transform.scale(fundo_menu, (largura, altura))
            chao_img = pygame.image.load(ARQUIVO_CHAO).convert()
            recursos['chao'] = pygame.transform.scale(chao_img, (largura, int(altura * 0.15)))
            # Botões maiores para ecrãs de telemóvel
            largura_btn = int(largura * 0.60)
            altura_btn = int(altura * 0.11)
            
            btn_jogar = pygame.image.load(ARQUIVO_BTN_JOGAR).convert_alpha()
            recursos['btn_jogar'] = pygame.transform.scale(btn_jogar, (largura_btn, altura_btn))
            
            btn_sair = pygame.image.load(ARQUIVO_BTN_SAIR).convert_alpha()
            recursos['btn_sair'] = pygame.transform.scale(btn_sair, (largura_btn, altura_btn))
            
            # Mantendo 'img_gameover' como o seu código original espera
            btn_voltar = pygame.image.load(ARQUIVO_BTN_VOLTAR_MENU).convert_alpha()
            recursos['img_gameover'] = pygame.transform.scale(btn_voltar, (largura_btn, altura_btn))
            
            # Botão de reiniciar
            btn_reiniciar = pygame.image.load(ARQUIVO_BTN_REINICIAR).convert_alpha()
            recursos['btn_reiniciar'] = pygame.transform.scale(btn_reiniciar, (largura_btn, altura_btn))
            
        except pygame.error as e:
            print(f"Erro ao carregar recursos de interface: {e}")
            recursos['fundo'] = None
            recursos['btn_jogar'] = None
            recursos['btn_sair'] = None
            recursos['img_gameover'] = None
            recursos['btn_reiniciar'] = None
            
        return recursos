import pygame
from config import (ARQUIVO_FUNDO, ARQUIVO_MUSICA, ARQUIVO_CHAO, ARQUIVO_MENU_FUNDO, 
                    ARQUIVO_BTN_JOGAR, ARQUIVO_BTN_SAIR,
                    ARQUIVO_BTN_REINICIAR, ARQUIVO_BTN_VOLTAR_MENU)

class GerenciadorRecursos:
    @staticmethod
    def iniciar_musica():
        """Inicializa o mixer e toca a música de fundo em loop"""
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(ARQUIVO_MUSICA)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            print("Música carregada com sucesso.")
        except pygame.error:
            print(f"Aviso: Não foi possível carregar a música '{ARQUIVO_MUSICA}'.")

    @staticmethod
    def carregar_fundo(largura, altura):
        """Carrega e redimensiona a imagem de fundo para o tamanho da tela"""
        try:
            fundo_img = pygame.image.load(ARQUIVO_FUNDO).convert()
            fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
            return fundo_img
        except pygame.error:
            print(f"Aviso: Não foi possível carregar a imagem de fundo '{ARQUIVO_FUNDO}'.")
            return None

    @staticmethod
    def carregar_recursos_menu(largura, altura):
        """Carrega os elementos visuais do menu e game over adaptados à resolução"""
        recursos = {}
        try:
            fundo_menu = pygame.image.load(ARQUIVO_MENU_FUNDO).convert()
            recursos['fundo'] = pygame.transform.scale(fundo_menu, (largura, altura))
            chao_img = pygame.image.load(ARQUIVO_CHAO).convert()
            recursos['chao'] = pygame.transform.scale(chao_img, (largura, int(altura * 0.15)))
            # Botões maiores para ecrãs de telemóvel
            largura_btn = int(largura * 0.60)
            altura_btn = int(altura * 0.11)
            
            btn_jogar = pygame.image.load(ARQUIVO_BTN_JOGAR).convert_alpha()
            recursos['btn_jogar'] = pygame.transform.scale(btn_jogar, (largura_btn, altura_btn))
            
            btn_sair = pygame.image.load(ARQUIVO_BTN_SAIR).convert_alpha()
            recursos['btn_sair'] = pygame.transform.scale(btn_sair, (largura_btn, altura_btn))
            
            # Mantendo 'img_gameover' como o seu código original espera
            btn_voltar = pygame.image.load(ARQUIVO_BTN_VOLTAR_MENU).convert_alpha()
            recursos['img_gameover'] = pygame.transform.scale(btn_voltar, (largura_btn, altura_btn))
            
            # Botão de reiniciar
            btn_reiniciar = pygame.image.load(ARQUIVO_BTN_REINICIAR).convert_alpha()
            recursos['btn_reiniciar'] = pygame.transform.scale(btn_reiniciar, (largura_btn, altura_btn))
            
        except pygame.error as e:
            print(f"Erro ao carregar recursos de interface: {e}")
            recursos['fundo'] = None
            recursos['btn_jogar'] = None
            recursos['btn_sair'] = None
            recursos['img_gameover'] = None
            recursos['btn_reiniciar'] = None
            
        return recursos
