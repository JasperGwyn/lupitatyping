import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from scenes.scene import Scene
import utils.resource_loader as resources
from utils.leaderboard import Leaderboard

class ResultsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 48)
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
            # Inicializar variables para el movimiento
            self.wizard_angle_x = 0
            self.wizard_angle_y = 0
            self.wizard_speed_x = 0.5  # Velocidad más lenta
            self.wizard_speed_y = 0.7  # Velocidad ligeramente diferente para crear patrón
            self.wizard_radius_x = SCREEN_WIDTH//4  # Radio horizontal
            self.wizard_radius_y = SCREEN_HEIGHT//4  # Radio vertical
            self.wizard_center = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
            self.wizard_float_offset = 0
            # Calcular posición inicial
            self.wizard_pos = [
                self.wizard_center[0] + math.sin(math.radians(self.wizard_angle_x)) * self.wizard_radius_x - wizard_size[0]//2,
                self.wizard_center[1] + math.sin(math.radians(self.wizard_angle_y)) * self.wizard_radius_y - wizard_size[1]//2
            ]
        
        # Iniciar música de fin de juego
        try:
            pygame.mixer.music.load('assets/sounds/music/endmusic.mp3')
            pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
            pygame.mixer.music.play(-1)  # -1 para reproducción en loop
        except Exception as e:
            print(f"No se pudo cargar la música de fin de juego: {e}")
        
        self.leaderboard = Leaderboard()
        self.nombre_jugador = ""
        self.esperando_nombre = False
        self.mostrar_cursor = True
        self.tiempo_cursor = 0
        
        # Crear textos
        self.game_over = self.font.render("¡JUEGO TERMINADO!", True, COLORS['BLANCO'])
        self.reintentar = self.font_small.render("PRESIONA ESPACIO PARA JUGAR DE NUEVO", True, COLORS['BLANCO'])
        
        # Obtener puntuación y nivel del juego anterior
        self.puntuacion = getattr(game, 'puntuacion', 0)
        self.nivel = getattr(game, 'nivel', 1)
        self.es_high_score = self.leaderboard.is_high_score(self.puntuacion)
        if self.es_high_score:
            self.esperando_nombre = True
        
    def handle_event(self, event):
        if self.esperando_nombre:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.nombre_jugador:
                    # Guardar el puntaje y desactivar la entrada de nombre
                    self.leaderboard.add_score(self.nombre_jugador, self.puntuacion, self.nivel)
                    self.esperando_nombre = False
                elif event.key == pygame.K_BACKSPACE:
                    self.nombre_jugador = self.nombre_jugador[:-1]
                elif event.unicode.isalnum() and len(self.nombre_jugador) < 10:
                    self.nombre_jugador += event.unicode
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Detener la música antes de reiniciar el juego
            pygame.mixer.music.stop()
            self.game.change_scene("menu")
            
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Actualizar fondo común
        self.update_background()
        
        # Animar a Lupita con movimiento tipo Lissajous
        self.wizard_angle_x = (self.wizard_angle_x + self.wizard_speed_x) % 360
        self.wizard_angle_y = (self.wizard_angle_y + self.wizard_speed_y) % 360
        self.wizard_float_offset = (self.wizard_float_offset + 1) % 360
        
        # Calcular nueva posición con movimiento más orgánico
        base_x = self.wizard_center[0] + math.sin(math.radians(self.wizard_angle_x)) * self.wizard_radius_x - self.wizard.get_width()//2
        base_y = self.wizard_center[1] + math.sin(math.radians(self.wizard_angle_y * 1.5)) * self.wizard_radius_y - self.wizard.get_height()//2
        
        # Agregar movimiento flotante suave
        float_offset = math.sin(math.radians(self.wizard_float_offset)) * 10
        
        self.wizard_pos = [base_x, base_y + float_offset]
        
        # Actualizar el parpadeo del cursor
        if tiempo_actual - self.tiempo_cursor > 500:
            self.mostrar_cursor = not self.mostrar_cursor
            self.tiempo_cursor = tiempo_actual
        
    def draw(self, screen):
        # Dibujar fondo común
        self.draw_background(screen)
        
        # Dibujar a Lupita
        if hasattr(self, 'wizard'):
            screen.blit(self.wizard, self.wizard_pos)
        
        # Dibujar "Game Over" y puntuación final (más arriba)
        game_over_rect = self.game_over.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(self.game_over, game_over_rect)
        
        punt_final = self.font_small.render(f"PUNTUACIÓN FINAL: {self.puntuacion}", True, COLORS['BLANCO'])
        nivel_final = self.font_small.render(f"NIVEL ALCANZADO: {self.nivel}", True, COLORS['BLANCO'])
        screen.blit(punt_final, (SCREEN_WIDTH//2 - punt_final.get_width()//2, 100))
        screen.blit(nivel_final, (SCREEN_WIDTH//2 - nivel_final.get_width()//2, 140))
        
        # Panel semi-transparente
        panel = pygame.Surface((SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5))
        panel.fill(COLORS['NEGRO'])
        panel.set_alpha(128)
        panel_rect = panel.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(panel, panel_rect)
        
        if self.esperando_nombre:
            # Solo mostrar la entrada de nombre en dos líneas
            texto_nombre1 = self.font_small.render("¡NUEVO HIGH SCORE!", True, COLORS['AMARILLO'])
            texto_nombre2 = self.font_small.render("INGRESA TU NOMBRE:", True, COLORS['AMARILLO'])
            nombre = self.nombre_jugador + ('|' if self.mostrar_cursor else '')
            input_nombre = self.font_small.render(nombre, True, COLORS['BLANCO'])
            
            # Centrar los textos en el panel
            screen.blit(texto_nombre1, (SCREEN_WIDTH//2 - texto_nombre1.get_width()//2, panel_rect.top + panel_rect.height//2 - 60))
            screen.blit(texto_nombre2, (SCREEN_WIDTH//2 - texto_nombre2.get_width()//2, panel_rect.top + panel_rect.height//2 - 20))
            screen.blit(input_nombre, (SCREEN_WIDTH//2 - input_nombre.get_width()//2, panel_rect.top + panel_rect.height//2 + 20))
        else:
            # Mostrar leaderboard
            title = self.font.render("MEJORES PUNTAJES", True, COLORS['BLANCO'])
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, panel_rect.top + 40))
            screen.blit(title, title_rect)
            
            # Mostrar puntajes
            y_offset = panel_rect.top + 100
            for i, score in enumerate(self.leaderboard.scores[:5]):
                text = f"{i+1}. {score['name']}: {score['score']} (Nivel {score['nivel']})"
                color = COLORS['VERDE'] if hasattr(self, 'puntuacion') and score['score'] == self.puntuacion else COLORS['BLANCO']
                score_surface = self.font_small.render(text, True, color)
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                screen.blit(score_surface, score_rect)
                y_offset += 40
        
        # Mensaje para volver al menú
        back_text = self.font_small.render("PRESIONA ESPACIO PARA VOLVER AL MENÚ", True, COLORS['BLANCO'])
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        back_text.set_alpha(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
        screen.blit(back_text, back_rect) 