import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
import utils.resource_loader as resources

class Scene:
    def __init__(self, game):
        self.game = game
        
    def init_background(self):
        """Inicializa los elementos comunes del fondo"""
        # Pasto
        self.grass_elements = []
        for i in range(10):
            grass_img = resources.get_image(f'grass{random.randint(1,3)}')
            if grass_img:
                grass_size = (25, 12)  # 25% del tamaño original
                grass_scaled = pygame.transform.scale(grass_img, grass_size)
                x_pos = i * (SCREEN_WIDTH // 10) + random.randint(-20, 20)
                self.grass_elements.append({
                    'surface': grass_scaled,
                    'pos': (x_pos, SCREEN_HEIGHT - grass_size[1])
                })
        
        # Árboles con posiciones fijas
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
                'pos': (int(SCREEN_WIDTH * 0.05), SCREEN_HEIGHT - tree_size[1])
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
                'pos': (int(SCREEN_WIDTH * 0.8), SCREEN_HEIGHT - tree_size[1])
            })
        
        # Cerca
        self.fence_pieces = []
        fence_img = resources.get_image('fence')
        if fence_img:
            fence_height = 45  # 75% del tamaño original (60 * 0.75)
            fence_scale = fence_height / fence_img.get_height()
            fence_size = (int(fence_img.get_width() * fence_scale), fence_height)
            fence_scaled = pygame.transform.scale(fence_img, fence_size)
            for i in range(15):
                x_pos = i * (fence_size[0] - 5)
                self.fence_pieces.append({
                    'surface': fence_scaled,
                    'pos': (x_pos, SCREEN_HEIGHT - fence_size[1])
                })
        
        # Castillo
        self.castle = resources.get_image('castle')
        if self.castle:
            castle_height = SCREEN_HEIGHT // 2
            castle_scale = castle_height / self.castle.get_height()
            castle_size = (int(self.castle.get_width() * castle_scale), castle_height)
            self.castle = pygame.transform.scale(self.castle, castle_size)
            self.castle_pos = (SCREEN_WIDTH//2 - castle_size[0]//2, SCREEN_HEIGHT - castle_size[1])
        
        # Sol
        self.sun = resources.get_image('sun')
        if self.sun:
            sun_size = (100, 100)
            self.sun = pygame.transform.scale(self.sun, sun_size)
            self.sun_pos = [50, 50]
            self.sun_angle = 0
        
        # Nubes
        self.clouds = []
        cloud = resources.get_image('cloud1')
        if cloud:
            for _ in range(5):
                cloud_size = (random.randint(150, 250), random.randint(75, 125))
                cloud_scaled = pygame.transform.scale(cloud, cloud_size)
                self.clouds.append({
                    'surface': cloud_scaled,
                    'pos': [random.randint(0, SCREEN_WIDTH), random.randint(30, 200)],
                    'speed': random.uniform(0.3, 1.0)
                })
    
    def draw_background(self, screen):
        """Dibuja los elementos comunes del fondo"""
        screen.fill(COLORS['AZUL_CIELO'])
        
        # Dibujar sol
        if hasattr(self, 'sun'):
            screen.blit(self.sun, self.sun_pos)
        
        # Dibujar nubes
        for cloud in self.clouds:
            screen.blit(cloud['surface'], cloud['pos'])
        
        # Dibujar árboles de fondo
        for tree in self.trees[:2]:
            screen.blit(tree['surface'], tree['pos'])
        
        # Dibujar castillo
        if hasattr(self, 'castle'):
            screen.blit(self.castle, self.castle_pos)
        
        # Dibujar árboles de frente
        for tree in self.trees[2:]:
            screen.blit(tree['surface'], tree['pos'])
        
        # Dibujar cerca
        for fence in self.fence_pieces:
            screen.blit(fence['surface'], fence['pos'])
        
        # Dibujar pasto
        for grass in self.grass_elements:
            screen.blit(grass['surface'], grass['pos'])
    
    def update_background(self):
        """Actualiza las animaciones del fondo"""
        tiempo_actual = pygame.time.get_ticks()
        
        # Animar el sol
        if hasattr(self, 'sun_angle'):
            self.sun_angle = (self.sun_angle + 0.5) % 360
            self.sun_pos[1] = 50 + math.sin(math.radians(self.sun_angle)) * 10
        
        # Animar las nubes
        for cloud in self.clouds:
            cloud['pos'][0] -= cloud['speed']
            if cloud['pos'][0] + cloud['surface'].get_width() < -200:
                cloud['pos'][0] = SCREEN_WIDTH + random.randint(100, 300)
                cloud['pos'][1] = random.randint(30, 200)
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass 