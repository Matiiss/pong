import pygame

from . import enums, types, settings


class Paddle(pygame.sprite.Sprite):
    image = pygame.Surface((5, 25))
    image.fill("white")

    velocity = pygame.Vector2(0, 170)

    # create a rectangle for each momentum value
    momentum_rects: list = [
        [(0, idx * 5, 5, 5), value] for idx, value in enumerate(settings.BALL_MOMENTA)
    ]

    def __init__(self, pos: types.Position, controls: dict[enums.MoveDirection, int]):
        super().__init__()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.velocity = Paddle.velocity.copy()
        self.controls = controls

        # create Rect objects from momentum rects
        self.momentum_rects = [
            [pygame.Rect(rect), momentum] for rect, momentum in self.momentum_rects
        ]

    def update(self, events: types.Events, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dy = 0

        if keys[self.controls[enums.MoveDirection.UP]]:
            dy -= self.velocity.y * dt
        if keys[self.controls[enums.MoveDirection.DOWN]]:
            dy += self.velocity.y * dt

        # collisions
        if self.rect.top + dy < 0:
            dy = 0 - self.rect.top
        elif self.rect.bottom + dy > settings.HEIGHT:
            dy = settings.HEIGHT - self.rect.bottom

        self.pos.y += dy
        self.rect.center = self.pos
        for idx, (rect, _) in enumerate(self.momentum_rects):
            rect.x = self.rect.x
            rect.y = self.rect.top + idx * 5
