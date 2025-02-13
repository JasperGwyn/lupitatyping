changeScene(currentScene, newSceneKey, useTransition = true) {
    if (useTransition) {
        currentScene.cameras.main.fadeOut(500);
        currentScene.cameras.main.once('camerafadeoutcomplete', () => {
            currentScene.scene.start(newSceneKey);
        });
    } else {
        currentScene.scene.start(newSceneKey);
    }
} 

scene: [IntroScene, MenuScene, InstructionsScene, GameScene],
// Asegúrate que IntroScene sea la primera escena 