import pygame
import os

# Diccionario para almacenar las imágenes cargadas
_images = {}

def load_all_resources():
    """Carga todos los recursos necesarios para el juego"""
    # Asegurarse que el directorio de assets existe
    if not os.path.exists('assets/images'):
        os.makedirs('assets/images')
    
    # Cargar imágenes
    load_image('castle', 'backgrounds/castle.png')
    load_image('cloud1', 'backgrounds/cloud1.png')
    load_image('sun', 'backgrounds/sun.png')
    load_image('wizard', 'characters/wizard.png')
    load_image('heart', 'ui/heart.png')

def load_image(name, path):
    """Carga una imagen y la guarda en el diccionario"""
    try:
        full_path = os.path.join('assets/images', path)
        image = pygame.image.load(full_path).convert_alpha()
        _images[name] = image
        return image
    except Exception as e:
        print(f"Error cargando imagen {path}: {str(e)}")
        return None

def get_image(name):
    """Obtiene una imagen del diccionario por su nombre"""
    return _images.get(name)

def clear_resources():
    """Limpia todos los recursos cargados"""
    _images.clear() 