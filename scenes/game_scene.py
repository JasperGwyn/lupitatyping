import pygame
import random
import math
import os
from . import Scene
from config import (COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_CONFIG, 
                   PALABRAS_POR_NIVEL, TECLAS_POR_DEDO, GAME_CONFIG,
                   INCREMENTO_VELOCIDAD, INCREMENTO_FRECUENCIA)
from entities.word import Word
from entities.animation import FallingAnimation, ExplosionAnimation
import utils.resource_loader as resources

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
        self.multiplicador_velocidad = 1.0
        self.multiplicador_frecuencia = 1.0
        
        # Definir área de juego (ajustada para dejar espacio al teclado)
        self.area_juego_height = SCREEN_HEIGHT - 180
        
        # Variables para el efecto de parpadeo del nivel
        self.nivel_cambio_tiempo = 0
        self.nivel_efecto_duracion = 2000  # 2 segundos de efecto
        self.nivel_anterior = 1
        
        # Configuración de música y sonidos
        self.cargar_musica_nivel(self.nivel)
            
        self.sonido_acierto = pygame.mixer.Sound('assets/sounds/effects/powerUp2.ogg')
        self.sonido_acierto.set_volume(0.3)  # Volumen al 30% para no opacar la música
        self.sonido_error = pygame.mixer.Sound('assets/sounds/effects/lowThreeTone.ogg')
        self.sonido_error.set_volume(0.3)
        self.sonido_explosion = pygame.mixer.Sound('assets/sounds/effects/sfx_explosionGoo.ogg')
        self.sonido_explosion.set_volume(0.4)  # Un poco más alto que los otros efectos
        
        # Cargar y preparar recursos visuales
        resources.load_all_resources()
        
        # Preparar el castillo de fondo
        self.castle = resources.get_image('castle')
        if self.castle:
            castle_height = SCREEN_HEIGHT // 2  # Mismo tamaño que en el menú
            castle_scale = castle_height / self.castle.get_height()
            new_size = (int(self.castle.get_width() * castle_scale), castle_height)
            self.castle = pygame.transform.scale(self.castle, new_size)
            # Posicionar el castillo justo sobre la línea de explosión
            self.castle_pos = (SCREEN_WIDTH//2 - new_size[0]//2, self.area_juego_height - new_size[1])
        
        # Preparar nubes decorativas
        self.clouds = []
        cloud = resources.get_image('cloud1')
        if cloud:
            for _ in range(3):
                cloud_size = (random.randint(100, 150), random.randint(50, 75))
                cloud_scaled = pygame.transform.scale(cloud, cloud_size)
                self.clouds.append({
                    'surface': cloud_scaled,
                    'pos': [random.randint(0, SCREEN_WIDTH), random.randint(50, 150)],
                    'speed': random.uniform(0.2, 0.5)
                })
        
        # Inicializar partículas mágicas
        self.particles = []
        for _ in range(20):
            self.particles.append({
                'pos': [random.randint(0, SCREEN_WIDTH), random.randint(0, self.area_juego_height)],
                'speed': random.uniform(0.5, 1.5),
                'size': random.randint(2, 4),
                'alpha': random.randint(50, 200)
            })
        
        # Cargar palabras del nivel actual
        self.palabras_disponibles = PALABRAS_POR_NIVEL[self.nivel]['palabras']
        
        # Preparar a Lupita para el gameplay
        self.wizard = resources.get_image('wizard')
        if self.wizard:
            wizard_height = 120  # Un poco más pequeña que en el menú
            wizard_scale = wizard_height / self.wizard.get_height()
            wizard_size = (int(self.wizard.get_width() * wizard_scale), wizard_height)
            self.wizard = pygame.transform.scale(self.wizard, wizard_size)
            self.wizard_pos = [SCREEN_WIDTH - wizard_size[0] - 20, SCREEN_HEIGHT - wizard_size[1] - 50]
            self.wizard_float_offset = 0
        
        # Variables para la secuencia de Game Over
        self.game_over = False
        self.game_over_timer = 0
        self.game_over_duration = 3000  # 3 segundos
        self.game_over_text = self.fuente.render("¡GAME OVER!", True, COLORS['ROJO'])
        self.game_over_alpha = 0
        
        # Preparar árboles
        self.trees = []
        tree_img = resources.get_image('tree1')
        if tree_img:
            tree_height = 200
            tree_scale = tree_height / tree_img.get_height()
            tree_size = (int(tree_img.get_width() * tree_scale), tree_height)
            tree_scaled = pygame.transform.scale(tree_img, tree_size)
            # Árbol a 5% desde la izquierda
            self.trees.append({
                'surface': tree_scaled,
                'pos': (int(SCREEN_WIDTH * 0.05), self.area_juego_height - tree_size[1])
            })
        
        tree_img = resources.get_image('tree2')
        if tree_img:
            tree_height = 200
            tree_scale = tree_height / tree_img.get_height()
            tree_size = (int(tree_img.get_width() * tree_scale), tree_height)
            tree_scaled = pygame.transform.scale(tree_img, tree_size)
            # Árbol a 20% desde la derecha
            self.trees.append({
                'surface': tree_scaled,
                'pos': (int(SCREEN_WIDTH * 0.8), self.area_juego_height - tree_size[1])
            })
        
    def cargar_musica_nivel(self, nivel):
        """Carga la música correspondiente al nivel actual"""
        # Lista de posibles extensiones a probar
        extensiones = ['ogg', 'opus', 'mp3']
        
        for ext in extensiones:
            try:
                archivo_musica = f'assets/sounds/music/game_theme_nivel{nivel}.{ext}'
                if os.path.exists(archivo_musica):
                    pygame.mixer.music.load(archivo_musica)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print(f"Música del nivel {nivel} cargada correctamente")
                    return
            except Exception as e:
                print(f"Error al cargar {archivo_musica}: {str(e)}")
        
        print(f"No se pudo cargar la música del nivel {nivel}")
        # Si falla todo, intentar cargar la música base
        try:
            pygame.mixer.music.load('assets/sounds/music/game_theme.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("No se pudo cargar la música base del juego")
        
    def dibujar_vidas(self, screen):
        """Dibuja los corazones que representan las vidas"""
        heart = resources.get_image('heart')
        if heart:
            # Escalar el corazón a un tamaño apropiado
            heart_size = (30, 30)
            heart_scaled = pygame.transform.scale(heart, heart_size)
            
            # Dibujar los corazones
            x = SCREEN_WIDTH - 40
            y = 10
            for i in range(self.vidas):
                screen.blit(heart_scaled, (x - heart_size[0]//2, y))
                x -= 35  # Espacio entre corazones
        
    def dibujar_area_juego(self, screen):
        """Dibuja una línea mágica que separa el área de juego del teclado y el suelo"""
        # Dibujar el suelo (área debajo de la línea)
        suelo = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - self.area_juego_height))
        suelo.fill((50, 30, 10))  # Color marrón oscuro para el suelo
        screen.blit(suelo, (0, self.area_juego_height))
        
        # Dibujar línea base con degradado en rojo
        for i in range(5):  # Grosor de la línea
            alpha = 255 - (i * 40)  # Degradado de opacidad
            pygame.draw.line(screen, (255, 0, 0, alpha), 
                           (0, self.area_juego_height + i), 
                           (SCREEN_WIDTH, self.area_juego_height + i), 1)
        
        # Agregar brillos mágicos a lo largo de la línea
        tiempo = pygame.time.get_ticks()
        for x in range(0, SCREEN_WIDTH, 50):  # Cada 50 píxeles
            offset = math.sin(tiempo * 0.003 + x * 0.1) * 3  # Movimiento ondulante
            brillo_size = 4 + math.sin(tiempo * 0.005 + x * 0.05) * 2  # Tamaño variable
            
            # Dibujar brillo
            pygame.draw.circle(screen, (255, 100, 100), 
                             (x, int(self.area_juego_height + offset)), 
                             int(brillo_size))
            
            # Agregar destello alrededor del brillo
            destello = pygame.Surface((brillo_size * 4, brillo_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(destello, (255, 0, 0, 128), 
                             (brillo_size * 2, brillo_size * 2), brillo_size * 2)
            screen.blit(destello, (x - brillo_size * 2, 
                                 int(self.area_juego_height + offset - brillo_size * 2)))
        
    def perder_vida(self, palabra):
        """Maneja la pérdida de una vida"""
        self.vidas -= 1
        self.sonido_explosion.play()
        # Crear animación de explosión
        self.animaciones.append(ExplosionAnimation(palabra.x, palabra.y, palabra.texto))
        
        if self.vidas <= 0 and not self.game_over:
            self.game_over = True
            self.game_over_timer = pygame.time.get_ticks()
            # La transición a la escena de resultados se manejará en el update
            # cuando termine la animación de Game Over
        
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
        
        # Obtener las palabras que ya están en pantalla
        palabras_activas = set(palabra.texto for palabra in self.palabras)
        
        # Filtrar las palabras disponibles para excluir las que ya están en pantalla
        palabras_disponibles = [p for p in self.palabras_disponibles if p not in palabras_activas]
        
        # Si no hay palabras disponibles (todas están en pantalla), esperar
        if not palabras_disponibles:
            return
            
        palabra = random.choice(palabras_disponibles)
        x = random.randint(50, SCREEN_WIDTH - 100)
        # Aplicar el multiplicador de velocidad
        velocidad_ajustada = config['velocidad_palabras'] * self.multiplicador_velocidad
        nueva_palabra = Word(palabra, x, velocidad_ajustada)
        nueva_palabra.area_limite = self.area_juego_height  # Establecer el área límite
        self.palabras.append(nueva_palabra)
        
    def get_tiempo_spawn_actual(self):
        """Calcula el tiempo de spawn actual basado en el nivel y multiplicador"""
        tiempo_base = LEVEL_CONFIG[self.nivel]['tiempo_spawn']
        return int(tiempo_base / self.multiplicador_frecuencia)
        
    def check_nivel_completo(self):
        """Verifica si se debe avanzar al siguiente nivel"""
        if self.palabras_acertadas >= LEVEL_CONFIG[self.nivel]['palabras_para_pasar']:
            if self.nivel < len(LEVEL_CONFIG):
                self.nivel_anterior = self.nivel
                self.nivel += 1
                self.palabras_acertadas = 0
                self.palabras_disponibles = PALABRAS_POR_NIVEL[self.nivel]['palabras']
                # Resetear los multiplicadores al cambiar de nivel
                self.multiplicador_velocidad = 1.0
                self.multiplicador_frecuencia = 1.0
                # Iniciar efecto de parpadeo
                self.nivel_cambio_tiempo = pygame.time.get_ticks()
                # Cargar la música del nuevo nivel
                self.cargar_musica_nivel(self.nivel)
                return True
        return False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Verificar si alguna palabra coincide
                palabra_acertada = False
                for palabra in self.palabras:
                    if palabra.check_match(self.texto_usuario):
                        palabra_acertada = True
                        # Reproducir sonido de acierto
                        self.sonido_acierto.play()
                        self.puntuacion += LEVEL_CONFIG[self.nivel]['puntos_palabra']
                        self.palabras_acertadas += 1
                        # Incrementar velocidad y frecuencia
                        self.multiplicador_velocidad *= INCREMENTO_VELOCIDAD
                        self.multiplicador_frecuencia *= INCREMENTO_FRECUENCIA
                        self.check_nivel_completo()
                        break
                
                if not palabra_acertada and self.texto_usuario:  # Solo reproducir error si escribió algo
                    self.sonido_error.play()
                
                self.texto_usuario = ""
            elif event.key == pygame.K_BACKSPACE:
                self.texto_usuario = self.texto_usuario[:-1]
            else:
                # Solo aceptamos letras
                if event.unicode.isalpha():
                    self.texto_usuario += event.unicode.upper()
                    
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Si estamos en Game Over, manejar la transición
        if self.game_over:
            tiempo_transcurrido = tiempo_actual - self.game_over_timer
            if tiempo_transcurrido < self.game_over_duration:
                # Aumentar la opacidad gradualmente
                self.game_over_alpha = min(255, int((tiempo_transcurrido / 1000) * 255))
            else:
                self.game.change_scene("results")
                return
        
        # Actualizar nubes
        for cloud in self.clouds:
            cloud['pos'][0] += cloud['speed']
            if cloud['pos'][0] > SCREEN_WIDTH:
                cloud['pos'][0] = -cloud['surface'].get_width()
        
        # Actualizar partículas
        for p in self.particles:
            p['pos'][1] += p['speed']
            if p['pos'][1] > self.area_juego_height:
                p['pos'][1] = 0
                p['pos'][0] = random.randint(0, SCREEN_WIDTH)
            p['alpha'] = 128 + int(math.sin(tiempo_actual * 0.001 + p['pos'][1] * 0.1) * 127)
        
        # Actualizar palabras y verificar colisiones
        for palabra in self.palabras[:]:  # Usamos una copia de la lista para poder modificarla
            palabra.update()
            if palabra.explotada:
                self.perder_vida(palabra)
                self.palabras.remove(palabra)
            elif palabra.acertada:  # Nuevo: manejar palabras acertadas
                self.palabras.remove(palabra)
        
        # Actualizar animaciones
        for animacion in self.animaciones[:]:
            animacion.update()
            if animacion.terminada:
                self.animaciones.remove(animacion)
        
        # Generar nuevas palabras
        if tiempo_actual - self.tiempo_ultimo_spawn > self.get_tiempo_spawn_actual():
            self.spawn_palabra()
            self.tiempo_ultimo_spawn = tiempo_actual
            
        # Animar flotación de Lupita
        if hasattr(self, 'wizard_float_offset'):
            self.wizard_float_offset = (self.wizard_float_offset + 2) % 360
            self.wizard_pos[1] = SCREEN_HEIGHT - self.wizard.get_height() - 50 + math.sin(math.radians(self.wizard_float_offset)) * 10
        
    def draw(self, screen):
        # Dibujar fondo
        screen.fill((100, 149, 237))  # Azul real más oscuro para el cielo
        
        # Dibujar nubes
        for cloud in self.clouds:
            screen.blit(cloud['surface'], cloud['pos'])
        
        # Dibujar árboles de fondo
        for tree in self.trees:
            screen.blit(tree['surface'], tree['pos'])
        
        # Dibujar castillo
        if hasattr(self, 'castle'):
            screen.blit(self.castle, self.castle_pos)
        
        # Dibujar partículas mágicas
        for p in self.particles:
            surf = pygame.Surface((p['size'], p['size']))
            surf.fill(COLORS['BLANCO'])
            surf.set_alpha(p['alpha'])
            screen.blit(surf, p['pos'])
        
        # Dibujar el área de juego
        self.dibujar_area_juego(screen)
        
        # Dibujar palabras
        for palabra in self.palabras:
            palabra.draw(screen)
            
        # Dibujar animaciones
        for animacion in self.animaciones:
            animacion.draw(screen)
            
        # Dibujar el teclado
        self.dibujar_teclado(screen)
        
        # Dibujar a Lupita
        if hasattr(self, 'wizard'):
            screen.blit(self.wizard, self.wizard_pos)
            
        # Dibujar interfaz
        self.dibujar_interfaz(screen)
        
        # Si estamos en Game Over, dibujar el texto
        if self.game_over:
            # Crear una copia del texto con la opacidad actual
            texto_con_alpha = self.game_over_text.copy()
            texto_con_alpha.set_alpha(self.game_over_alpha)
            
            # Agregar un resplandor rojo
            glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            glow.fill((255, 0, 0, min(100, self.game_over_alpha // 2)))
            screen.blit(glow, (0, 0))
            
            # Centrar y dibujar el texto
            texto_rect = texto_con_alpha.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(texto_con_alpha, texto_rect)
        
    def dibujar_interfaz(self, screen):
        # Dibujar texto del usuario
        texto_surface = self.fuente.render(f"> {self.texto_usuario}", True, COLORS['BLANCO'])
        screen.blit(texto_surface, (10, self.area_juego_height + 10))
        
        # Dibujar nivel y descripción en el centro superior
        nivel_text = f"NIVEL {self.nivel}"
        
        # Calcular el efecto de parpadeo/color
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.nivel_cambio_tiempo < self.nivel_efecto_duracion:
            # Calcular color basado en el tiempo transcurrido
            progress = (tiempo_actual - self.nivel_cambio_tiempo) / self.nivel_efecto_duracion
            flash_intensity = abs(math.sin(progress * math.pi * 6))  # 3 parpadeos completos
            color_texto = (
                int(255 * flash_intensity),  # R
                int(255 * (1 - flash_intensity * 0.5)),  # G
                int(50 * flash_intensity)  # B
            )
            color_fondo = (
                int(100 * flash_intensity),  # R
                int(50 * flash_intensity),   # G
                int(20 * flash_intensity)    # B
            )
            nivel_surface = self.fuente.render(nivel_text, True, color_texto)
            desc_surface = self.fuente_pequeña.render(PALABRAS_POR_NIVEL[self.nivel]['descripcion'], True, COLORS['BLANCO'])
            
            # Calcular posiciones para centrado
            nivel_rect = nivel_surface.get_rect(centerx=SCREEN_WIDTH // 2, top=10)
            desc_rect = desc_surface.get_rect(centerx=SCREEN_WIDTH // 2, top=nivel_rect.bottom + 5)
            
            # Agregar un fondo semitransparente con efecto
            bg_height = desc_rect.bottom - nivel_rect.top + 10
            bg_width = max(nivel_surface.get_width(), desc_surface.get_width()) + 20
            nivel_bg = pygame.Surface((bg_width, bg_height))
            nivel_bg.fill(color_fondo)
            nivel_bg.set_alpha(128 + int(64 * flash_intensity))
        else:
            nivel_surface = self.fuente.render(nivel_text, True, COLORS['BLANCO'])
            desc_surface = self.fuente_pequeña.render(PALABRAS_POR_NIVEL[self.nivel]['descripcion'], True, COLORS['BLANCO'])
            
            # Calcular posiciones para centrado
            nivel_rect = nivel_surface.get_rect(centerx=SCREEN_WIDTH // 2, top=10)
            desc_rect = desc_surface.get_rect(centerx=SCREEN_WIDTH // 2, top=nivel_rect.bottom + 5)
            
            # Fondo normal
            bg_height = desc_rect.bottom - nivel_rect.top + 10
            bg_width = max(nivel_surface.get_width(), desc_surface.get_width()) + 20
            nivel_bg = pygame.Surface((bg_width, bg_height))
            nivel_bg.fill(COLORS['NEGRO'])
            nivel_bg.set_alpha(128)
        
        # Dibujar el fondo y los textos del nivel
        screen.blit(nivel_bg, (SCREEN_WIDTH//2 - bg_width//2, 5))
        screen.blit(nivel_surface, nivel_rect)
        screen.blit(desc_surface, desc_rect)
        
        # Panel de estadísticas con fondo semitransparente (movido debajo de la línea)
        stats_panel = pygame.Surface((200, 100))  # Altura reducida
        stats_panel.fill(COLORS['NEGRO'])
        stats_panel.set_alpha(128)
        panel_x = 10
        panel_y = self.area_juego_height + 50  # 50 píxeles debajo de la línea
        screen.blit(stats_panel, (panel_x, panel_y))
        
        # Dibujar estadísticas
        punt_surface = self.fuente.render(f"PUNTOS: {self.puntuacion}", True, COLORS['BLANCO'])
        progreso_surface = self.fuente.render(f"{self.palabras_acertadas}/{LEVEL_CONFIG[self.nivel]['palabras_para_pasar']}", True, COLORS['BLANCO'])
        
        screen.blit(punt_surface, (panel_x + 10, panel_y + 10))
        screen.blit(progreso_surface, (panel_x + 10, panel_y + 40))
        
        # Dibujar multiplicadores con efecto brillante
        mult_surface = self.fuente_pequeña.render(f"VELOCIDAD: x{self.multiplicador_velocidad:.1f}", True, COLORS['BLANCO'])
        freq_surface = self.fuente_pequeña.render(f"FRECUENCIA: x{self.multiplicador_frecuencia:.1f}", True, COLORS['BLANCO'])
        
        # Agregar brillo basado en el valor
        glow = pygame.Surface((mult_surface.get_width() + 10, mult_surface.get_height() + 10))
        glow.fill(COLORS['AZUL'])
        glow_alpha = int(min(self.multiplicador_velocidad * 50, 200))
        glow.set_alpha(glow_alpha)
        
        screen.blit(glow, (panel_x + 5, panel_y + 65))
        screen.blit(mult_surface, (panel_x + 10, panel_y + 70))
        
        # Dibujar vidas
        self.dibujar_vidas(screen) 