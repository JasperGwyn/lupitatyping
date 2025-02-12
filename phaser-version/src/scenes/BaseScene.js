export default class BaseScene extends Phaser.Scene {
    constructor(key) {
        super(key);
    }

    init() {
        // Asegurarnos de que tenemos acceso al juego
        this.game = window.game;
    }

    preload() {
        if (!this.textures.exists('castle')) {
            // Cargar todos los assets necesarios para el fondo
            this.load.image('castle', 'assets/images/backgrounds/castle.png');
            this.load.image('sun', 'assets/images/backgrounds/sun.png');
            this.load.image('cloud1', 'assets/images/backgrounds/cloud1.png');
            this.load.image('tree1', 'assets/images/backgrounds/tree1.png');
            this.load.image('tree2', 'assets/images/backgrounds/tree2.png');
            this.load.image('fence', 'assets/images/backgrounds/fence.png');
            this.load.image('grass1', 'assets/images/backgrounds/grass1.png');
            this.load.image('grass2', 'assets/images/backgrounds/grass2.png');
            this.load.image('grass3', 'assets/images/backgrounds/grass3.png');
        }
    }

    create() {
        // Configurar eventos de teclado globales
        this.input.keyboard.on('keydown', this.handleKeyDown, this);
        
        // Inicializar el fondo común si la escena lo requiere
        if (this.useCommonBackground) {
            this.initBackground();
        }
    }

    initBackground() {
        // Fondo azul cielo
        this.add.rectangle(0, 0, this.cameras.main.width, this.cameras.main.height, 0x87CEEB)
            .setOrigin(0);

        // Sol con animación
        this.sun = this.add.image(50, 50, 'sun')
            .setDisplaySize(100, 100);
        
        // Animación del sol
        this.tweens.add({
            targets: this.sun,
            y: '+=20',
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.InOut'
        });

        // Nubes
        this.clouds = [];
        for (let i = 0; i < 5; i++) {
            const width = Phaser.Math.Between(150, 250);
            const height = Phaser.Math.Between(75, 125);
            const cloud = this.add.image(
                Phaser.Math.Between(0, this.cameras.main.width),
                Phaser.Math.Between(30, 200),
                'cloud1'
            ).setDisplaySize(width, height);
            
            cloud.speed = Phaser.Math.FloatBetween(0.3, 1.0);
            this.clouds.push(cloud);
        }

        // Castillo (mitad de la altura de la pantalla)
        const castleHeight = this.cameras.main.height / 2;
        this.castle = this.add.image(this.cameras.main.width / 2, this.cameras.main.height, 'castle')
            .setOrigin(0.5, 1)
            .setDisplaySize(castleHeight * 1.5, castleHeight); // Mantener proporción aproximada

        // Árboles
        const treeHeight = 200;
        this.add.image(this.cameras.main.width * 0.05, this.cameras.main.height, 'tree1')
            .setOrigin(0, 1)
            .setDisplaySize(treeHeight * 0.75, treeHeight);
        
        this.add.image(this.cameras.main.width * 0.8, this.cameras.main.height, 'tree2')
            .setOrigin(0, 1)
            .setDisplaySize(treeHeight * 0.75, treeHeight);

        // Cerca
        const fenceHeight = 45;
        const fenceWidth = fenceHeight * 0.8;
        const fenceSpacing = fenceWidth - 5; // Espacio entre cercas con superposición
        const numFences = Math.ceil(this.cameras.main.width / fenceSpacing) + 1; // +1 para asegurar cobertura completa
        
        for (let i = 0; i < numFences; i++) {
            this.add.image(i * fenceSpacing, this.cameras.main.height, 'fence')
                .setOrigin(0, 1)
                .setDisplaySize(fenceWidth, fenceHeight);
        }

        // Pasto
        for (let i = 0; i < 10; i++) {
            const grassType = `grass${Phaser.Math.Between(1, 3)}`;
            const xPos = i * (this.cameras.main.width / 10) + Phaser.Math.Between(-20, 20);
            this.add.image(xPos, this.cameras.main.height, grassType)
                .setOrigin(0, 1)
                .setDisplaySize(25, 12);
        }

        // Evento de update para las nubes
        this.events.on('update', this.updateBackground, this);
    }

    updateBackground() {
        // Mover las nubes
        if (this.clouds) {
            this.clouds.forEach(cloud => {
                cloud.x -= cloud.speed;
                if (cloud.x + cloud.width < -200) {
                    cloud.x = this.cameras.main.width + Phaser.Math.Between(100, 300);
                    cloud.y = Phaser.Math.Between(30, 200);
                }
            });
        }
    }

    handleKeyDown(event) {
        // Manejar tecla ESC para volver al menú
        if (event.keyCode === Phaser.Input.Keyboard.KeyCodes.ESC) {
            this.game.changeScene(this, 'menu');
        }
    }

    // Métodos de utilidad para crear elementos de UI con estilos mejorados
    createButton(x, y, text, callback) {
        const padding = { x: 20, y: 10 };
        const button = this.add.container(x, y);

        // Crear el fondo del botón
        const background = this.add.rectangle(0, 0, 200, 50, 0x333333)
            .setOrigin(0.5);

        // Crear el texto del botón con mejor estilo
        const buttonText = this.add.text(0, 0, text, {
            fontFamily: 'Roboto Mono',
            fontSize: '24px',
            fill: '#fff',
            padding: padding
        }).setOrigin(0.5);

        // Ajustar el tamaño del fondo al texto
        background.width = buttonText.width + padding.x * 2;
        background.height = buttonText.height + padding.y * 2;

        // Agregar elementos al contenedor
        button.add([background, buttonText]);

        // Hacer el botón interactivo
        button.setSize(background.width, background.height);
        button.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                background.setFillStyle(0x444444);
                buttonText.setStyle({ fill: '#ffff00' });
            })
            .on('pointerout', () => {
                background.setFillStyle(0x333333);
                buttonText.setStyle({ fill: '#ffffff' });
            })
            .on('pointerdown', () => {
                background.setFillStyle(0x222222);
                this.time.delayedCall(100, callback);
            });

        return button;
    }

    createText(x, y, text, fontSize = '32px', shadow = true) {
        const textStyle = {
            fontFamily: 'Roboto Mono',
            fontSize: fontSize,
            fill: '#fff',
            padding: { x: 20, y: 10 }
        };

        if (shadow) {
            textStyle.shadow = {
                offsetX: 2,
                offsetY: 2,
                color: '#000',
                blur: 3,
                fill: true
            };
        }

        return this.add.text(x, y, text, textStyle).setOrigin(0.5);
    }

    // Método para crear fondos con degradado
    createGradientBackground(fromColor, toColor) {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const texture = this.textures.createCanvas('gradientTexture', width, height);
        const context = texture.getContext();
        
        const gradient = context.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, fromColor);
        gradient.addColorStop(1, toColor);
        
        context.fillStyle = gradient;
        context.fillRect(0, 0, width, height);
        
        texture.refresh();
        
        return this.add.image(width/2, height/2, 'gradientTexture');
    }
} 