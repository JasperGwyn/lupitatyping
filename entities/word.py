import pygame
from config import SCREEN_HEIGHT, COLORS, TECLAS_POR_DEDO

class Word:
    def __init__(self, texto, x, velocidad):
        self.texto = texto
        self.x = x
        self.y = 0  # Empieza desde arriba
        self.velocidad = velocidad
        self.fuente = pygame.font.Font(None, 36)
        self.activa = True
        self.area_limite = SCREEN_HEIGHT  # Por defecto, usa toda la pantalla
        
        # Asignar colores a cada letra según el dedo que debe usarla
        self.colores_letras = []
        for letra in texto:
            color = COLORS['NEGRO']  # Color por defecto
            for dedo, teclas in TECLAS_POR_DEDO.items():
                if letra in teclas:
                    color = COLORS[dedo]
                    break
            self.colores_letras.append(color)
        
    def update(self):
        if self.activa:
            self.y += self.velocidad
            # Si la palabra sale del área de juego, la desactivamos
            if self.y > self.area_limite:
                self.activa = False
                
    def draw(self, screen):
        if self.activa:
            # Dibujamos cada letra con su color correspondiente
            x_offset = self.x
            for i, letra in enumerate(self.texto):
                letra_surface = self.fuente.render(letra, True, self.colores_letras[i])
                screen.blit(letra_surface, (x_offset, self.y))
                # Aumentamos el offset según el ancho de la letra
                x_offset += self.fuente.size(letra)[0]
            
    def check_match(self, texto_usuario):
        """Verifica si el texto del usuario coincide con esta palabra"""
        if self.activa and texto_usuario == self.texto:
            self.activa = False
            return True
        return False 