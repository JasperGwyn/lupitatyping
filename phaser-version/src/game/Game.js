export default class Game {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.running = true;
    }

    changeScene(scene, sceneName) {
        // Manejar la lógica de cambio de escena
        if (sceneName === 'game') {
            // Detener la música si existe
            if (scene.sound && scene.sound.music) {
                scene.sound.music.stop();
            }
        }
        
        // Guardar puntuación y nivel antes de cambiar a resultados
        if (sceneName === 'results') {
            this.score = scene.score || 0;
            this.level = scene.level || 1;
        }

        // Iniciar la nueva escena y detener la actual
        scene.scene.start(sceneName);
        scene.scene.stop(scene.scene.key);
    }
} 