import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from scenes.scene import Scene
import utils.resource_loader as resources

class InstructionsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 42)
        self.font_small = pygame.font.Font(None, 36)
        
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
        
        # Textos de instrucciones
        self.instructions = [
            "¡BIENVENIDO A LA AVENTURA!",
            "ESCRIBE LAS PALABRAS QUE CAEN",
            "USA LAS TECLAS DEL COLOR CORRECTO",
            "¡NO DEJES QUE TOQUEN LA LÍNEA ROJA!"
        ]
        
        self.text_alpha = 255
    
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Actualizar fondo común
        self.update_background()
        
        # Animar partículas
        for p in self.particles:
            p['angle'] = (p['angle'] + p['speed']) % 360
            centro_x = self.wizard_pos[0] + self.wizard.get_width()//2
            centro_y = self.wizard_pos[1] + self.wizard.get_height()//2
            radio = 50 + math.sin(math.radians(p['angle'])) * 20
            p['pos'][0] = centro_x + math.cos(math.radians(p['angle'])) * radio
            p['pos'][1] = centro_y + math.sin(math.radians(p['angle'])) * radio
            p['alpha'] = 128 + int(math.sin(tiempo_actual * 0.001 + p['angle']) * 127)
        
        # Animar a Lupita
        if hasattr(self, 'wizard_float_offset'):
            self.wizard_float_offset = (self.wizard_float_offset + 2) % 360
            self.wizard_pos[1] = SCREEN_HEIGHT//2 - self.wizard.get_height()//2 + math.sin(math.radians(self.wizard_float_offset)) * 15
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mixer.music.stop()  # Detenemos la música de intro
            self.game.change_scene("game")
    
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
        if hasattr(self, 'wizard'):
            screen.blit(self.wizard, self.wizard_pos)
        
        # Panel semi-transparente para las instrucciones
        panel = pygame.Surface((SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.4))
        panel.fill(COLORS['NEGRO'])
        panel.set_alpha(128)
        panel_rect = panel.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(panel, panel_rect)
        
        # Dibujar instrucciones con menos espacio entre líneas
        y_offset = panel_rect.top + 30
        for instruction in self.instructions:
            text_surface = self.font.render(instruction, True, COLORS['BLANCO'])
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 50
        
        # Dibujar mensaje de "Presiona ESPACIO"
        start_text = self.font_small.render("PRESIONA ESPACIO PARA COMENZAR", True, COLORS['BLANCO'])
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        start_text.set_alpha(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
        screen.blit(start_text, start_rect) 