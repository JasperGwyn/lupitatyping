import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from scenes.scene import Scene
import utils.resource_loader as resources

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.fuente = pygame.font.Font(None, 48)
        self.fuente_pequeña = pygame.font.Font(None, 36)
        
        # Cargar recursos
        resources.load_all_resources()
        
        # Preparar el sol
        self.sun = resources.get_image('sun')
        if self.sun:
            sun_size = (100, 100)
            self.sun = pygame.transform.scale(self.sun, sun_size)
            self.sun_pos = [50, 50]
            self.sun_angle = 0
        
        # Preparar las nubes
        self.clouds = []
        cloud = resources.get_image('cloud1')
        if cloud:
            for _ in range(5):  # Mismo número de nubes que en la historia
                cloud_size = (random.randint(150, 250), random.randint(75, 125))
                cloud_scaled = pygame.transform.scale(cloud, cloud_size)
                self.clouds.append({
                    'surface': cloud_scaled,
                    'pos': [random.randint(0, SCREEN_WIDTH), random.randint(30, 200)],
                    'speed': random.uniform(0.3, 1.0)
                })
        
        # Preparar el castillo
        self.castle = resources.get_image('castle')
        if self.castle:
            castle_height = SCREEN_HEIGHT // 2
            castle_scale = castle_height / self.castle.get_height()
            castle_size = (int(self.castle.get_width() * castle_scale), castle_height)
            self.castle = pygame.transform.scale(self.castle, castle_size)
            # Posicionar el castillo en el centro
            self.castle_pos = (SCREEN_WIDTH//2 - castle_size[0]//2, SCREEN_HEIGHT - castle_size[1] - 100)
            
        # Preparar a Lupita
        self.wizard = resources.get_image('wizard')
        if self.wizard:
            wizard_height = 150
            wizard_scale = wizard_height / self.wizard.get_height()
            wizard_size = (int(self.wizard.get_width() * wizard_scale), wizard_height)
            self.wizard = pygame.transform.scale(self.wizard, wizard_size)
            # Posicionar a Lupita en el centro
            self.wizard_pos = [SCREEN_WIDTH//2 - wizard_size[0]//2, SCREEN_HEIGHT - wizard_size[1] - 150]
            self.wizard_float_offset = 0
            
        # Partículas mágicas
        self.particles = []
        for _ in range(30):
            self.particles.append({
                'pos': [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)],
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(2, 4),
                'alpha': random.randint(50, 200),
                'angle': random.uniform(0, 360)
            })
    
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Animar el sol
        if hasattr(self, 'sun_angle'):
            self.sun_angle = (self.sun_angle + 0.5) % 360
            self.sun_pos[1] = 50 + math.sin(math.radians(self.sun_angle)) * 10
        
        # Animar las nubes
        for cloud in self.clouds:
            cloud['pos'][0] -= cloud['speed']
            if cloud['pos'][0] + cloud['surface'].get_width() < -200:
                cloud['pos'][0] = SCREEN_WIDTH + random.randint(100, 300)
                cloud['pos'][1] = random.randint(30, 200)
        
        # Animar partículas
        for p in self.particles:
            p['angle'] = (p['angle'] + p['speed']) % 360
            centro_x = self.wizard_pos[0] + self.wizard.get_width()//2
            centro_y = self.wizard_pos[1] + self.wizard.get_height()//2
            radio = 50 + math.sin(math.radians(p['angle'])) * 20
            p['pos'][0] = centro_x + math.cos(math.radians(p['angle'])) * radio
            p['pos'][1] = centro_y + math.sin(math.radians(p['angle'])) * radio
            p['alpha'] = 128 + int(math.sin(tiempo_actual * 0.001 + p['angle']) * 127)
            
        # Animar flotación de Lupita
        if hasattr(self, 'wizard_float_offset'):
            self.wizard_float_offset = (self.wizard_float_offset + 2) % 360
            self.wizard_pos[1] = SCREEN_HEIGHT - self.wizard.get_height() - 150 + math.sin(math.radians(self.wizard_float_offset)) * 15
    
    def draw(self, screen):
        # Dibujar fondo
        screen.fill((135, 206, 235))  # Mismo color de cielo que en la historia
        
        # Dibujar sol con brillo
        if hasattr(self, 'sun'):
            # Brillo del sol
            glow = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 200, 64), (75, 75), 60)
            screen.blit(glow, (self.sun_pos[0] - 25, self.sun_pos[1] - 25))
            screen.blit(self.sun, self.sun_pos)
        
        # Dibujar nubes
        for cloud in self.clouds:
            screen.blit(cloud['surface'], cloud['pos'])
        
        # Dibujar castillo
        if hasattr(self, 'castle'):
            screen.blit(self.castle, self.castle_pos)
            
        # Dibujar partículas mágicas
        for p in self.particles:
            surf = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 255, p['alpha']), (p['size']//2, p['size']//2), p['size']//2)
            screen.blit(surf, p['pos'])
        
        # Dibujar a Lupita
        if hasattr(self, 'wizard'):
            screen.blit(self.wizard, self.wizard_pos)
            
        # Dibujar título y botones
        title = self.fuente.render("LA AVENTURA MÁGICA DE LUPITA", True, COLORS['BLANCO'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        start_text = self.fuente.render("PRESIONA ESPACIO PARA COMENZAR", True, COLORS['BLANCO'])
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        start_text.set_alpha(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
        screen.blit(start_text, start_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # No detenemos la música aquí, dejamos que siga sonando
            self.game.change_scene("instructions")  # Cambiamos a la escena de instrucciones en lugar de ir directo al juego 