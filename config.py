# Configuración general
GAME_TITLE = "LA AVENTURA MÁGICA DE LUPITA"
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
    'NEGRO': (0, 0, 0),
    'BLANCO': (255, 255, 255),
    'ROJO': (255, 0, 0),
    'VERDE': (0, 255, 0),
    'AZUL': (0, 0, 255),
    'AMARILLO': (255, 255, 0),
    'CELESTE': (0, 191, 255),
    'AZUL_CIELO': (135, 206, 235),  # Agregado para el fondo
    'MEÑIQUE_IZQ': (255, 100, 100),
    'ANULAR_IZQ': (100, 255, 100),
    'MEDIO_IZQ': (100, 100, 255),
    'INDICE_IZQ': (255, 255, 100),
    'INDICE_DER': (255, 100, 255),
    'MEDIO_DER': (100, 255, 255),
    'ANULAR_DER': (255, 200, 100),
    'MEÑIQUE_DER': (200, 100, 255)
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
        'descripcion': 'POSICIÓN BASE - DEDOS ÍNDICES (F Y J)'
    },
    2: {  # Nivel 2: Dedos medios
        'palabras': ['DEDO', 'KILO', 'DIKE'],
        'descripcion': 'DEDOS MEDIOS (D Y K)'
    },
    3: {  # Nivel 3: Dedos anulares
        'palabras': ['SOL', 'LOS', 'SAL'],
        'descripcion': 'DEDOS ANULARES (S Y L)'
    },
    4: {  # Nivel 4: Dedos meñiques
        'palabras': ['PAZ', 'AÑO', 'QUE'],
        'descripcion': 'DEDOS MEÑIQUES (Q Y P)'
    },
    5: {  # Nivel 5: Combinaciones
        'palabras': ['CASA', 'MESA', 'PATO', 'LUNA'],
        'descripcion': 'COMBINANDO TODOS LOS DEDOS'
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