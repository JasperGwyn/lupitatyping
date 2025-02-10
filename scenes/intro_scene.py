import pygame
import math
import random
from scenes.scene import Scene
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
import utils.resource_loader as resources

class IntroScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.current_page = 0
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Cargar recursos
        resources.load_all_resources()
        
        # Inicializar fondo común
        self.init_background()
        
        # Preparar a Lupita
        self.wizard = resources.get_image('wizard')
        if self.wizard:
            wizard_height = 150  # Mismo tamaño que en el menú
            wizard_scale = wizard_height / self.wizard.get_height()
            wizard_size = (int(self.wizard.get_width() * wizard_scale), wizard_height)
            self.wizard = pygame.transform.scale(self.wizard, wizard_size)
            # Posicionar a Lupita - Empezamos desde la izquierda
            self.wizard_pos = [-wizard_size[0], SCREEN_HEIGHT//2 - wizard_size[1]//2]
            
            # Posición final en el centro
            self.wizard_target_x = SCREEN_WIDTH//2 - wizard_size[0]//2
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
        
        # Textos de la historia (cortos y simples)
        self.story_texts = [
            "¡HOLA! SOY LUPITA",
            "QUIERO SER UNA GRAN MAGA",
            "¡PERO PRIMERO DEBO APRENDER A TIPEAR!",
            "¿ME AYUDAS?"
        ]
        
        # Variables de animación
        self.fade_alpha = 255  # Solo para el inicio
        self.text_alpha = 0
        self.animation_state = "FADE_IN"
        self.animation_timer = 0
        self.first_fade = True  # Para controlar que solo haya fade al inicio
        
        # Iniciar música de intro
        pygame.mixer.init()
        try:
            pygame.mixer.music.load('assets/sounds/music/intro.mp3')
            pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
            pygame.mixer.music.play(-1)  # -1 para reproducción en loop
        except:
            print("No se pudo cargar la música de intro")
    
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
        if hasattr(self, 'wizard_pos'):
            # Movimiento de entrada suave hasta la posición objetivo
            if self.wizard_pos[0] < self.wizard_target_x:
                self.wizard_pos[0] += 5
            
            # Flotación suave alrededor del centro
            self.wizard_float_offset = (self.wizard_float_offset + 2) % 360
            self.wizard_pos[1] = SCREEN_HEIGHT//2 - self.wizard.get_height()//2 + math.sin(math.radians(self.wizard_float_offset)) * 15
        
        # Manejar las transiciones
        if self.animation_state == "FADE_IN" and self.first_fade:
            self.fade_alpha = max(0, self.fade_alpha - 5)
            if self.fade_alpha == 0:
                self.animation_state = "SHOW_TEXT"
                self.first_fade = False
                
        elif self.animation_state == "SHOW_TEXT":
            self.text_alpha = min(255, self.text_alpha + 10)  # Más rápido
            if self.text_alpha == 255:
                self.animation_state = "WAIT"
                self.animation_timer = tiempo_actual
                
        elif self.animation_state == "WAIT":
            if tiempo_actual - self.animation_timer > 3000:
                self.animation_state = "FADE_OUT"
                
        elif self.animation_state == "FADE_OUT":
            self.text_alpha = max(0, self.text_alpha - 10)  # Más rápido
            if self.text_alpha == 0:
                self.animation_state = "SHOW_TEXT"
                self.current_page += 1
                if self.current_page >= len(self.story_texts):
                    # Ya no detenemos la música aquí
                    self.game.change_scene("menu")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Saltar a la siguiente página
                self.animation_state = "FADE_OUT"
                self.text_alpha = 0
    
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
        
        # Dibujar el texto actual
        if self.current_page < len(self.story_texts):
            text = self.story_texts[self.current_page]
            text_surface = self.font.render(text, True, COLORS['BLANCO'])
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            
            # Agregar sombra al texto
            shadow_surface = self.font.render(text, True, COLORS['NEGRO'])
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            
            # Aplicar transparencia
            text_surface.set_alpha(self.text_alpha)
            shadow_surface.set_alpha(self.text_alpha)
            
            screen.blit(shadow_surface, shadow_rect)
            screen.blit(text_surface, text_rect)
        
        # Dibujar el mensaje de "Presiona ESPACIO"
        if self.animation_state == "WAIT":
            skip_text = self.font_small.render("PRESIONA ESPACIO", True, COLORS['BLANCO'])
            skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            skip_text.set_alpha(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
            screen.blit(skip_text, skip_rect)
        
        # Dibujar el fade solo al inicio
        if self.fade_alpha > 0 and self.first_fade:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill(COLORS['NEGRO'])
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0)) 