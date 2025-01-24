import pygame
from config import SCREEN_HEIGHT, COLORS, TECLAS_POR_DEDO

class Word:
    def __init__(self, texto, x, velocidad):
        self.texto = texto
        self.x = x
        self.y = 0
        self.velocidad = velocidad
        self.explotada = False
        self.acertada = False  # Nuevo estado para palabras correctamente escritas
        self.area_limite = 0
        self.fuente = pygame.font.Font(None, 36)
        
        # Preparar la superficie de renderizado
        self.surface = self.fuente.render(self.texto, True, COLORS['BLANCO'])
        
    def update(self):
        """Actualiza la posición de la palabra"""
        if not self.explotada and not self.acertada:  # Solo mover si no está explotada ni acertada
            self.y += self.velocidad
            
            # Verificar si ha tocado la línea límite
            altura_texto = self.surface.get_height()
            if self.y + altura_texto >= self.area_limite:
                self.explotada = True
        
    def draw(self, screen):
        """Dibuja la palabra en la pantalla"""
        if not self.explotada and not self.acertada:  # Solo dibujar si no está explotada ni acertada
            screen.blit(self.surface, (self.x, self.y))
            
    def check_match(self, texto_usuario):
        """Verifica si el texto ingresado coincide con esta palabra"""
        if self.texto.upper() == texto_usuario.upper():
            self.acertada = True  # Marcar como acertada en lugar de explotada
            return True
        return False 