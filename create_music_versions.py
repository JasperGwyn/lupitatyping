import pygame
import os
import shutil

def create_tempo_versions(input_file, output_dir):
    """Crea diferentes versiones del archivo de música copiando el archivo original"""
    print(f"Creando versiones del archivo: {input_file}")
    
    # Obtener la extensión del archivo original
    _, extension = os.path.splitext(input_file)
    
    # Crear versiones con diferentes nombres
    tempos = {
        1: 1.0,    # Normal
        2: 1.25,   # 25% más rápido
        3: 1.5,    # 50% más rápido
        4: 1.75,   # 75% más rápido
        5: 2.0     # Doble velocidad
    }
    
    for nivel, tempo in tempos.items():
        print(f"Creando versión nivel {nivel} (tempo: x{tempo})")
        
        # Crear nombre del archivo de salida manteniendo la extensión original
        output_file = os.path.join(output_dir, f'game_theme_nivel{nivel}{extension}')
        
        # Copiar el archivo
        shutil.copy2(input_file, output_file)
        print(f"Archivo guardado: {output_file}")
        
    print("\nNOTA: Como no podemos modificar el tempo directamente, se han creado copias del archivo original.")
    print("Por favor, usa un editor de audio externo como Audacity para ajustar el tempo de cada archivo:")
    for nivel, tempo in tempos.items():
        print(f"- Nivel {nivel}: ajustar a {tempo*100}% de velocidad")

if __name__ == "__main__":
    # Rutas de archivos
    input_file = "assets/sounds/music/game_theme.opus"  # Cambiado a .opus
    output_dir = "assets/sounds/music"
    
    # Asegurarse de que el directorio existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear las versiones
    create_tempo_versions(input_file, output_dir)
    print("\n¡Proceso completado!") 