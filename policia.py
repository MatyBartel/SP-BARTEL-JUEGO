import pygame
from config import *
class Policia(pygame.sprite.Sprite):
    def __init__(self, path_imagen:str, size:tuple, midTop:tuple, speed):
        super().__init__()
        
        self.image = pygame.image.load(path_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.midtop = midTop

        self.velocidad_y = speed
        sonido_policia = pygame.mixer.Sound(SONIDO_POLICIA)
        sonido_policia.play()

    def update(self):
        self.rect.y += self.velocidad_y
