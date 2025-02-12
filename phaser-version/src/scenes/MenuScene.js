import BaseScene from './BaseScene';

export default class MenuScene extends BaseScene {
    constructor() {
        super('menu');
    }

    preload() {
        // Cargar assets del menú
        this.load.image('background', 'assets/images/backgrounds/castle.png');
        // Cargar música si existe
        this.load.audio('menu_music', 'assets/sounds/menu_music.mp3');
    }

    create() {
        super.create();

        // Agregar fondo
        this.add.image(400, 300, 'background').setScale(2);

        // Reproducir música del menú
        if (this.cache.audio.exists('menu_music')) {
            this.sound.play('menu_music', { loop: true });
        }

        // Crear título
        this.createText(400, 100, 'Menú Principal', '48px');

        // Crear botones
        const buttonSpacing = 80;
        const startY = 250;

        this.createButton(400, startY, 'Jugar', () => {
            this.game.changeScene(this, 'game');
        }).setOrigin(0.5);

        this.createButton(400, startY + buttonSpacing, 'Instrucciones', () => {
            this.game.changeScene(this, 'instructions');
        }).setOrigin(0.5);

        this.createButton(400, startY + buttonSpacing * 2, 'Salir', () => {
            // En un juego web, podríamos redirigir a otra página o mostrar un mensaje
            window.close();
        }).setOrigin(0.5);
    }
} 