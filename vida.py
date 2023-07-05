import pygame
from config import *
class Vida(pygame.sprite.Sprite):
    def __init__(self,path_imagen,size:tuple):
        super().__init__()  #llama al constructor del padre
        
        self.image = pygame.image.load(path_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.center = POS_VIDAS

    def actualizar_imagen(self, nueva_imagen,size):
        self.image =  pygame.image.load(nueva_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

    def perder_vida(self):
        sonido = pygame.mixer.Sound(SONIDO_VIDA)
        sonido.play()