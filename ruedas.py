import pygame
from config import *
class Ruedas(pygame.sprite.Sprite):
    def __init__(self,path_imagen:str,size, midRight:tuple, speed):
        super().__init__()  #llama al constructor del padre
        
        self.image = pygame.image.load(path_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.midright = midRight
        self.velocidad_x = speed
    
    def update(self):
        self.rect.x += self.velocidad_x
