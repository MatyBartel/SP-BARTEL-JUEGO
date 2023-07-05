import pygame

class Cono(pygame.sprite.Sprite):
    def __init__(self, path_imagen:str, size:tuple, midRight:tuple, speed):
        super().__init__()
        
        self.image = pygame.image.load(path_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.midright = midRight

        self.velocidad_x = speed
    
    def update(self):
        self.rect.x -= self.velocidad_x

