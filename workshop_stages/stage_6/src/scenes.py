import pygame

from . import enums, settings, types, paddle, ball, score_keeper

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

        self.ball_group = pygame.sprite.GroupSingle()
        pygame.time.set_timer(enums.GameEvents.RESPAWN_BALL, 1000, loops=1)

        self.score_keeper = score_keeper.ScoreKeeper(
            (settings.WIDTH / 2, 25), self.ball_group, settings.FONT
        )

    def update(self, events: types.Events, dt: float) -> None:
        for event in events:
            if event.type == enums.GameEvents.SCORE_EVENT:
                self.ball_group.empty()
                pygame.time.set_timer(enums.GameEvents.RESPAWN_BALL, 1000, loops=1)
            elif event.type == enums.GameEvents.RESPAWN_BALL:
                self.ball_group.sprite = ball.Ball.spawn(self.paddle_group)
            elif event.type == enums.GameEvents.WIN_EVENT:
                pass

        self.paddle_group.update(events, dt)
        self.ball_group.update(events, dt)
        self.score_keeper.update()

    def draw(self, surf: pygame.Surface) -> None:
        self.paddle_group.draw(surf)
        self.ball_group.draw(surf)
        self.score_keeper.draw(surf)


class MainMenu(Scene):
    def __init__(self) -> None:
        pass
