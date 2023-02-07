import itertools

import pygame

from . import ball, enums, paddle, score_keeper, settings, types

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
        self.updating = True
        self.winner = False

        self.pause_surf = settings.FONT.render("Paused. Press Esc to resume...", False, "white")
        self.pause_rect = self.pause_surf.get_rect(center=(settings.WIDTH / 2, settings.HEIGHT / 2))

    def update(self, events: types.Events, dt: float) -> None:
        for event in events:
            if event.type == enums.GameEvents.SCORE_EVENT:
                self.ball_group.empty()
                pygame.time.set_timer(enums.GameEvents.RESPAWN_BALL, 1000, loops=1)
            elif event.type == enums.GameEvents.RESPAWN_BALL:
                self.ball_group.sprite = ball.Ball.spawn(self.paddle_group)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.updating = not self.updating
            elif event.type == enums.GameEvents.WIN_EVENT:
                self.updating = False
                self.winner = True
                change_scene(MainMenu(), 5000)

        if self.updating:
            self.paddle_group.update(events, dt)
            self.ball_group.update(events, dt)
            self.score_keeper.update()

    def draw(self, surf: pygame.Surface) -> None:
        self.draw_field(surf)
        self.paddle_group.draw(surf)
        self.ball_group.draw(surf)
        self.score_keeper.draw(surf)
        if not self.winner and not self.updating:
            surf.blit(self.pause_surf, self.pause_rect)

    @staticmethod
    def draw_field(surf: pygame.Surface, rect: pygame.Rect | None = None) -> None:
        if rect is None:
            rect = pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT)
        pygame.draw.rect(surf, "white", rect, width=2)
        pygame.draw.line(surf, "white", rect.midtop, rect.midbottom, width=1)


class MainMenu(Scene):
    def __init__(self) -> None:
        self.font = settings.FONT
        self.text_surf = self.font.render(
            "Welcome to pong! Press any key to start...", True, "white"
        )
        self.factor = itertools.cycle(
            map(lambda x: x / 500, list(range(450, 500, 1)) + list(range(500, 450, -1)))
        )
        self.pos = (settings.WIDTH / 2, settings.HEIGHT / 2)

    def update(self, events: types.Events, dt: float) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                change_scene(GameScene())

    def draw(self, surf: pygame.Surface) -> None:
        result = pygame.transform.smoothscale_by(self.text_surf, next(self.factor))
        rect = result.get_rect(center=self.pos)
        surf.blit(result, rect)
