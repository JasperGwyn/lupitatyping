import BaseScene from './BaseScene';
import { COLORS, PALABRAS_POR_NIVEL, GAME_CONFIG, SCREEN_CONFIG } from '../config/gameConfig';

export default class GameScene extends BaseScene {
    constructor() {
        super('game');
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
    }

    preload() {
        // Cargar assets
        this.load.image('background', 'assets/images/backgrounds/magic_school.png');
        this.load.image('wizard', 'assets/images/characters/wizard.png');
        this.load.image('heart', 'assets/images/ui/heart.png');
        this.load.image('cloud1', 'assets/images/backgrounds/cloud1.png');
        this.load.image('tree1', 'assets/images/backgrounds/tree1.png');
        this.load.image('tree2', 'assets/images/backgrounds/tree2.png');
        
        // Cargar sonidos
        this.load.audio('success', 'assets/sounds/effects/powerUp2.ogg');
        this.load.audio('error', 'assets/sounds/effects/lowThreeTone.ogg');
        this.load.audio('explosion', 'assets/sounds/effects/sfx_explosionGoo.ogg');
        this.load.audio('game_music', `assets/sounds/music/game_theme_nivel${this.level}.ogg`);
    }

    create() {
        super.create();

        // Configurar fondo
        this.add.image(400, 300, 'background').setScale(2);

        // Configurar sonidos
        this.sounds = {
            success: this.sound.add('success', { volume: 0.3 }),
            error: this.sound.add('error', { volume: 0.3 }),
            explosion: this.sound.add('explosion', { volume: 0.4 })
        };

        // Iniciar música
        this.music = this.sound.add('game_music', { volume: 0.5, loop: true });
        this.music.play();

        // Crear elementos visuales
        this.createWizard();
        this.createClouds();
        this.createTrees();
        this.createParticles();
        this.createUI();

        // Configurar entrada de texto
        this.input.keyboard.on('keydown', this.handleKeyInput, this);

        // Iniciar spawning de palabras
        this.time.addEvent({
            delay: this.getSpawnTime(),
            callback: this.spawnWord,
            callbackScope: this,
            loop: true
        });
    }

    createWizard() {
        this.wizard = this.add.image(700, 450, 'wizard')
            .setScale(0.8);
        
        // Animación flotante
        this.tweens.add({
            targets: this.wizard,
            y: '+=20',
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.inOut'
        });
    }

    createClouds() {
        this.clouds = [];
        for (let i = 0; i < 3; i++) {
            const cloud = this.add.image(
                Phaser.Math.Between(0, 800),
                Phaser.Math.Between(50, 150),
                'cloud1'
            ).setScale(Phaser.Math.FloatBetween(0.5, 0.8));
            
            this.clouds.push({
                sprite: cloud,
                speed: Phaser.Math.FloatBetween(0.2, 0.5)
            });
        }
    }

    createTrees() {
        this.add.image(50, GAME_CONFIG.AREA_JUEGO_HEIGHT - 100, 'tree1')
            .setScale(0.8);
        this.add.image(750, GAME_CONFIG.AREA_JUEGO_HEIGHT - 100, 'tree2')
            .setScale(0.8);
    }

    createParticles() {
        this.particles = this.add.particles(0, 0, 'magic_particle', {
            quantity: 20,
            gravityY: 0,
            lifespan: 2000,
            alpha: { start: 0.8, end: 0 },
            scale: { start: 0.2, end: 0 },
            speed: { min: 50, max: 100 },
            emitZone: {
                type: 'random',
                source: new Phaser.Geom.Rectangle(0, 0, 800, GAME_CONFIG.AREA_JUEGO_HEIGHT)
            }
        });
    }

