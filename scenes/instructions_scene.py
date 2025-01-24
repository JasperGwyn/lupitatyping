import pygame
import random
import math
from scenes.scene import Scene
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
import utils.resource_loader as resources

class InstructionsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
        # Cargar recursos visuales
        resources.load_all_resources()
        
        # Preparar el castillo de fondo
        self.castle = resources.get_image('castle')
        if self.castle:
            castle_height = SCREEN_HEIGHT // 2
            castle_scale = castle_height / self.castle.get_height()
            new_size = (int(self.castle.get_width() * castle_scale), castle_height)
            self.castle = pygame.transform.scale(self.castle, new_size)
            self.castle_pos = (SCREEN_WIDTH//2 - new_size[0]//2, SCREEN_HEIGHT - new_size[1] - 100)
        
        # Preparar nubes decorativas
        self.clouds = []
        cloud = resources.get_image('cloud1')
        if cloud:
            for _ in range(3):
                cloud_size = (random.randint(100, 150), random.randint(50, 75))
                cloud_scaled = pygame.transform.scale(cloud, cloud_size)
                self.clouds.append({
                    'surface': cloud_scaled,
                    'pos': [random.randint(0, SCREEN_WIDTH), random.randint(50, 150)],
                    'speed': random.uniform(0.2, 0.5)
                })
        
        # Texto de instrucciones
        self.instrucciones = [
            "¡BIENVENIDO A LA AVENTURA MÁGICA DE LUPITA!",
            "",
            "CÓMO JUGAR:",
            "- ESCRIBE LAS PALABRAS QUE CAEN ANTES DE QUE LLEGUEN AL SUELO",
            "- USA LAS TECLAS DEL COLOR CORRESPONDIENTE",
            "- PRESIONA ENTER PARA ENVIAR TU RESPUESTA",
            "- CADA NIVEL TIENE NUEVAS LETRAS Y MAYOR VELOCIDAD",
            "",
            "CONSEJOS:",
            "- MANTÉN TUS DEDOS EN LA POSICIÓN BASE (F Y J)",
            "- PRACTICA LA PRECISIÓN ANTES QUE LA VELOCIDAD",
            "- ¡DIVIÉRTETE MIENTRAS APRENDES!",
            "",
            "PRESIONA ESPACIO PARA COMENZAR"
        ]
        
    def update(self):
        # Actualizar posición de las nubes
        for cloud in self.clouds:
            cloud['pos'][0] += cloud['speed']
            if cloud['pos'][0] > SCREEN_WIDTH:
                cloud['pos'][0] = -cloud['surface'].get_width()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Detenemos la música de intro antes de iniciar el juego
            pygame.mixer.music.stop()
            self.game.change_scene("game")
    
    def draw(self, screen):
        # Dibujar fondo
        screen.fill(COLORS['AZUL_CIELO'])
        
        # Dibujar nubes
        for cloud in self.clouds:
            screen.blit(cloud['surface'], cloud['pos'])
        
        # Dibujar castillo
        if self.castle:
            screen.blit(self.castle, self.castle_pos)
        
        # Panel semitransparente para las instrucciones
        panel = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        panel.fill(COLORS['NEGRO'])
        panel.set_alpha(128)
        screen.blit(panel, (50, 50))
        
        # Dibujar instrucciones
        y = 80
        for linea in self.instrucciones:
            if linea == "":
                y += 20
                continue
                
            if "¡BIENVENIDO" in linea:
                texto = self.fuente.render(linea, True, COLORS['AMARILLO'])
            elif "CÓMO JUGAR:" in linea or "CONSEJOS:" in linea:
                texto = self.fuente.render(linea, True, COLORS['CELESTE'])
            elif "PRESIONA ESPACIO" in linea:
                # Efecto parpadeante
                tiempo = pygame.time.get_ticks()
                alpha = abs(math.sin(tiempo * 0.005)) * 255
                texto = self.fuente.render(linea, True, COLORS['AMARILLO'])
                texto.set_alpha(int(alpha))
            else:
                texto = self.fuente_pequeña.render(linea, True, COLORS['BLANCO'])
            
            texto_rect = texto.get_rect(centerx=SCREEN_WIDTH//2, y=y)
            screen.blit(texto, texto_rect)
            y += 40 