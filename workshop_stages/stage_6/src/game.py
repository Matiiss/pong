import pygame

from . import scenes, settings


class Game:
    def __init__(self, title: str = "Pong") -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT), flags=pygame.SCALED
        )
        pygame.display.set_caption(title)

        self.running = True

        self.clock = pygame.time.Clock()
        self.scene_manager = scenes.SceneManager()
        self.scene_manager.set_scene(scenes.GameScene())

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000
            self.screen.fill("black")

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == scenes.SCENE_CHANGE:
                    self.scene_manager.set_scene(event.scene)

            self.scene_manager.update(events, dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()