    createUI() {
        // Crear corazones de vida con mejor estilo
        this.hearts = [];
        for (let i = 0; i < this.lives; i++) {
            const heart = this.add.image(760 - i * 35, 30, 'heart')
                .setScale(0.5)
                .setTint(0xff0000);
            this.hearts.push(heart);
        }

        // Crear texto de puntuación con mejor estilo
        this.scoreText = this.add.text(20, 20, `Puntuación: ${this.score}`, {
            fontFamily: 'Press Start 2P',
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
            fontFamily: 'Press Start 2P',
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

        // Crear campo de texto del usuario con mejor estilo
        this.userTextField = this.add.text(400, 550, '', {
            fontFamily: 'Press Start 2P',
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

    handleKeyInput(event) {
        if (this.gameOver) return;

        if (event.key === 'Backspace') {
            this.userText = this.userText.slice(0, -1);
        } else if (event.key === 'Enter') {
            this.checkWord();
        } else if (event.key.length === 1) {
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
            word.sprite.destroy();
            
            // Efectos visuales
            this.createSuccessEffect(word.sprite.x, word.sprite.y);
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
        const particles = this.add.particles(x, y, 'magic_particle', {
            speed: { min: 100, max: 200 },
            angle: { min: 0, max: 360 },
            scale: { start: 0.5, end: 0 },
            lifespan: 1000,
            quantity: 20
        });

        this.time.delayedCall(1000, () => particles.destroy());
    }

    spawnWord() {
        const availableWords = PALABRAS_POR_NIVEL[this.level].palabras;
        const word = Phaser.Math.RND.pick(availableWords);
        const x = Phaser.Math.Between(100, SCREEN_CONFIG.WIDTH - 100);
        
        // Crear un contenedor para la palabra
        const container = this.add.container(x, 0);
        
        // Agregar sombra del texto
        const shadow = this.add.text(2, 2, word, {
            fontFamily: 'Press Start 2P',
            fontSize: '24px',
            fill: '#000',
            padding: { x: 10, y: 5 }
        }).setOrigin(0.5);
        
        // Agregar el texto principal
        const text = this.add.text(0, 0, word, {
            fontFamily: 'Press Start 2P',
            fontSize: '24px',
            fill: '#fff',
            padding: { x: 10, y: 5 }
        }).setOrigin(0.5);
        
        // Agregar un fondo semi-transparente
        const bounds = text.getBounds();
        const background = this.add.rectangle(
            0,
            0,
            bounds.width + 20,
            bounds.height + 10,
            0x000000,
            0.5
        ).setOrigin(0.5);
        
        // Agregar los elementos al contenedor en orden
        container.add([background, shadow, text]);
        
        // Agregar un efecto de brillo
        const glow = this.add.rectangle(
            0,
            0,
            bounds.width + 30,
            bounds.height + 20,
            0xffffff,
            0.2
        ).setOrigin(0.5);
        
        container.add(glow);
        
        // Animación de brillo
        this.tweens.add({
            targets: glow,
            alpha: 0,
            duration: 1500,
            ease: 'Sine.InOut',
            yoyo: true,
            repeat: -1
        });

        this.words.push({
            sprite: container,
            text: word,
            speed: GAME_CONFIG.VELOCIDAD_BASE * this.speedMultiplier
        });
    }

    getSpawnTime() {
        return GAME_CONFIG.FRECUENCIA_SPAWN / this.frequencyMultiplier;
    }

    checkLevelComplete() {
        if (this.wordsCompleted >= GAME_CONFIG.PALABRAS_POR_NIVEL) {
            this.level++;
            this.speedMultiplier += GAME_CONFIG.INCREMENTO_VELOCIDAD;
            this.frequencyMultiplier += GAME_CONFIG.INCREMENTO_FRECUENCIA;
            this.game.changeScene(this, 'results');
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
        const gameOverText = this.add.text(400, 300, '¡GAME OVER!', {
            fontSize: '64px',
            fill: '#ff0000'
        }).setOrigin(0.5);

        this.tweens.add({
            targets: gameOverText,
            alpha: { from: 0, to: 1 },
            duration: 2000,
            onComplete: () => {
                this.game.changeScene(this, 'results');
            }
        });
    }

    update(time, delta) {
        // Actualizar nubes
        this.clouds.forEach(cloud => {
            cloud.sprite.x += cloud.speed;
            if (cloud.sprite.x > 850) {
                cloud.sprite.x = -50;
            }
        });

        // Actualizar palabras
        this.words.forEach(word => {
            word.sprite.y += (word.speed * delta) / 1000;
            
            // Verificar si la palabra llegó al fondo
            if (word.sprite.y > GAME_CONFIG.AREA_JUEGO_HEIGHT) {
                this.loseLife();
                word.sprite.destroy();
                this.words = this.words.filter(w => w !== word);
            }
        });

        // Actualizar textos de UI
        this.scoreText.setText(`Puntuación: ${this.score}`);
        this.levelText.setText(`Nivel: ${this.level}`);
    }
} 