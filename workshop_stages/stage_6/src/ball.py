import random

import pygame

from . import types, settings


class Ball(pygame.sprite.Sprite):
    image = pygame.Surface((4, 4), flags=pygame.SRCALPHA)
    pygame.draw.circle(image, "white", (2, 2), 2)

    velocity = pygame.Vector2(150)

    def __init__(
        self,
        pos: types.Position,
        initial_direction: pygame.Vector2,
        paddles: pygame.sprite.Group,
    ):
        super().__init__()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.velocity = Ball.velocity.elementwise() * initial_direction
        self.paddles = paddles

    def update(self, events: types.Events, dt: float) -> None:
        dx, dy = self.velocity * dt

        # table boundaries
        if self.rect.top + dy < 0:
            dy = 0 - self.rect.top
            self.velocity.y *= -1
        elif self.rect.bottom + dy > settings.HEIGHT:
            dy = settings.HEIGHT - self.rect.bottom
            self.velocity.y *= -1

        # paddle collisions
        projection = self.rect.move(dx, dy)
        for paddle in self.paddles:
            if projection.colliderect(paddle.rect):
                if dx > 0:
                    dx = paddle.rect.left - projection.right
                else:
                    dx = paddle.rect.right - projection.left
                center = pygame.Vector2(projection.center)
                dct = {
                    center.distance_squared_to(rect.center): momentum
                    for rect, momentum in paddle.momentum_rects
                }
                self.velocity.y = Ball.velocity.y * dct[min(dct)]
                self.velocity.x *= -1
                break

        self.pos += (dx, dy)
        self.rect.center = round(self.pos.x), round(self.pos.y)

    @classmethod
    def spawn(cls, paddles) -> "Ball":
        return Ball(
            (settings.WIDTH / 2, settings.HEIGHT / 2),
            pygame.Vector2(
                random.choice([-1, 1]), random.choice(settings.BALL_MOMENTA)
            ),
            paddles,
        )
