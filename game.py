import pygame
import json
import sys
import random
from config import *
from auto import Auto
from conos import Cono
from nafta import Nafta
from policia import Policia
from vida import Vida

class Juego: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GALAXY CAR")  
        self.logo = pygame.image.load(IMAGEN_LOGO)
        pygame.display.set_icon(self.logo) 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.reloj = pygame.time.Clock()

        self.score = 0
        self.jugando = False
        self.finalizado = False
        self.pausa = False
        self.imagen_pausa = pygame.image.load(IMAGEN_ESC).convert_alpha()
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa, TAM_IMG_PAUSA)

        self.temporizador = TIEMPO
        self.segundos_anteriores = 0

        self.fondo = pygame.image.load(IMAGEN_LVL1).convert()#sacar el hardcodeo
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))
        self.fuente = pygame.font.Font(FUENTE, TAMANO_FUENTE)

        self.sprites = pygame.sprite.Group()
        self.conos = pygame.sprite.Group()
        self.ruedas = pygame.sprite.Group()
        self.naftas = pygame.sprite.Group()
        self.policias= pygame.sprite.Group()
        self.vidas = pygame.sprite.Group()

        self.img_vidas = [IMG_3_VIDAS, IMG_2_VIDAS, IMG_1_VIDA]
        self.vida_index = 0
        self.vida = Vida(self.img_vidas[self.vida_index], SIZE_VIDA)
        self.vidas = VIDAS

        self.auto = Auto(IMAGEN_AUTO, SIZE_AUTO, POS_AUTO)

        self.agregar_sprite(self.auto)
        self.agregar_sprite(self.vida)

# AGREGO SPRITES
    def agregar_sprite(self, sprite):
        self.sprites.add(sprite)

    def agregar_conos(self, cono):
        self.conos.add(cono)

    def agregar_rueda(self, rueda):
        self.ruedas.add(rueda)

    def agregar_nafta(self, nafta):
        self.naftas.add(nafta)

    def agregar_policia(self, policia):
        self.policias.add(policia)

