import BaseScene from './BaseScene';

export default class ResultsScene extends BaseScene {
    constructor() {
        super('results');
    }

    preload() {
        this.load.image('background', 'assets/images/backgrounds/castle.png');
        this.load.image('star', 'assets/images/ui/star.png');
    }

    create() {
        super.create();

        // Agregar fondo
        this.add.image(400, 300, 'background').setScale(2);

        // Título
        this.createText(400, 100, '¡Nivel Completado!', '48px');

        // Mostrar puntuación
        this.createText(400, 200, `Puntuación: ${this.game.score}`, '32px');
        this.createText(400, 250, `Nivel: ${this.game.level}`, '32px');

        // Calcular estrellas basado en la puntuación
        const stars = Math.min(Math.floor(this.game.score / 1000), 3);
        
        // Mostrar estrellas
        for (let i = 0; i < 3; i++) {
            const star = this.add.image(300 + i * 100, 350, 'star')
                .setScale(0.5)
                .setAlpha(i < stars ? 1 : 0.3);
        }

        // Botones
        const buttonY = 450;
        const buttonSpacing = 80;

        this.createButton(400, buttonY, 'Siguiente Nivel', () => {
            this.game.level++;
            this.game.changeScene(this, 'game');
        }).setOrigin(0.5);

        this.createButton(400, buttonY + buttonSpacing, 'Volver al Menú', () => {
            this.game.changeScene(this, 'menu');
        }).setOrigin(0.5);

        // Guardar puntuación en el almacenamiento local
        this.saveScore();
    }

    saveScore() {
        try {
            const highScores = JSON.parse(localStorage.getItem('highScores') || '[]');
            highScores.push({
                score: this.game.score,
                level: this.game.level,
                date: new Date().toISOString()
            });
            
            // Ordenar por puntuación y mantener solo los mejores 10
            highScores.sort((a, b) => b.score - a.score);
            highScores.splice(10);
            
            localStorage.setItem('highScores', JSON.stringify(highScores));
        } catch (error) {
            console.error('Error saving score:', error);
        }
    }
} 