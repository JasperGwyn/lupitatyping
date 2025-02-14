import BaseScene from './BaseScene';
import { COLORS, PALABRAS_POR_NIVEL, GAME_CONFIG, SCREEN_CONFIG } from '../config/gameConfig';

export default class GameScene extends BaseScene {
    constructor() {
        super('game');
        this.useCommonBackground = true;  // Activar el fondo común
        this.words = [];
        this.userText = '';
        this.score = 0;
        this.level = 1;
        this.wordsCompleted = 0;
        this.lives = GAME_CONFIG.VIDAS_INICIALES;
        this.lastSpawnTime = 0;
        this.speedMultiplier = 1.0;
        this.frequencyMultiplier = 1.0;
        this.gameOver = false;
        this.canSpawnWords = false;
        this.nextSpawnTime = 0;  // Nuevo: tiempo exacto para el próximo spawn
    }

    preload() {
        super.preload();
        // Cargar solo los assets específicos del juego
        this.load.image('wizard', 'assets/images/characters/wizard.png');
        this.load.image('heart', 'assets/images/ui/heart.png');
        this.load.image('magic_effect', 'assets/images/effects/magic_effect.png');
        
        // Cargar sonidos
        this.load.audio('success', 'assets/sounds/effects/powerUp2.ogg');
        this.load.audio('error', 'assets/sounds/effects/lowThreeTone.ogg');
        this.load.audio('explosion', 'assets/sounds/effects/sfx_explosionGoo.ogg');
        this.load.audio('game_music', `assets/sounds/music/game_theme_nivel${this.level}.ogg`);
    }

    create() {
        super.create();  // Esto creará el fondo común

        // Configurar sonidos
        this.sounds = {
            success: this.sound.add('success', { volume: 0.3 }),
            error: this.sound.add('error', { volume: 0.3 }),
            explosion: this.sound.add('explosion', { volume: 0.4 })
        };

        // Iniciar música
        this.music = this.sound.add('game_music', { volume: 0.5, loop: true });
        this.music.play();

        // Crear elementos visuales específicos del juego
        this.createWizard();
        this.createUI();

        // Configurar entrada de texto
        this.input.keyboard.on('keydown', this.handleKeyInput, this);

        // Mostrar introducción del nivel antes de comenzar
        this.showLevelIntro();
    }

    createWizard() {
        const wizardHeight = 120;
        this.wizard = this.add.image(SCREEN_CONFIG.WIDTH - 100, SCREEN_CONFIG.HEIGHT - wizardHeight/2, 'wizard');
        
        // Ajustar el tamaño manteniendo la proporción
        const scale = wizardHeight / this.wizard.height;
        this.wizard.setScale(scale);
        
        // Animación flotante
        this.tweens.add({
            targets: this.wizard,
            y: '-=20',
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.inOut'
        });
    }

    createUI() {
        // Crear corazones de vida
        this.hearts = [];
        for (let i = 0; i < this.lives; i++) {
            const heart = this.add.image(760 - i * 35, 30, 'heart')
                .setScale(0.5)
                .setTint(0xff0000);
            this.hearts.push(heart);
        }

        // Crear teclado visual
        this.createKeyboard();

        // Crear texto de puntuación
        this.scoreText = this.add.text(20, 20, `Puntuación: ${this.score}`, {
            fontFamily: '"Press Start 2P"',
            fontSize: '20px',
            fill: '#fff',
            padding: { x: 10, y: 5 },
            shadow: {
                offsetX: 2,
                offsetY: 2,
                color: '#000',
                blur: 3,
                fill: true
            }
        });

        // Crear texto de nivel
        this.levelText = this.add.text(20, 50, `Nivel: ${this.level}`, {
            fontFamily: '"Press Start 2P"',
            fontSize: '20px',
            fill: '#fff',
            padding: { x: 10, y: 5 },
            shadow: {
                offsetX: 2,
                offsetY: 2,
                color: '#000',
                blur: 3,
                fill: true
            }
        });

        // Crear campo de texto del usuario
        this.userTextField = this.add.text(400, SCREEN_CONFIG.HEIGHT - 50, '', {
            fontFamily: '"Press Start 2P"',
            fontSize: '28px',
            fill: '#fff',
            backgroundColor: '#00000088',
            padding: { x: 15, y: 10 },
            shadow: {
                offsetX: 2,
                offsetY: 2,
                color: '#000',
                blur: 3,
                fill: true
            }
        }).setOrigin(0.5);
    }

