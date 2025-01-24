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

# Colores del juego
COLORS = {
    'NEGRO': (0, 0, 0),
    'BLANCO': (255, 255, 255),
    'ROJO': (255, 50, 50),         # Meñique izquierdo
    'VERDE': (50, 255, 100),       # Anular izquierdo
    'AZUL': (200, 250, 150),        # Medio izquierdo
    'MORADO': (200, 50, 255),      # Índice izquierdo
    'ROSA': (255, 100, 150),       # Índice derecho
    'CYAN': (50, 200, 255),        # Medio derecho
    'NARANJA': (255, 150, 50),     # Anular derecho
    'MAGENTA': (255, 50, 255),     # Meñique derecho
    'AZUL_CIELO': (135, 206, 235)  # Para el fondo
}

# Teclas asignadas a cada dedo
TECLAS_POR_DEDO = {
    'ROJO': {'Q', 'A', 'Z'},           # Meñique izquierdo
    'VERDE': {'W', 'S', 'X'},          # Anular izquierdo
    'AZUL': {'E', 'D', 'C'},           # Medio izquierdo
    'MORADO': {'R', 'F', 'V', 'T', 'G', 'B'},         # Índice izquierdo
    'ROSA': {'Y', 'H', 'N', 'U', 'J', 'M'},           # Índice derecho
    'CYAN': {'I', 'K'},           # Medio derecho
    'NARANJA': {'O', 'L'},        # Anular derecho
    'MAGENTA': {'P', 'Ñ'}  # Meñique derecho
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