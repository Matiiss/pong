import pygame

pygame.font.init()

WIDTH, HEIGHT = 640, 360
FPS = 60

PADDLE_OFFSET = 25
BALL_MOMENTA = [-1, -0.5, 0, 0.5, 1]

FONT = pygame.font.Font(None, 32)
WIN_TEXT = "YOU WIN!"
LOSE_TEXT = "YOU LOSE!"
WIN_SCORE = 10
