import pygame
import os

# Diccionario para almacenar las imágenes cargadas
_images = {}

def load_image(name, path):
    """Carga una imagen y la almacena en el diccionario"""
    try:
        fullpath = os.path.join('assets/images', path)
        image = pygame.image.load(fullpath).convert_alpha()
        _images[name] = image
        return image
    except Exception as e:
        print(f"Error cargando imagen {path}: {str(e)}")
        return None

def get_image(name):
    """Obtiene una imagen del diccionario"""
    return _images.get(name)

def clear_resources():
    """Limpia todas las imágenes cargadas"""
    _images.clear()

def load_all_resources():
    """Carga todos los recursos necesarios para el juego"""
    # Cargar personajes
    load_image('wizard', 'characters/wizard.png')
    
    # Cargar elementos de fondo
    load_image('castle', 'backgrounds/castle.png')
    load_image('sun', 'backgrounds/sun.png')
    load_image('cloud1', 'backgrounds/cloud1.png')
    load_image('tree1', 'backgrounds/tree1.png')
    load_image('tree2', 'backgrounds/tree2.png')
    load_image('grass1', 'backgrounds/grass1.png')
    load_image('grass2', 'backgrounds/grass2.png')
    load_image('grass3', 'backgrounds/grass3.png')
    load_image('fence', 'backgrounds/fence.png')
    
    # Cargar UI
    load_image('heart', 'ui/heart.png')  # Nuevo corazón pixel art 