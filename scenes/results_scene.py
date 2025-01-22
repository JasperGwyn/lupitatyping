import pygame
from . import Scene
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.leaderboard import Leaderboard

class ResultsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.fuente_grande = pygame.font.Font(None, 64)
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
        self.leaderboard = Leaderboard()
        self.nombre_jugador = ""
        self.esperando_nombre = False
        self.mostrar_cursor = True
        self.tiempo_cursor = 0
        
        # Crear textos
        self.game_over = self.fuente_grande.render("¡Juego Terminado!", True, COLORS['BLANCO'])
        self.reintentar = self.fuente.render("Presiona ESPACIO para jugar de nuevo", True, COLORS['BLANCO'])
        
        # Verificar si es high score
        if hasattr(game.current_scene, 'puntuacion'):
            self.puntuacion = game.current_scene.puntuacion
            self.nivel = game.current_scene.nivel
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
            self.game.change_scene("game")
            
    def update(self):
        # Actualizar el parpadeo del cursor
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_cursor > 500:  # Parpadear cada 500ms
            self.mostrar_cursor = not self.mostrar_cursor
            self.tiempo_cursor = tiempo_actual
        
    def draw(self, screen):
        screen.fill(COLORS['AZUL'])
        
        # Centrar y dibujar "Game Over"
        game_over_rect = self.game_over.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(self.game_over, game_over_rect)
        
        # Mostrar puntuación final
        punt_final = self.fuente.render(f"Puntuación Final: {self.puntuacion}", True, COLORS['BLANCO'])
        nivel_final = self.fuente.render(f"Nivel Alcanzado: {self.nivel}", True, COLORS['BLANCO'])
        screen.blit(punt_final, (SCREEN_WIDTH//2 - punt_final.get_width()//2, 150))
        screen.blit(nivel_final, (SCREEN_WIDTH//2 - nivel_final.get_width()//2, 190))
        
        if self.esperando_nombre:
            # Entrada de nombre
            texto_nombre = self.fuente.render("Nuevo High Score! Ingresa tu nombre:", True, COLORS['BLANCO'])
            nombre = self.nombre_jugador + ('|' if self.mostrar_cursor else '')
            input_nombre = self.fuente.render(nombre, True, COLORS['BLANCO'])
            screen.blit(texto_nombre, (SCREEN_WIDTH//2 - texto_nombre.get_width()//2, 250))
            screen.blit(input_nombre, (SCREEN_WIDTH//2 - input_nombre.get_width()//2, 290))
        else:
            # Mostrar leaderboard
            titulo_lb = self.fuente.render("Mejores Puntajes", True, COLORS['BLANCO'])
            screen.blit(titulo_lb, (SCREEN_WIDTH//2 - titulo_lb.get_width()//2, 250))
            
            y = 290
            for i, score in enumerate(self.leaderboard.scores):
                texto = f"{i+1}. {score['name']}: {score['score']} (Nivel {score['nivel']})"
                color = COLORS['VERDE'] if score['score'] == self.puntuacion else COLORS['BLANCO']
                score_surface = self.fuente_pequeña.render(texto, True, color)
                screen.blit(score_surface, (SCREEN_WIDTH//2 - score_surface.get_width()//2, y))
                y += 30
            
            # Dibujar mensaje para reintentar
            reintentar_rect = self.reintentar.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            screen.blit(self.reintentar, reintentar_rect) 