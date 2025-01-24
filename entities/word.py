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
        
        # Asignar colores a cada letra según el dedo que debe usarla
        self.colores_letras = []
        for letra in texto:
            color = COLORS['BLANCO']  # Color por defecto
            for dedo, teclas in TECLAS_POR_DEDO.items():
                if letra.upper() in teclas:
                    color = COLORS[dedo]
                    break
            self.colores_letras.append(color)
        
    def update(self):
        """Actualiza la posición de la palabra"""
        if not self.explotada and not self.acertada:  # Solo mover si no está explotada ni acertada
            self.y += self.velocidad
            
            # Verificar si ha tocado la línea límite
            altura_texto = self.fuente.size(self.texto)[1]
            if self.y + altura_texto >= self.area_limite:
                self.explotada = True
        
    def draw(self, screen):
        """Dibuja la palabra en la pantalla"""
        if not self.explotada and not self.acertada:  # Solo dibujar si no está explotada ni acertada
            # Dibujar cada letra con su color correspondiente
            x_offset = self.x
            for i, letra in enumerate(self.texto):
                letra_surface = self.fuente.render(letra, True, self.colores_letras[i])
                screen.blit(letra_surface, (x_offset, self.y))
                # Aumentamos el offset según el ancho de la letra
                x_offset += self.fuente.size(letra)[0]
            
    def check_match(self, texto_usuario):
        """Verifica si el texto ingresado coincide con esta palabra"""
        if self.texto.upper() == texto_usuario.upper():
            self.acertada = True  # Marcar como acertada en lugar de explotada
            return True
        return False 