import pygame

from . import enums, types, settings


class ScoreKeeper:
    def __init__(
        self,
        pos: types.Position,
        ball_group: pygame.sprite.GroupSingle,
        font: pygame.font.Font,
    ):
        self.pos = pygame.Vector2(pos)
        self.ball_group = ball_group
        self.font = font

        self.scored = False
        self.left_score = 0
        self.right_score = 0
        self.winner = False

    def update(self) -> None:
        if self.ball_group.sprite is None:
            return

        if self.ball_group.sprite.rect.left >= settings.WIDTH:
            self._update_score(enums.Side.LEFT)
        elif self.ball_group.sprite.rect.right <= 0:
            self._update_score(enums.Side.RIGHT)
        else:
            self.scored = False

    def _update_score(self, side: enums.Side) -> None:
        if self.scored:
            return

        if side == enums.Side.LEFT:
            self.left_score += 1
        elif side == enums.Side.RIGHT:
            self.right_score += 1
        self.scored = True

        if (
            self.right_score >= settings.WIN_SCORE
            or self.left_score >= settings.WIN_SCORE
        ):
            pygame.event.post(pygame.event.Event(enums.GameEvents.WIN_EVENT))
            self.winner = True
            return

        self.post_score_event()

    def draw(self, surf: pygame.Surface) -> None:
        if not self.winner:
            text = f"{self.left_score: >10}    {self.right_score: <10}"
        else:
            if self.left_score > self.right_score:
                text = f"{settings.WIN_TEXT: >30}    {settings.LOSE_TEXT: <30}"
            else:
                text = f"{settings.LOSE_TEXT: >30}    {settings.WIN_TEXT: <30}"

        text_surf = self.font.render(text, False, "white")
        rect = text_surf.get_rect(center=self.pos)
        surf.blit(text_surf, rect)

    @staticmethod
    def post_score_event() -> None:
        pygame.event.post(pygame.event.Event(enums.GameEvents.SCORE_EVENT))
