import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from scenes.scene import Scene
import utils.resource_loader as resources

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Cargar recursos
        resources.load_all_resources()
        
        # Inicializar fondo común
        self.init_background()
        
        # Preparar a Lupita
        self.wizard = resources.get_image('wizard')
        if self.wizard:
            wizard_height = 150
            wizard_scale = wizard_height / self.wizard.get_height()
            wizard_size = (int(self.wizard.get_width() * wizard_scale), wizard_height)
            self.wizard = pygame.transform.scale(self.wizard, wizard_size)
            self.wizard_pos = [SCREEN_WIDTH//2 - wizard_size[0]//2, SCREEN_HEIGHT//2 - wizard_size[1]//2]
            self.wizard_float_offset = 0
        
        # Preparar textos con la misma fuente que la intro
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Crear textos con efectos
        self.title = self.font.render("LA AVENTURA MÁGICA DE LUPITA", True, COLORS['BLANCO'])
        self.press_space = self.font_small.render("PRESIONA ESPACIO", True, COLORS['BLANCO'])
        
        # Variables para efectos de texto
        self.text_alpha = 255
        self.alpha_speed = 2
        
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
        
        # Actualizar fondo común
        self.update_background()
        
        # Animar flotación de Lupita
        self.wizard_float_offset = (self.wizard_float_offset + 1) % 360
        float_offset = math.sin(math.radians(self.wizard_float_offset)) * 15
        self.wizard_pos[1] = SCREEN_HEIGHT//2 - self.wizard.get_height()//2 + float_offset
        
        # Actualizar efectos de texto
        self.text_alpha = abs(math.sin(tiempo_actual * 0.005)) * 255
        
        # Animar partículas
        for p in self.particles:
            p['angle'] = (p['angle'] + p['speed']) % 360
            centro_x = self.wizard_pos[0] + self.wizard.get_width()//2
            centro_y = self.wizard_pos[1] + self.wizard.get_height()//2
            radio = 50 + math.sin(math.radians(p['angle'])) * 20
            p['pos'][0] = centro_x + math.cos(math.radians(p['angle'])) * radio
            p['pos'][1] = centro_y + math.sin(math.radians(p['angle'])) * radio
            p['alpha'] = 128 + int(math.sin(tiempo_actual * 0.001 + p['angle']) * 127)
    
    def draw(self, screen):
        # Dibujar fondo común
        self.draw_background(screen)
        
        # Dibujar partículas
        for p in self.particles:
            surf = pygame.Surface((p['size'], p['size']))
            surf.fill(COLORS['BLANCO'])
            surf.set_alpha(p['alpha'])
            screen.blit(surf, p['pos'])
        
        # Dibujar a Lupita
        screen.blit(self.wizard, self.wizard_pos)
        
        # Dibujar sombra del título
        title_shadow = self.font.render("LA AVENTURA MÁGICA DE LUPITA", True, COLORS['NEGRO'])
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, 102))
        screen.blit(title_shadow, title_shadow_rect)
        
        # Dibujar título
        title_rect = self.title.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(self.title, title_rect)
        
        # Dibujar texto "Presiona ESPACIO" con efecto de parpadeo
        press_space_copy = self.press_space.copy()
        press_space_copy.set_alpha(self.text_alpha)
        press_space_rect = press_space_copy.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(press_space_copy, press_space_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # No detenemos la música aquí, dejamos que siga sonando
            self.game.change_scene("instructions")  # Cambiamos a la escena de instrucciones 