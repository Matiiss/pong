import pygame

from . import enums, settings, types

SCENE_CHANGE = pygame.event.custom_type()


class Scene:
    def update(self, *args, **kwargs) -> None:
        ...

    def draw(self, surf: pygame.Surface) -> None:
        ...


def change_scene(scene: Scene, delay: int | None = None):
    event = pygame.event.Event(SCENE_CHANGE, {"scene": scene})
    if delay is None:
        pygame.event.post(event)
    else:
        pygame.time.set_timer(event, delay)


class SceneManager:
    def __init__(self) -> None:
        self.current_scene = None

    def set_scene(self, scene: Scene) -> None:
        self.current_scene = scene

    def update(self, *args, **kwargs) -> None:
        if self.current_scene is not None:
            self.current_scene.update(*args, **kwargs)

    def draw(self, surf: pygame.Surface) -> None:
        if self.current_scene is not None:
            self.current_scene.draw(surf)


class GameScene(Scene):
    def __init__(self) -> None:
        pass


class MainMenu(Scene):
    def __init__(self) -> None:
        pass
