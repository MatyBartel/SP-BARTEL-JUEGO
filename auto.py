import pygame
from config import *
from ruedas import Ruedas

class Auto(pygame.sprite.Sprite):
    def __init__(self, path_imagen:str, size:tuple, midLeft:tuple):
        super().__init__() 
        
        self.image = pygame.image.load(path_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.midleft = midLeft

        self.velocidad_X = 0
        self.velocidad_Y = 0

        self.ruedas_disponibles = 20

    def update(self):
        self.rect.x += self.velocidad_X
        self.rect.y += self.velocidad_Y

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH // 2 - 200:
            self.rect.right = WIDTH // 2 - 200
    
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT-60:
            self.rect.bottom = HEIGHT-60

    def disparar(self, sprites, ruedas):
        if self.ruedas_disponibles > 0:
            rueda = Ruedas(IMAGEN_RUEDAS, SIZE_RUEDAS, self.rect.midright, SPEED_RUEDAS)
            sound = pygame.mixer.Sound(SONIDO_RUEDAS)
            sound.play()
            sprites.add(rueda)
            ruedas.add(rueda)
            self.ruedas_disponibles -= 1
        else:
            sonido_sin_municion = pygame.mixer.Sound(SONIDO_NO_AMMO)
            sonido_sin_municion.play()

    def recargar(self):
        sonido_recargar = pygame.mixer.Sound(SONIDO_RECARGA)
        sonido_recargar.play()
        self.ruedas_disponibles = 20

    def reiniciar(self):
        self.rect.topleft = POS_AUTO