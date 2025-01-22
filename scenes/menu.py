import pygame
from . import Scene
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 64)
        self.title = self.font.render("Lupita's Typing Adventure", True, COLORS['AZUL'])
        self.start_text = pygame.font.Font(None, 36).render("Presiona ESPACIO para comenzar", True, COLORS['NEGRO'])
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_scene("game")
            
    def draw(self, screen):
        screen.fill(COLORS['ROSA'])
        
        # Centrar título
        title_rect = self.title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        screen.blit(self.title, title_rect)
        
        # Centrar texto de inicio
        start_rect = self.start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3))
        screen.blit(self.start_text, start_rect) 