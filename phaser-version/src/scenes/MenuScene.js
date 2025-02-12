import BaseScene from './BaseScene';
import { SCREEN_CONFIG } from '../config/gameConfig';

export default class MenuScene extends BaseScene {
    constructor() {
        super('menu');
        this.useCommonBackground = true;
    }

    preload() {
        super.preload();
        this.load.image('wizard', 'assets/images/characters/wizard.png');
        this.load.audio('menu_music', 'assets/sounds/music/menu.mp3');
    }

    create() {
        super.create();

        // Reproducir música del menú
        if (this.cache.audio.exists('menu_music')) {
            this.music = this.sound.add('menu_music', { 
                volume: 0.5,
                loop: true 
            });
            this.music.play();
        }

        // Agregar a Lupita en el centro
        const wizardHeight = 150;
        this.wizard = this.add.image(
            SCREEN_CONFIG.WIDTH / 2,
            SCREEN_CONFIG.HEIGHT / 2,
            'wizard'
        ).setOrigin(0.5);

        // Ajustar el tamaño de Lupita manteniendo la proporción
        const scale = wizardHeight / this.wizard.height;
        this.wizard.setScale(scale);

        // Animación de flotación de Lupita
        this.tweens.add({
            targets: this.wizard,
            y: '+=30',
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.InOut'
        });

        // Crear título con sombra
        const titleText = "LA AVENTURA MÁGICA DE LUPITA";
        
        // Sombra del título
        this.add.text(SCREEN_CONFIG.WIDTH / 2 + 2, 102, titleText, {
            fontFamily: '"Press Start 2P"',
            fontSize: '32px',
            color: '#000000',
            align: 'center'
        }).setOrigin(0.5);

        // Título principal
        this.add.text(SCREEN_CONFIG.WIDTH / 2, 100, titleText, {
            fontFamily: '"Press Start 2P"',
            fontSize: '32px',
            color: '#ffffff',
            align: 'center'
        }).setOrigin(0.5);

        // Texto de "Presiona ESPACIO" con efecto de parpadeo
        this.pressSpaceText = this.add.text(SCREEN_CONFIG.WIDTH / 2, SCREEN_CONFIG.HEIGHT - 50, 'PRESIONA ESPACIO', {
            fontFamily: '"Press Start 2P"',
            fontSize: '24px',
            color: '#ffffff',
            align: 'center'
        }).setOrigin(0.5);

        // Animación de parpadeo
        this.tweens.add({
            targets: this.pressSpaceText,
            alpha: 0,
            duration: 500,
            yoyo: true,
            repeat: -1
        });

        // Evento de teclado para ESPACIO
        this.input.keyboard.on('keydown-SPACE', () => {
            // No detenemos la música, igual que en la versión Python
            this.game.changeScene(this, 'instructions');
        });
    }
} 