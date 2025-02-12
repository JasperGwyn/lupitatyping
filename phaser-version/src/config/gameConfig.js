export const COLORS = {
    NEGRO: '#000000',
    BLANCO: '#FFFFFF',
    ROJO: '#FF0000',
    VERDE: '#00FF00',
    AZUL: '#0000FF',
    AMARILLO: '#FFFF00',
    MEÑIQUE_IZQ: '#FF69B4',  // Rosa
    ANULAR_IZQ: '#4B0082',   // Índigo
    MEDIO_IZQ: '#9400D3',    // Violeta
    INDICE_IZQ: '#0000FF',   // Azul
    PULGAR_IZQ: '#FFFFFF',   // Blanco
    INDICE_DER: '#00FF00',   // Verde
    MEDIO_DER: '#FFFF00',    // Amarillo
    ANULAR_DER: '#FFA500',   // Naranja
    MEÑIQUE_DER: '#FF0000'   // Rojo
};

export const TECLAS_POR_DEDO = {
    MEÑIQUE_IZQ: ['Q', 'A', 'Z'],
    ANULAR_IZQ: ['W', 'S', 'X'],
    MEDIO_IZQ: ['E', 'D', 'C'],
    INDICE_IZQ: ['R', 'F', 'V'],
    PULGAR_IZQ: [' '],
    INDICE_DER: ['Y', 'H', 'N'],
    MEDIO_DER: ['U', 'J', 'M'],
    ANULAR_DER: ['I', 'K'],
    MEÑIQUE_DER: ['O', 'L', 'P', 'Ñ']
};

export const PALABRAS_POR_NIVEL = {
    1: {
        palabras: [
            'HOLA', 'CASA', 'MESA', 'SILLA', 'LIBRO',
            'PAPEL', 'LAPIZ', 'TAZA', 'VASO', 'PLATO'
        ]
    },
    2: {
        palabras: [
            'ESCUELA', 'VENTANA', 'PUERTA', 'JARDIN',
            'COCINA', 'CUARTO', 'PATIO', 'SALON'
        ]
    },
    3: {
        palabras: [
            'COMPUTADORA', 'TELEFONO', 'TELEVISION',
            'ESCRITORIO', 'BIBLIOTECA', 'CALENDARIO'
        ]
    }
};

export const GAME_CONFIG = {
    VIDAS_INICIALES: 3,
    VELOCIDAD_BASE: 100,
    FRECUENCIA_SPAWN: 3000,
    INCREMENTO_VELOCIDAD: 0.2,
    INCREMENTO_FRECUENCIA: 0.2,
    PALABRAS_POR_NIVEL: 10,
    PUNTOS_POR_LETRA: 10,
    AREA_JUEGO_HEIGHT: 420  // 600 - 180 para el teclado
};

export const SCREEN_CONFIG = {
    WIDTH: 800,
    HEIGHT: 600
}; 