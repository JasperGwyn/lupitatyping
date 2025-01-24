import pygame
from config import *
from scenes.menu_scene import MenuScene
from scenes.game_scene import GameScene
from scenes.results_scene import ResultsScene
from scenes.intro_scene import IntroScene
from scenes.instructions_scene import InstructionsScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None  # Inicializar como None primero
        
        # Registrar todas las escenas
        self.scenes = {
            "menu": MenuScene(self),
            "game": GameScene(self),
            "instructions": InstructionsScene(self)
        }
        
        # Comenzar con la escena de intro
        self.current_scene = IntroScene(self)
        
    def change_scene(self, scene_name):
        if scene_name == "intro":
            self.current_scene = IntroScene(self)
        elif scene_name == "menu":
            self.current_scene = MenuScene(self)
        elif scene_name == "game":
            pygame.mixer.music.stop()
            self.current_scene = GameScene(self)
        elif scene_name == "instructions":
            self.current_scene = InstructionsScene(self)
        elif scene_name == "results":
            # Pasar la puntuación y el nivel antes de crear la escena
            self.puntuacion = getattr(self.current_scene, 'puntuacion', 0)
            self.nivel = getattr(self.current_scene, 'nivel', 1)
            # Crear la escena de resultados
            self.current_scene = ResultsScene(self)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.current_scene.handle_event(event)

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.current_scene.draw(self.screen)
        pygame.display.flip() 