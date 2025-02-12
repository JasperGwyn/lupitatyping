import Phaser from 'phaser';
import Game from './game/Game';
import MenuScene from './scenes/MenuScene';
import GameScene from './scenes/GameScene';
import ResultsScene from './scenes/ResultsScene';
import IntroScene from './scenes/IntroScene';
import InstructionsScene from './scenes/InstructionsScene';
import { SCREEN_CONFIG } from './config/gameConfig';

// Crear instancia del juego primero
window.game = new Game();

// Configuración global del juego
const config = {
    type: Phaser.AUTO,
    width: SCREEN_CONFIG.WIDTH,
    height: SCREEN_CONFIG.HEIGHT,
    pixelArt: true,  // Esto asegura que no se aplique suavizado a los píxeles
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    render: {
        antialias: false,
        pixelArt: true,
        roundPixels: true
    },
    scene: [IntroScene, MenuScene, GameScene, InstructionsScene, ResultsScene]
};

// Crear instancia de Phaser
new Phaser.Game(config); 