    createKeyboard() {
        const keySize = 20;  // Reducido un poco para que quepa mejor
        const padding = 2;
        const startY = 70;  // Debajo de los corazones
        const rightMargin = 20;  // Margen desde el borde derecho
        
        // Definir las filas del teclado
        const rows = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ];

        // Definir colores por dedo
        const fingerColors = {
            'Q': 0xff0000, 'A': 0xff0000, 'Z': 0xff0000,  // Meñique izquierdo (rojo)
            'W': 0x00ff00, 'S': 0x00ff00, 'X': 0x00ff00,  // Anular izquierdo (verde)
            'E': 0x9933ff, 'D': 0x9933ff, 'C': 0x9933ff,  // Medio izquierdo (morado)
            'R': 0xff00ff, 'F': 0xff00ff, 'V': 0xff00ff,   // Índice izquierdo (rosa)
            'T': 0xff00ff, 'G': 0xff00ff, 'B': 0xff00ff,   // Índice izquierdo (rosa)
            'Y': 0x00ffff, 'H': 0x00ffff, 'N': 0x00ffff,   // Índice derecho (cyan)
            'U': 0x00ffff, 'J': 0x00ffff, 'M': 0x00ffff,   // Índice derecho (cyan)
            'I': 0x0000ff, 'K': 0x0000ff,                  // Medio derecho (azul)
            'O': 0xffa500, 'L': 0xffa500,                  // Anular derecho (naranja)
            'P': 0x006400, 'Ñ': 0x006400                   // Meñique derecho (verde oscuro)
        };

        // Calcular el ancho total del teclado para alinearlo a la derecha
        const maxRowLength = Math.max(...rows.map(row => row.length));
        const totalWidth = maxRowLength * (keySize + padding) - padding;
        const startX = SCREEN_CONFIG.WIDTH - totalWidth - rightMargin;

