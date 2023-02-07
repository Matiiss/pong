import pygame

from . import enums, settings, types, paddle

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
        self.paddle_group = pygame.sprite.Group()
        self.paddle_group.add(
            paddle.Paddle(  # noqa
                (settings.PADDLE_OFFSET, settings.HEIGHT / 2),
                {
                    enums.MoveDirection.UP: pygame.K_w,
                    enums.MoveDirection.DOWN: pygame.K_s,
                },
            )
        )
        self.paddle_group.add(
            paddle.Paddle(  # noqa
                (settings.WIDTH - settings.PADDLE_OFFSET, settings.HEIGHT / 2),
                {
                    enums.MoveDirection.UP: pygame.K_UP,
                    enums.MoveDirection.DOWN: pygame.K_DOWN,
                },
            )
        )

    def update(self, events: types.Events, dt: float) -> None:
        self.paddle_group.update(events, dt)

    def draw(self, surf: pygame.Surface) -> None:
        self.paddle_group.draw(surf)


class MainMenu(Scene):
    def __init__(self) -> None:
        pass
