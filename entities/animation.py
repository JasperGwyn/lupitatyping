import pygame
import random
import math
from config import COLORS, GAME_CONFIG

class FallingAnimation:
    def __init__(self, texto, x, y):
        self.texto = texto
        self.x = x
        self.y = y
        self.alpha = 255  # Transparencia
        self.scale = 1.0  # Escala
        self.tiempo_inicio = pygame.time.get_ticks()
        self.activa = True
        self.fuente = pygame.font.Font(None, 36)
        
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        
        if tiempo_transcurrido > GAME_CONFIG['TIEMPO_ANIMACION']:
            self.activa = False
            return
        
        # Calculamos el progreso de la animación (0 a 1)
        progreso = tiempo_transcurrido / GAME_CONFIG['TIEMPO_ANIMACION']
        
        # La palabra se desvanece y cae
        self.alpha = max(0, 255 * (1 - progreso))
        self.y += GAME_CONFIG['VELOCIDAD_ANIMACION']
        self.scale = max(0.5, 1 - (progreso * 0.5))
        
    def draw(self, screen):
        if not self.activa:
            return
            
        # Crear superficie con transparencia
        texto_surface = self.fuente.render(self.texto, True, COLORS['ROJO'])
        texto_surface.set_alpha(self.alpha)
        
        # Escalar la superficie
        nuevo_ancho = int(texto_surface.get_width() * self.scale)
        nuevo_alto = int(texto_surface.get_height() * self.scale)
        texto_surface = pygame.transform.scale(texto_surface, (nuevo_ancho, nuevo_alto))
        
        # Dibujar en pantalla
        screen.blit(texto_surface, (self.x, self.y))

class ExplosionAnimation:
    def __init__(self, x, y, texto):
        self.particulas = []
        self.tiempo_inicio = pygame.time.get_ticks()
        self.activa = True
        
        # Crear partículas de la explosión
        for _ in range(20):  # 20 partículas por explosión
            angulo = random.uniform(0, 360)
            velocidad = random.uniform(2, 5)
            tamaño = random.randint(3, 8)
            # Usar funciones trigonométricas en lugar de Vector2
            angulo_rad = math.radians(angulo)
            dx = velocidad * math.cos(angulo_rad)
            dy = velocidad * math.sin(angulo_rad)
            self.particulas.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'tamaño': tamaño,
                'alpha': 255
            })
            
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        
        if tiempo_transcurrido > GAME_CONFIG['TIEMPO_ANIMACION']:
            self.activa = False
            return
            
        # Actualizar cada partícula
        for p in self.particulas:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['dy'] += 0.2  # Gravedad
            p['alpha'] = max(0, 255 * (1 - tiempo_transcurrido/GAME_CONFIG['TIEMPO_ANIMACION']))
            
    def draw(self, screen):
        if not self.activa:
            return
            
        for p in self.particulas:
            surf = pygame.Surface((p['tamaño'], p['tamaño']))
            surf.fill(COLORS['ROJO'])
            surf.set_alpha(p['alpha'])
            screen.blit(surf, (p['x'], p['y'])) 