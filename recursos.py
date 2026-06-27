import pygame
from config import *

class GerenciadorRecursos:
    @staticmethod
    def tocar_musica(nivel):
        """Muda a música baseado no nível jogado"""
        pygame.mixer.init()
        if nivel == 1:
            arquivo = ARQUIVO_MUSICA_1
        elif nivel == 2:
            arquivo = ARQUIVO_MUSICA_2
        elif nivel == 3:
            arquivo = ARQUIVO_MUSICA_3
        else:
            arquivo = ARQUIVO_MUSICA_4
            
        try:
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Aviso: Não foi possível carregar a música '{arquivo}'.")

    @staticmethod
    def carregar_fundo_nivel(largura, altura, nivel):
        """Carrega o fundo específico da fase"""
        if nivel == 1:
            arquivo = ARQUIVO_FUNDO_1
        elif nivel == 2:
            arquivo = ARQUIVO_FUNDO_2
        elif nivel == 3:
            arquivo = ARQUIVO_FUNDO_3
        else:
            arquivo = ARQUIVO_FUNDO_4
            
        try:
            fundo_img = pygame.image.load(arquivo).convert()
            return pygame.transform.scale(fundo_img, (largura, altura))
        except pygame.error:
            print(f"Aviso: Fundo '{arquivo}' não encontrado.")
            return None

    @staticmethod
    def carregar_chao_nivel(largura, altura, nivel):
        """Carrega o chão específico da fase"""
        if nivel == 1:
            arquivo = ARQUIVO_CHAO_1
        elif nivel == 2:
            arquivo = ARQUIVO_CHAO_2
        elif nivel == 3:
            arquivo = ARQUIVO_CHAO_3
        else:
            arquivo = ARQUIVO_CHAO_4
            
        try:
            chao_img = pygame.image.load(arquivo).convert_alpha()
            return pygame.transform.scale(chao_img, (largura, int(altura * 0.15)))
        except pygame.error:
            print(f"Aviso: Chão '{arquivo}' não encontrado.")
            return None

    @staticmethod
    def carregar_obstaculo_nivel(nivel):
        """Carrega a imagem base do obstáculo para o nível atual"""
        if nivel == 1:
            arquivo = ARQUIVO_OBSTACULO_1
        elif nivel == 2:
            arquivo = ARQUIVO_OBSTACULO_2
        elif nivel == 3:
            arquivo = ARQUIVO_OBSTACULO_3
        else:
            arquivo = ARQUIVO_OBSTACULO_4
            
        try:
            return pygame.image.load(arquivo).convert_alpha()
        except pygame.error:
            print(f"Aviso: Imagem do obstáculo '{arquivo}' não encontrada. Usando modo clássico.")
            return None

    @staticmethod
    def carregar_recursos_menu(largura, altura):
        """Carrega os elementos visuais do menu, níveis e game over"""
        recursos = {}
        try:
            fundo_menu = pygame.image.load(ARQUIVO_MENU_FUNDO).convert()
            recursos['fundo'] = pygame.transform.scale(fundo_menu, (largura, altura))
            
            fundo_niveis = pygame.image.load(ARQUIVO_FUNDO_NIVEIS).convert()
            recursos['fundo_niveis'] = pygame.transform.scale(fundo_niveis, (largura, altura))
            
            largura_btn = int(largura * 0.60)
            altura_btn = int(altura * 0.11)
            
            recursos['btn_jogar'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_JOGAR).convert_alpha(), (largura_btn, altura_btn))
            recursos['btn_sair'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_SAIR).convert_alpha(), (largura_btn, altura_btn))
            recursos['img_gameover'] = pygame.transform.scale(pygame.image.load(ARQUIVO_GAME_OVER).convert_alpha(), (largura_btn, altura_btn))
            recursos['btn_reiniciar'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_REINICIAR).convert_alpha(), (largura_btn, altura_btn))
            
            tamanho_btn_nivel = int(largura * 0.25)
            recursos['btn_1'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_1).convert_alpha(), (tamanho_btn_nivel, tamanho_btn_nivel))
            recursos['btn_2'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_2).convert_alpha(), (tamanho_btn_nivel, tamanho_btn_nivel))
            recursos['btn_3'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_3).convert_alpha(), (tamanho_btn_nivel, tamanho_btn_nivel))
            recursos['btn_4'] = pygame.transform.scale(pygame.image.load(ARQUIVO_BTN_4).convert_alpha(), (tamanho_btn_nivel, tamanho_btn_nivel))
            
        except pygame.error as e:
            print(f"Erro ao carregar interface: {e}")
            for key in ['fundo', 'fundo_niveis', 'btn_jogar', 'btn_sair', 'img_gameover', 'btn_reiniciar', 'btn_1', 'btn_2', 'btn_3', 'btn_4']:
                recursos[key] = None
            
        return recursos
