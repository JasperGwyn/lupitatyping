import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lupita's Typing Adventure")

# Colores
ROSA = (255, 192, 203)
AZUL = (100, 149, 237)
VERDE = (144, 238, 144)

# Palabras por nivel
palabras_nivel1 = ['A', 'B', 'C', 'D', 'E']
palabras_nivel2 = ['SOL', 'LUZ', 'MAR', 'OSO']
palabras_nivel3 = ['GATO', 'PERRO', 'CASA', 'LUNA']

class Palabra:
    def __init__(self, texto, x, velocidad):
        self.texto = texto
        self.x = x
        self.y = 0
        self.velocidad = velocidad
        self.fuente = pygame.font.Font(None, 36)
        
    def dibujar(self, superficie):
        texto_render = self.fuente.render(self.texto, True, AZUL)
        superficie.blit(texto_render, (self.x, self.y))
        
    def mover(self):
        self.y += self.velocidad

def main():
    reloj = pygame.time.Clock()
    palabra_actual = None
    texto_usuario = ""
    puntuacion = 0
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_usuario == palabra_actual.texto:
                        puntuacion += 10
                    texto_usuario = ""
                elif evento.key == pygame.K_BACKSPACE:
                    texto_usuario = texto_usuario[:-1]
                else:
                    texto_usuario += evento.unicode
        
        # Lógica del juego aquí
        
        # Dibujar
        pantalla.fill(ROSA)
        # Más código de dibujo aquí
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main() 