# MENUS 
    def menu(self):
        self.score = 0
        fondo = pygame.image.load(IMG_MENU).convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

        texto_start = self.fuente.render(MENSAJE_START, True, CUSTOM_COLOR)
        rect_texto_start = texto_start.get_rect()
        rect_texto_start.center = CENTER

        # texto_config = self.fuente.render(MENSAJE_CONFIG, True, CUSTOM_COLOR)
        # rect_texto_config = texto_config.get_rect()

        texto_exit = self.fuente.render(MENSAJE_EXIT, True, CUSTOM_COLOR)
        rect_texto_exit = texto_exit.get_rect()
        rect_texto_exit.center = (WIDTH // 2, HEIGHT // 2 + 140)

        accion = "menu"
        while accion == "menu":
            self.screen.blit(fondo, ORIGIN)
            self.screen.blit(texto_start, rect_texto_start)
            # self.screen.blit(texto_config, rect_texto_config)
            self.screen.blit(texto_exit, rect_texto_exit)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    
                    self.salir()
                    

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_texto_start.collidepoint(evento.pos):
                        accion = "jugar"
                    if rect_texto_exit.collidepoint(evento.pos):
                        accion = "exit"
                        
        return accion

    def pausar(self):
        pausa = True
        texto_pausa = self.fuente.render(MENSAJE_PAUSA,  True, BLANCO)
        rect_texto_pausa = texto_pausa.get_rect()
        rect_texto_pausa.center = CENTER
        rect_imagen_pausa = self.imagen_pausa.get_rect()
        rect_imagen_pausa.midbottom = MID_BOTTOM
        while pausa:
            self.screen.fill(NEGRO)
            self.screen.blit(texto_pausa, rect_texto_pausa)
            self.screen.blit(self.imagen_pausa,rect_imagen_pausa)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    
                    self.salir()
                    
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pausa = False

# COMIENZO
    def comenzar(self):
        while True:
            
            estado = self.menu() 

            if estado == "jugar":
                self.jugar()
                if self.nivel == 2:
                    self.puntuacion()
            if estado == "exit":
                
                self.salir()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                
                self.salir()
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and self.auto.velocidad_X >= 0:
                    self.auto.velocidad_X = -SPEED_AUTO
                elif evento.key == pygame.K_RIGHT and self.auto.velocidad_X <= 0:
                    self.auto.velocidad_X = SPEED_AUTO

                elif evento.key == pygame.K_UP and self.auto.velocidad_Y <= 0:
                    self.auto.velocidad_Y = -SPEED_AUTO
                elif evento.key == pygame.K_DOWN and self.auto.velocidad_X <= 0:
                    self.auto.velocidad_Y = SPEED_AUTO

                elif evento.key == pygame.K_SPACE:
                    self.auto.disparar(self.sprites, self.ruedas)

                elif evento.key == pygame.K_ESCAPE:
                        self.pausar()

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and self.auto.velocidad_X < 0:
                    self.auto.velocidad_X = 0
                elif evento.key == pygame.K_RIGHT and self.auto.velocidad_X > 0:
                    self.auto.velocidad_X = 0
                elif evento.key == pygame.K_UP and self.auto.velocidad_Y < 0:
                    self.auto.velocidad_Y = 0
                elif evento.key == pygame.K_DOWN and self.auto.velocidad_Y > 0:
                    self.auto.velocidad_Y = 0

    def actualizar_elementos(self):
        self.generar_conos(MAX_CONOS)
        self.generar_nafta(MAX_NAFTA)
        self.generar_policias(MAX_POLICIA)
        self.sprites.update()

        for cono in self.conos:
            if cono.rect.left <= 0:
                cono.kill()
            lista = pygame.sprite.spritecollide(self.auto, self.conos,True)

            if len(lista) > 0:
                if self.vidas > 1:
                    self.vidas -= 1
                    self.vida_index += 1
                    self.vida.actualizar_imagen(self.img_vidas[self.vida_index],SIZE_VIDA)
                    self.vida.perder_vida()

                else:
                    self.game_over()

        for policia in self.policias:
            if policia.rect.bottom >= HEIGHT:
                policia.kill()
            lista = pygame.sprite.spritecollide(self.auto, self.policias,True)

            if len(lista) > 0:
                if self.vidas > 1:
                    self.vidas -= 1
                    self.vida_index += 1
                    self.vida.actualizar_imagen(self.img_vidas[self.vida_index],SIZE_VIDA)
                    self.vida.perder_vida()
                else:
                    self.game_over()

        for nafta in self.naftas:
            if nafta.rect.left <= 0:
                nafta.kill()
            lista_nafta = pygame.sprite.spritecollide(self.auto, self.naftas,True)

            if len(lista_nafta) > 0:
                self.auto.recargar()

        for rueda in self.ruedas:
            if rueda.rect.right <= 0:
                rueda.kill()

            lista = pygame.sprite.spritecollide(rueda, self.conos, True)
            if len(lista):    
                rueda.kill()
                self.score += 1

    def renderizar_pantalla(self):
            self.screen.blit(self.fondo, ORIGIN)

            self.cronometro()

            self.sprites.draw(self.screen)

    def jugar(self):
        while True:
            
            self.reloj.tick(FPS)
            self.manejar_eventos()
            self.actualizar_elementos()
            self.renderizar_pantalla()
            pygame.display.update()
            

# ESCAPE
    def salir(self):
        pygame.quit()
        sys.exit()

    def terminar(self):
        self.jugando = False

# COMIENZO JUEGO (CRONOMETRO,GENERO SPRITES)
    def cronometro(self):
        segundos_transcurridos = pygame.time.get_ticks()//1000  
        if segundos_transcurridos > self.segundos_anteriores :
            self.temporizador -= 1
            self.segundos_anteriores = segundos_transcurridos
            if self.temporizador == 0:
                    self.nivel_ganado()
        texto_tiempo = self.fuente.render(str(self.temporizador), True, NEGRO)
        self.screen.blit(texto_tiempo, POS_TIEMPO)

    def generar_nafta(self, cantidad):
        if len(self.naftas) == 0:
            for i in range(cantidad):
                posicion = (random.randrange(WIDTH,WIDTH+100), random.randrange(0,HEIGHT))
                naftas = Nafta(IMAGEN_NAFTA, SIZE_NAFTA, posicion, SPEED_NAFTA)

                self.agregar_nafta(naftas)
                self.agregar_sprite(naftas)

    def generar_conos(self, cantidad):
        if len(self.conos) == 0:
            for i in range(cantidad):
                posicion = (random.randrange(WIDTH, WIDTH+200),random.randrange(0, HEIGHT - 100))
                conos = Cono(IMAGEN_CONOS, SIZE_CONOS, posicion, SPEED_CONOS)

                self.agregar_conos (conos)
                self.agregar_sprite(conos)

    def generar_policias(self, cantidad):
        if len(self.policias) == 0:
            for i in range(cantidad):
                posicion = (random.randrange(0, WIDTH), random.randrange(-20, 0))
                policias = Policia(IMAGEN_POLICIA, SIZE_POLICIA, posicion, SPEED_POLICIA)

                self.agregar_policia(policias)
                self.agregar_sprite(policias)

# PASAR / PERDER / REINICIAR / NUEVO NIVEL
    def game_over(self):
        self.finalizado = True
        sonido = pygame.mixer.Sound(SONIDO_PERDISTE)
        sonido.play()
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    
                    self.salir()
                    

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_texto_reintentar.collidepoint(evento.pos):
                        self.reinicar_juego()
            texto_perdiste = self.fuente.render(MENSAJE_PERDISTE, True, ROJO)
            rect_texto_perdiste = texto_perdiste.get_rect()
            rect_texto_perdiste.center = CENTER
            texto_reintentar = self.fuente.render(MENSAJE_REINTENTAR, True, ROJO)
            rect_texto_reintentar = texto_reintentar.get_rect()
            rect_texto_reintentar.center = (WIDTH//2,HEIGHT//2 + 100)
            self.screen.fill(NEGRO)
            self.screen.blit(texto_perdiste, rect_texto_perdiste)
            self.screen.blit(texto_reintentar, rect_texto_reintentar)

            pygame.display.flip()

    def nivel_ganado(self):
        self.score = self.score + 300

        texto_nivel_ganado = self.fuente.render(MENSAJE_NIVEL_PASADO, True, AZUL)
        rect_texto_nivel_ganado = texto_nivel_ganado.get_rect()
        rect_texto_nivel_ganado.center = CENTER

        texto_siguiente_nivel = self.fuente.render(MENSAJE_SIGUIENTE_NIVEL, True, AZUL)
        rect_texto_siguiente_nivel = texto_siguiente_nivel.get_rect()
        rect_texto_siguiente_nivel.center = (WIDTH // 2, HEIGHT // 2 + 200)

        texto_reintentar = self.fuente.render(MENSAJE_REINTENTAR, True, ROJO)
        rect_texto_reintentar = texto_reintentar.get_rect()
        rect_texto_reintentar.center = (WIDTH//2,HEIGHT//2 - 300)

        texto_puntuacion = self.fuente.render("Puntaje: " + str(self.score), True, AZUL)
        rect_texto_puntuacion = texto_puntuacion.get_rect()
        rect_texto_puntuacion.center = (WIDTH//2,HEIGHT//2 + 300)

        maximo_puntaje = self.leer_puntuacion()
        texto_maximo_puntaje = self.fuente.render("Max Score: " + str(maximo_puntaje), True, BLANCO)
        rect_maximo_puntaje = texto_maximo_puntaje.get_rect()
        rect_maximo_puntaje.center = (WIDTH//2,HEIGHT//2-200)

        self.screen.fill(NEGRO)
        self.screen.blit(texto_maximo_puntaje, rect_maximo_puntaje)
        self.screen.blit(texto_reintentar, rect_texto_reintentar)
        self.screen.blit(texto_puntuacion, rect_texto_puntuacion)
        self.screen.blit(texto_nivel_ganado, rect_texto_nivel_ganado)
        self.screen.blit(texto_siguiente_nivel, rect_texto_siguiente_nivel)
        sonido_pasaste = pygame.mixer.Sound(SONIDO_PASASTE)
        sonido_pasaste.play()
        pygame.display.flip()
        flag_nivel = 1
        while True:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    
                    self.salir()
                    
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_texto_siguiente_nivel.collidepoint(evento.pos): 
                        if flag_nivel == 1:
                            self.comenzar_nivel(IMAGEN_LVL2)
                            if self.temporizador == 0:
                                self.nivel = 2
                    elif rect_texto_reintentar.collidepoint(evento.pos):
                        self.reinicar_juego()

                    elif rect_texto_puntuacion.collidepoint(evento.pos):
                        self.puntuacion()

    def reinicar_juego(self):
        self.guardar_puntuacion()

        self.auto.recargar()
        self.auto.reiniciar()
        self.fondo = pygame.image.load(IMAGEN_LVL1).convert()#sacar el hardcodeo
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))
        self.score = 0
        self.temporizador = TIEMPO
        self.vidas = VIDAS
        self.vida_index = 0
        self.nivel = 1
        self.vida.actualizar_imagen(self.img_vidas[self.vida_index],SIZE_VIDA)
        self.auto.reiniciar()

        for sprite in self.conos:
            sprite.kill()
        for sprite in self.policias:
            sprite.kill()
        for sprite in self.naftas:
            sprite.kill()

        self.comenzar()

    def comenzar_nivel(self,imagen):
        self.temporizador = TIEMPO
        self.segundos_anteriores = 0
        self.temporizador = TIEMPO
        self.vidas = VIDAS
        self.vida_index = 0
        self.vida.actualizar_imagen(self.img_vidas[self.vida_index],SIZE_VIDA)
        self.auto.reiniciar()
        self.fondo = pygame.image.load(imagen).convert()
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))

        for sprite in self.conos:
            sprite.kill()
        for sprite in self.policias:
            sprite.kill()
        for sprite in self.naftas:
            sprite.kill()

        self.jugar()

# PUNTUACION
    def guardar_puntuacion(self):
        try:
            with open('puntuacion.json', 'r+') as archivo:
                puntuacion_existente = int(archivo.read())
        except (FileNotFoundError, json.JSONDecodeError):
            puntuacion_existente = 0

        if self.score > puntuacion_existente:
            with open('puntuacion.json', 'w+') as archivo:
                archivo.write(str(self.score))
                
    def leer_puntuacion(self):
        try:
            with open('puntuacion.json', 'r') as archivo:
                puntuacion = json.load(archivo)
        except FileNotFoundError:
            puntuacion = 0
        return puntuacion
juego = Juego()

juego.comenzar() 