import BaseScene from './BaseScene';

export default class InstructionsScene extends BaseScene {
    constructor() {
        super('instructions');
    }

    preload() {
        this.load.image('background', 'assets/images/backgrounds/magic_school.png');
    }

    create() {
        super.create();

        // Agregar fondo
        this.add.image(400, 300, 'background').setScale(2);

        // Título
        this.createText(400, 80, 'Instrucciones', '48px');

        // Instrucciones
        const instructions = [
            'Escribe las palabras que aparecen en pantalla',
            'Cada palabra correcta suma puntos',
            'Las palabras incorrectas restan vida',
            'Completa el nivel antes de quedarte sin vida',
            'Presiona ESC para volver al menú',
            'Presiona ESPACIO para comenzar'
        ];

        instructions.forEach((text, index) => {
            this.createText(400, 180 + index * 60, text, '24px');
        });

        // Botón para volver al menú
        this.createButton(400, 550, 'Volver al Menú', () => {
            this.game.changeScene(this, 'menu');
        }).setOrigin(0.5);

        // Evento de teclado para comenzar el juego
        this.input.keyboard.once('keydown-SPACE', () => {
            this.game.changeScene(this, 'game');
        });
    }
} 