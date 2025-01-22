# Configuración general
GAME_TITLE = "Lupita's Typing Adventure"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Configuración base del juego
VELOCIDAD_BASE = 1        # Velocidad inicial de caída
FRECUENCIA_BASE = 3000      # Tiempo entre palabras en milisegundos (4 segundos)
INCREMENTO_VELOCIDAD = 1.1  # Multiplicador de velocidad por palabra acertada (50% más rápido)
INCREMENTO_FRECUENCIA = 1.1 # Multiplicador de frecuencia por palabra acertada (20% más frecuente)

# Generación automática de configuración de niveles
LEVEL_CONFIG = {}
for nivel in range(1, 6):  # 5 niveles
    multiplicador = (1.5 ** (nivel - 1))  # 1, 1.5, 2.25, 3.375, 5.0625
    LEVEL_CONFIG[nivel] = {
        'velocidad_palabras': VELOCIDAD_BASE * multiplicador,
        'tiempo_spawn': int(FRECUENCIA_BASE / multiplicador),  # Dividimos porque queremos que sea más frecuente
        'puntos_palabra': 10 * nivel,
        'palabras_para_pasar': 5 + (nivel - 1) * 3
    }

# Colores
COLORS = {
    'ROSA': (255, 192, 203),
    'AZUL': (100, 149, 237),
    'VERDE': (144, 238, 144),
    'NEGRO': (0, 0, 0),
    'BLANCO': (255, 255, 255),
    'ROJO': (255, 0, 0),
    # Colores para cada dedo
    'MEÑIQUE_IZQ': (255, 100, 100),  # Rojo suave
    'ANULAR_IZQ': (255, 180, 100),   # Naranja
    'MEDIO_IZQ': (150, 220, 150),    # Verde suave
    'INDICE_IZQ': (180, 255, 100),   # Verde claro
    'INDICE_DER': (100, 255, 180),   # Verde agua
    'MEDIO_DER': (100, 255, 255),    # Celeste
    'ANULAR_DER': (100, 180, 255),   # Azul claro
    'MEÑIQUE_DER': (180, 100, 255)   # Violeta
}

# Configuración de teclas por dedo
TECLAS_POR_DEDO = {
    'MEÑIQUE_IZQ': ['Q', 'A', 'Z'],
    'ANULAR_IZQ': ['W', 'S', 'X'],
    'MEDIO_IZQ': ['E', 'D', 'C'],
    'INDICE_IZQ': ['R', 'F', 'V', 'T', 'G', 'B'],
    'INDICE_DER': ['Y', 'H', 'N', 'U', 'J', 'M'],
    'MEDIO_DER': ['I', 'K'],
    'ANULAR_DER': ['O', 'L'],
    'MEÑIQUE_DER': ['P', 'Ñ']
}

# Palabras organizadas por nivel y posición de dedos
PALABRAS_POR_NIVEL = {
    1: {  # Nivel 1: Dedos índices (posición base)
        'palabras': ['MAMA', 'NENE', 'NANA'],
        'descripcion': 'Posición base - Dedos índices (F y J)'
    },
    2: {  # Nivel 2: Dedos medios
        'palabras': ['DEDO', 'KILO', 'DIKE'],
        'descripcion': 'Dedos medios (D y K)'
    },
    3: {  # Nivel 3: Dedos anulares
        'palabras': ['SOL', 'LOS', 'SAL'],
        'descripcion': 'Dedos anulares (S y L)'
    },
    4: {  # Nivel 4: Dedos meñiques
        'palabras': ['PAZ', 'AÑO', 'QUE'],
        'descripcion': 'Dedos meñiques (Q y P)'
    },
    5: {  # Nivel 5: Combinaciones
        'palabras': ['CASA', 'MESA', 'PATO', 'LUNA'],
        'descripcion': 'Combinando todos los dedos'
    }
}

# Configuración del juego
GAME_CONFIG = {
    'VIDAS_INICIALES': 3,
    'TIEMPO_ANIMACION': 1000,  # milisegundos
    'VELOCIDAD_ANIMACION': 0.5
}

# Rutas de recursos
PATHS = {
    'FONTS': 'assets/fonts',
    'IMAGES': 'assets/images',
    'SOUNDS': 'assets/sounds',
    'DATA': 'data'
} 