        // Crear el teclado
        rows.forEach((row, rowIndex) => {
            const rowWidth = row.length * (keySize + padding) - padding;
            let rowX;

            if (rowIndex === 1) {
                // Para la segunda fila (A-Ñ), desplazar un cuarto de tecla
                rowX = startX + (keySize + padding) * 0.25;
            } else if (rowIndex === 2) {
                // Para la tercera fila (Z-M), desplazar media tecla más que la segunda fila
                rowX = startX + (keySize + padding) * 0.75;
            } else {
                rowX = startX;
            }

            row.forEach((key, keyIndex) => {
                const x = rowX + keyIndex * (keySize + padding);
                const y = startY + rowIndex * (keySize + padding);

                // Crear fondo de la tecla
                const keyBackground = this.add.rectangle(x, y, keySize, keySize, fingerColors[key])
                    .setOrigin(0, 0)
                    .setAlpha(0.8);

                // Crear texto de la tecla
                this.add.text(x + keySize/2, y + keySize/2, key, {
                    fontFamily: '"Press Start 2P"',
                    fontSize: '8px',  // Reducido un poco para que quepa mejor
                    fill: '#fff'
                }).setOrigin(0.5);
            });
        });
    }

    handleKeyInput(event) {
        if (this.gameOver) return;

        if (event.key === 'Backspace') {
            this.userText = this.userText.slice(0, -1);
        } else if (event.key === 'Enter') {
            this.checkWord();
        } else if (event.key.length === 1 && event.key.match(/[a-záéíóúñA-ZÁÉÍÓÚÑ]/i)) {
            this.userText += event.key.toUpperCase();
        }

        this.userTextField.setText(this.userText);
    }

    checkWord() {
        const word = this.words.find(w => w.text === this.userText);
        if (word) {
            // Palabra correcta
            this.score += word.text.length * GAME_CONFIG.PUNTOS_POR_LETRA;
            this.wordsCompleted++;
            this.sounds.success.play();
            
            // Eliminar la palabra
            this.words = this.words.filter(w => w !== word);
            word.container.destroy();
            
            // Efectos visuales
            this.createSuccessEffect(word.container.x, word.container.y);

            // Si no hay palabras en pantalla, programar la siguiente palabra
            if (this.words.length === 0 && this.canSpawnWords) {
                this.nextSpawnTime = this.time.now;  // Spawn inmediato
            }
        } else {
            // Palabra incorrecta
            this.sounds.error.play();
        }

        // Limpiar texto del usuario
        this.userText = '';
        this.userTextField.setText('');

        // Verificar nivel completo
        this.checkLevelComplete();
    }

    createSuccessEffect(x, y) {
        const particles = this.add.particles(x, y, 'magic_effect', {
            speed: { min: 100, max: 200 },
            angle: { min: 0, max: 360 },
            scale: { start: 0.5, end: 0 },
            lifespan: 1000,
            quantity: 20
        });

        this.time.delayedCall(1000, () => particles.destroy());
    }

    spawnWord() {
        // No spawnear si no está permitido
        if (!this.canSpawnWords) return;
        
        const availableWords = PALABRAS_POR_NIVEL[this.level].palabras;
        const word = Phaser.Math.RND.pick(availableWords);
        const x = Phaser.Math.Between(100, SCREEN_CONFIG.WIDTH - 100);
        
        // Crear un contenedor para la palabra
        const container = this.add.container(x, 0);
        
        // Definir colores por letra (usando los mismos del teclado)
        const letterColors = {
            'Q': 0xff0000, 'A': 0xff0000, 'Z': 0xff0000,  // Meñique izquierdo (rojo)
            'W': 0x00ff00, 'S': 0x00ff00, 'X': 0x00ff00,  // Anular izquierdo (verde)
            'E': 0x9933ff, 'D': 0x9933ff, 'C': 0x9933ff,  // Medio izquierdo (morado)
            'R': 0xff00ff, 'F': 0xff00ff, 'V': 0xff00ff,   // Índice izquierdo (rosa)
            'T': 0xff00ff, 'G': 0xff00ff, 'B': 0xff00ff,   // Índice izquierdo (rosa)
            'Y': 0x00ffff, 'H': 0x00ffff, 'N': 0x00ffff,   // Índice derecho (cyan)
            'U': 0x00ffff, 'J': 0x00ffff, 'M': 0x00ffff,   // Índice derecho (cyan)
            'I': 0x0000ff, 'K': 0x0000ff,                  // Medio derecho (azul)
            'O': 0xffa500, 'L': 0xffa500,                  // Anular derecho (naranja)
            'P': 0x006400, 'Ñ': 0x006400                   // Meñique derecho (verde oscuro)
        };

        // Crear cada letra individualmente
        let totalWidth = 0;
        const letterSpacing = 5;
        const letterObjects = [];

        // Primero crear todas las letras para calcular el ancho total
        word.split('').forEach((letter, index) => {
            const letterText = this.add.text(0, 0, letter, {
                fontFamily: '"Press Start 2P"',
                fontSize: '24px',
                fill: '#fff'
            });
            letterText.setTint(letterColors[letter] || 0xffffff);
            letterObjects.push(letterText);
            totalWidth += letterText.width + (index < word.length - 1 ? letterSpacing : 0);
        });

        // Ahora posicionar cada letra
        let currentX = -totalWidth / 2;
        letterObjects.forEach(letterText => {
            letterText.setPosition(currentX, 0);
            currentX += letterText.width + letterSpacing;
            container.add(letterText);
        });

        this.words.push({
            container,
            text: word,
            speed: GAME_CONFIG.VELOCIDAD_BASE * this.speedMultiplier
        });
    }

    getSpawnTime() {
        return GAME_CONFIG.FRECUENCIA_SPAWN / this.frequencyMultiplier;
    }

    showLevelIntro() {
        // Desactivar el spawning de palabras durante la introducción
        this.canSpawnWords = false;
        
        // Crear un fondo semi-transparente
        const bg = this.add.rectangle(0, 0, SCREEN_CONFIG.WIDTH, SCREEN_CONFIG.HEIGHT, 0x000000, 0.7)
            .setOrigin(0, 0);

        const centerY = SCREEN_CONFIG.HEIGHT * 0.4;

        // Texto del número de nivel
        const levelTitle = this.add.text(SCREEN_CONFIG.WIDTH/2, centerY, `NIVEL ${this.level}`, {
            fontFamily: '"Press Start 2P"',
            fontSize: '28px',
            fill: '#fff',
            align: 'center'
        }).setOrigin(0.5);

        // Texto de la descripción
        const descText = this.add.text(SCREEN_CONFIG.WIDTH/2, centerY + 60, PALABRAS_POR_NIVEL[this.level].descripcion, {
            fontFamily: '"Press Start 2P"',
            fontSize: '16px',
            fill: '#fff',
            align: 'center',
            wordWrap: { width: 600 }
        }).setOrigin(0.5);

        // Animación de fade out después de 2 segundos
        this.time.delayedCall(2000, () => {
            this.tweens.add({
                targets: [bg, levelTitle, descText],
                alpha: 0,
                duration: 500,
                onComplete: () => {
                    // Limpiar los elementos visuales
                    bg.destroy();
                    levelTitle.destroy();
                    descText.destroy();
                    
                    // Activar el spawning de palabras
                    this.canSpawnWords = true;
                    
                    // Spawnear la primera palabra y programar la siguiente
                    this.spawnWord();
                    this.nextSpawnTime = this.time.now + (GAME_CONFIG.FRECUENCIA_SPAWN / this.frequencyMultiplier);
                }
            });
        });
    }

    checkLevelComplete() {
        if (this.wordsCompleted >= GAME_CONFIG.PALABRAS_POR_NIVEL) {
            this.level++;
            this.speedMultiplier *= GAME_CONFIG.INCREMENTO_VELOCIDAD;
            this.frequencyMultiplier *= GAME_CONFIG.INCREMENTO_FRECUENCIA;
            
            // Si hay siguiente nivel, mostrar la introducción del nuevo nivel
            if (PALABRAS_POR_NIVEL[this.level]) {
                // Limpiar palabras existentes
                this.words.forEach(word => word.container.destroy());
                this.words = [];
                this.wordsCompleted = 0;
                
                // Mostrar la introducción del nuevo nivel
                this.showLevelIntro();
            } else {
                // Si no hay más niveles, ir a la pantalla de resultados
                this.game.changeScene(this, 'results');
            }
        }
    }

    loseLife() {
        this.lives--;
        this.sounds.explosion.play();
        
        // Actualizar corazones
        if (this.hearts.length > 0) {
            const heart = this.hearts.pop();
            heart.destroy();
        }

        if (this.lives <= 0) {
            this.gameOver = true;
            this.showGameOver();
        }
    }

    showGameOver() {
        const gameOverText = this.add.text(SCREEN_CONFIG.WIDTH/2, SCREEN_CONFIG.HEIGHT/2, '¡GAME OVER!', {
            fontFamily: '"Press Start 2P"',
            fontSize: '64px',
            fill: '#ff0000'
        }).setOrigin(0.5).setAlpha(0);

        this.tweens.add({
            targets: gameOverText,
            alpha: 1,
            duration: 2000,
            onComplete: () => {
                this.game.changeScene(this, 'results');
            }
        });
    }

    update(time, delta) {
        // Actualizar palabras
        this.words.forEach(word => {
            word.container.y += (word.speed * delta) / 1000;
            
            // Verificar si la palabra llegó al fondo
            if (word.container.y > SCREEN_CONFIG.HEIGHT) {
                this.loseLife();
                // Crear efecto de explosión antes de destruir
                this.createExplosionEffect(word.container.x, SCREEN_CONFIG.HEIGHT);
                word.container.destroy();
                this.words = this.words.filter(w => w !== word);
            }
        });

        // Verificar si es tiempo de generar una nueva palabra
        if (this.canSpawnWords && time >= this.nextSpawnTime) {
            this.spawnWord();
            // Programar el próximo spawn
            this.nextSpawnTime = time + (GAME_CONFIG.FRECUENCIA_SPAWN / this.frequencyMultiplier);
        }

        // Actualizar textos de UI
        this.scoreText.setText(`Puntuación: ${this.score}`);
        this.levelText.setText(`Nivel: ${this.level}`);
    }

    createExplosionEffect(x, y) {
        // Efecto de explosión más dramático
        const particles = this.add.particles(x, y, 'magic_effect', {
            speed: { min: 200, max: 400 },
            angle: { min: 0, max: 360 },
            scale: { start: 0.6, end: 0 },
            lifespan: 800,
            quantity: 30,
            gravityY: 200
        });

        this.time.delayedCall(800, () => particles.destroy());
    }
} 