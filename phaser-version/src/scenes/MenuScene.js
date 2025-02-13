import BaseScene from './BaseScene';
import { SCREEN_CONFIG } from '../config/gameConfig';

export default class MenuScene extends BaseScene {
    constructor() {
        super('menu');
        this.useCommonBackground = false;
    }

    preload() {
        super.preload();
        this.load.audio('menu_music', 'assets/sounds/music/menu.mp3');
    }

    create() {
        // No llamamos a super.create() porque no queremos el fondo
        // La escena de intro seguirá visible debajo
        
        // Reproducir música del menú
        if (this.cache.audio.exists('menu_music')) {
            this.music = this.sound.add('menu_music', { 
                volume: 0.5,
                loop: true 
            });
            this.music.play();
        }

        // Crear título con sombra
        const titleText = "LA AVENTURA\nMÁGICA DE LUPITA";
        
        // Sombra del título
        const titleShadow = this.add.text(SCREEN_CONFIG.WIDTH / 2 + 2, 96, titleText, {
            fontFamily: '"Press Start 2P"',
            fontSize: '40px',
            color: '#000000',
            align: 'center',
            lineSpacing: 10
        }).setOrigin(0.5).setAlpha(0);

        // Título principal
        const titleMain = this.add.text(SCREEN_CONFIG.WIDTH / 2, 94, titleText, {
            fontFamily: '"Press Start 2P"',
            fontSize: '40px',
            color: '#ffffff',
            align: 'center',
            lineSpacing: 10
        }).setOrigin(0.5).setAlpha(0);

        // Fade in del título
        this.tweens.add({
            targets: [titleShadow, titleMain],
            alpha: 1,
            duration: 1000
        });

        // Evento de teclado para ESPACIO
        this.input.keyboard.on('keydown-SPACE', () => {
            this.game.changeScene(this, 'instructions');
        });

        // Iniciar esta escena en modo transparente
        this.cameras.main.setBackgroundColor('rgba(0,0,0,0)');
    }
} 