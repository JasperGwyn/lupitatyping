import pygame
import random
from . import Scene
from config import (COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_CONFIG, 
                   PALABRAS_POR_NIVEL, TECLAS_POR_DEDO, GAME_CONFIG,
                   INCREMENTO_VELOCIDAD, INCREMENTO_FRECUENCIA)
from entities.word import Word
from entities.animation import FallingAnimation, ExplosionAnimation

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.palabras = []
        self.animaciones = []
        self.texto_usuario = ""
        self.puntuacion = 0
        self.nivel = 1
        self.palabras_acertadas = 0
        self.vidas = GAME_CONFIG['VIDAS_INICIALES']
        self.tiempo_ultimo_spawn = 0
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        self.multiplicador_velocidad = 1.0  # Factor de velocidad inicial
        self.multiplicador_frecuencia = 1.0  # Factor de frecuencia inicial
        
        # Definir área de juego
        self.area_juego_height = SCREEN_HEIGHT - 180  # Dejar espacio para el teclado
        
        # Cargar palabras del nivel actual
        self.palabras_disponibles = PALABRAS_POR_NIVEL[self.nivel]['palabras']
        
    def dibujar_vidas(self, screen):
        """Dibuja los corazones que representan las vidas"""
        x = SCREEN_WIDTH - 40
        y = 10
        for i in range(self.vidas):
            # Dibujamos un corazón más elaborado
            # Círculo izquierdo del corazón
            pygame.draw.circle(screen, COLORS['ROJO'], (x-4, y+6), 6)
            # Círculo derecho del corazón
            pygame.draw.circle(screen, COLORS['ROJO'], (x+4, y+6), 6)
            # Triángulo inferior
            puntos = [
                (x-8, y+6),
                (x+8, y+6),
                (x, y+20)
            ]
            pygame.draw.polygon(screen, COLORS['ROJO'], puntos)
            x -= 35  # Más espacio entre corazones
        
    def dibujar_area_juego(self, screen):
        """Dibuja una línea que separa el área de juego del teclado"""
        pygame.draw.line(screen, COLORS['NEGRO'], 
                        (0, self.area_juego_height), 
                        (SCREEN_WIDTH, self.area_juego_height), 2)
        
    def perder_vida(self, palabra):
        """Maneja la pérdida de una vida"""
        self.vidas -= 1
        # Crear animación de explosión
        self.animaciones.append(ExplosionAnimation(palabra.x, palabra.y, palabra.texto))
        if self.vidas <= 0:
            self.game.change_scene("results")
        
    def dibujar_teclado(self, screen):
        """Dibuja una representación simple del teclado con colores por dedo"""
        # Definimos las teclas que queremos mostrar y su posición
        teclas = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        
        # Tamaño y posición del teclado
        tecla_size = 30
        espacio = 5
        start_y = SCREEN_HEIGHT - 120
        
        # Dibujamos cada fila de teclas
        for row_idx, row in enumerate(teclas):
            # Centramos cada fila
            total_width = len(row) * (tecla_size + espacio)
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            for col_idx, tecla in enumerate(row):
                x = start_x + col_idx * (tecla_size + espacio)
                y = start_y + row_idx * (tecla_size + espacio)
                
                # Encontrar el color correspondiente al dedo
                color = COLORS['NEGRO']
                for dedo, teclas_dedo in TECLAS_POR_DEDO.items():
                    if tecla in teclas_dedo:
                        color = COLORS[dedo]
                        break
                
                # Dibujar la tecla
                pygame.draw.rect(screen, color, (x, y, tecla_size, tecla_size))
                texto = self.fuente_pequeña.render(tecla, True, COLORS['BLANCO'])
                texto_rect = texto.get_rect(center=(x + tecla_size//2, y + tecla_size//2))
                screen.blit(texto, texto_rect)
        
    def spawn_palabra(self):
        """Crea una nueva palabra en una posición aleatoria"""
        config = LEVEL_CONFIG[self.nivel]
        palabra = random.choice(self.palabras_disponibles)
        x = random.randint(50, SCREEN_WIDTH - 100)
        # Aplicar el multiplicador de velocidad
        velocidad_ajustada = config['velocidad_palabras'] * self.multiplicador_velocidad
        nueva_palabra = Word(palabra, x, velocidad_ajustada)
        nueva_palabra.area_limite = self.area_juego_height
        self.palabras.append(nueva_palabra)
        
    def get_tiempo_spawn_actual(self):
        """Calcula el tiempo de spawn actual basado en el nivel y multiplicador"""
        tiempo_base = LEVEL_CONFIG[self.nivel]['tiempo_spawn']
        return int(tiempo_base / self.multiplicador_frecuencia)
        
    def check_nivel_completo(self):
        """Verifica si se debe avanzar al siguiente nivel"""
        if self.palabras_acertadas >= LEVEL_CONFIG[self.nivel]['palabras_para_pasar']:
            if self.nivel < len(LEVEL_CONFIG):
                self.nivel += 1
                self.palabras_acertadas = 0
                self.palabras_disponibles = PALABRAS_POR_NIVEL[self.nivel]['palabras']
                # Resetear los multiplicadores al cambiar de nivel
                self.multiplicador_velocidad = 1.0
                self.multiplicador_frecuencia = 1.0
                return True
        return False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Verificar si alguna palabra coincide
                for palabra in self.palabras:
                    if palabra.check_match(self.texto_usuario):
                        self.puntuacion += LEVEL_CONFIG[self.nivel]['puntos_palabra']
                        self.palabras_acertadas += 1
                        # Incrementar velocidad y frecuencia
                        self.multiplicador_velocidad *= INCREMENTO_VELOCIDAD
                        self.multiplicador_frecuencia *= INCREMENTO_FRECUENCIA
                        self.check_nivel_completo()
                self.texto_usuario = ""
            elif event.key == pygame.K_BACKSPACE:
                self.texto_usuario = self.texto_usuario[:-1]
            else:
                # Solo aceptamos letras
                if event.unicode.isalpha():
                    self.texto_usuario += event.unicode.upper()
                    
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Crear nuevas palabras si:
        # 1. Ha pasado el tiempo suficiente, o
        # 2. No hay palabras activas en pantalla
        if (tiempo_actual - self.tiempo_ultimo_spawn > self.get_tiempo_spawn_actual()) or \
           (len(self.palabras) == 0):
            self.spawn_palabra()
            self.tiempo_ultimo_spawn = tiempo_actual
            
        # Actualizar posición de palabras y verificar si alguna llegó al fondo
        for palabra in self.palabras:
            palabra.update()
            if not palabra.activa and palabra.y >= self.area_juego_height:
                self.perder_vida(palabra)
            
        # Actualizar animaciones
        for animacion in self.animaciones:
            animacion.update()
            
        # Limpiar palabras inactivas y animaciones terminadas
        self.palabras = [p for p in self.palabras if p.activa]
        self.animaciones = [a for a in self.animaciones if a.activa]
        
    def draw(self, screen):
        screen.fill(COLORS['BLANCO'])
        
        # Dibujar el área de juego
        self.dibujar_area_juego(screen)
        
        # Dibujar palabras
        for palabra in self.palabras:
            palabra.draw(screen)
            
        # Dibujar animaciones
        for animacion in self.animaciones:
            animacion.draw(screen)
            
        # Dibujar texto del usuario
        texto_surface = self.fuente.render(f"> {self.texto_usuario}", True, COLORS['AZUL'])
        screen.blit(texto_surface, (10, self.area_juego_height + 10))
        
        # Dibujar puntuación, nivel y multiplicadores
        punt_surface = self.fuente.render(f"Puntos: {self.puntuacion}", True, COLORS['NEGRO'])
        nivel_surface = self.fuente.render(f"Nivel {self.nivel}: {PALABRAS_POR_NIVEL[self.nivel]['descripcion']}", True, COLORS['NEGRO'])
        progreso_surface = self.fuente.render(f"Palabras: {self.palabras_acertadas}/{LEVEL_CONFIG[self.nivel]['palabras_para_pasar']}", True, COLORS['NEGRO'])
        velocidad_surface = self.fuente.render(f"Velocidad: x{self.multiplicador_velocidad:.1f}", True, COLORS['NEGRO'])
        frecuencia_surface = self.fuente.render(f"Frecuencia: x{self.multiplicador_frecuencia:.1f}", True, COLORS['NEGRO'])
        
        screen.blit(punt_surface, (10, 10))
        screen.blit(nivel_surface, (10, 40))
        screen.blit(progreso_surface, (10, 70))
        screen.blit(velocidad_surface, (10, 100))
        screen.blit(frecuencia_surface, (10, 130))
        
        # Dibujar vidas
        self.dibujar_vidas(screen)
        
        # Dibujar el teclado
        self.dibujar_teclado(screen) 