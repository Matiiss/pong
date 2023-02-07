import enum

import pygame


class MoveDirection(enum.Enum):
    UP = enum.auto()  # noqa
    DOWN = enum.auto()  # noqa


class Side(enum.Enum):
    LEFT = enum.auto()  # noqa
    RIGHT = enum.auto()  # noqa


class GameEvents:
    SCORE_EVENT: int = pygame.event.custom_type()
    RESPAWN_BALL: int = pygame.event.custom_type()
    WIN_EVENT: int = pygame.event.custom_type()
