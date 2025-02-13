import BaseScene from './BaseScene';
import { SCREEN_CONFIG } from '../config/gameConfig';

export default class InstructionsScene extends BaseScene {
    constructor() {
        super('instructions');
        this.useCommonBackground = true;
        this.instructions = [
            "¡BIENVENIDO A LA AVENTURA!",
            "ESCRIBE LAS PALABRAS QUE CAEN\nY PRESIONA ENTER\n ANTES QUE TOQUEN LA LÍNEA ROJA",
            "USA LOS DEDOS CORRECTOS",
            "¡NO DEJES LAS PALABRAS\nTOQUEN LA LÍNEA ROJA!"
        ];
        this.particles = [];
    }

    preload() {
        super.preload();
        this.load.image('wizard', 'assets/images/characters/wizard.png');
        this.load.image('magic_effect', 'assets/images/effects/magic_effect.png');
    }

    create() {
        super.create();

        // Agregar a Lupita en el centro
        const wizardHeight = 150;
        this.wizard = this.add.image(
            SCREEN_CONFIG.WIDTH / 2,
            SCREEN_CONFIG.HEIGHT / 2,
            'wizard'
        ).setOrigin(0.5);

        // Ajustar el tamaño de Lupita
        const scale = wizardHeight / this.wizard.height;
        this.wizard.setScale(scale);

        // Animación de flotación
        this.tweens.add({
            targets: this.wizard,
            y: '+=30',
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.InOut'
        });

        // Crear partículas mágicas
        for (let i = 0; i < 30; i++) {
            const particle = this.add.image(
                Phaser.Math.Between(0, SCREEN_CONFIG.WIDTH),
                Phaser.Math.Between(0, SCREEN_CONFIG.HEIGHT),
                'magic_effect'
            ).setAlpha(Phaser.Math.FloatBetween(0.2, 0.8))
             .setScale(Phaser.Math.FloatBetween(0.1, 0.3));
            
            this.particles.push({
                sprite: particle,
                speed: Phaser.Math.FloatBetween(0.5, 2.0),
                angle: Phaser.Math.FloatBetween(0, 360)
            });
        }

        // Panel semi-transparente para las instrucciones
        const panelWidth = SCREEN_CONFIG.WIDTH * 0.8;
        const panelHeight = SCREEN_CONFIG.HEIGHT * 0.7;
        const panel = this.add.rectangle(
            SCREEN_CONFIG.WIDTH / 2,
            SCREEN_CONFIG.HEIGHT / 2,
            panelWidth,
            panelHeight,
            0x000000,
            0.5
        );

        // Configuración simple de espaciado
        const fontSize = 20;
        const lineSpacing = 35;
        const fixedParagraphHeight = 100; // Altura fija para cada párrafo

        // Calcular altura total y posición inicial
        const totalHeight = fixedParagraphHeight * this.instructions.length;
        let startY = panel.y - (totalHeight / 2) + (fixedParagraphHeight / 2);

        // Agregar instrucciones
        this.instructions.forEach(instruction => {
            this.add.text(SCREEN_CONFIG.WIDTH / 2, startY, instruction, {
                fontFamily: '"Press Start 2P"',
                fontSize: `${fontSize}px`,
                color: '#ffffff',
                align: 'center',
                lineSpacing: lineSpacing / 2
            }).setOrigin(0.5);
            
            // Simplemente avanzar una altura fija para cada párrafo
            startY += fixedParagraphHeight;
        });

        // Texto de "Presiona ESPACIO"
        const pressSpaceText = this.add.text(
            SCREEN_CONFIG.WIDTH / 2,
            SCREEN_CONFIG.HEIGHT - 50,
            'PRESIONA ESPACIO PARA COMENZAR',
            {
                fontFamily: '"Press Start 2P"',
                fontSize: '20px',
                color: '#ffffff',
                align: 'center'
            }
        ).setOrigin(0.5);

        // Animación de parpadeo
        this.tweens.add({
            targets: pressSpaceText,
            alpha: 0,
            duration: 500,
            yoyo: true,
            repeat: -1
        });

        // Evento de teclado para ESPACIO
        this.input.keyboard.on('keydown-SPACE', () => {
            this.game.changeScene(this, 'game');
        });
    }

    update() {
        // Actualizar partículas
        this.particles.forEach(p => {
            p.angle = (p.angle + p.speed) % 360;
            const centerX = this.wizard.x;
            const centerY = this.wizard.y;
            const radius = 50 + Math.sin(p.angle * Math.PI / 180) * 20;
            
            p.sprite.x = centerX + Math.cos(p.angle * Math.PI / 180) * radius;
            p.sprite.y = centerY + Math.sin(p.angle * Math.PI / 180) * radius;
            p.sprite.alpha = 0.5 + Math.sin(this.time.now * 0.001 + p.angle) * 0.5;
        });
    }
} 