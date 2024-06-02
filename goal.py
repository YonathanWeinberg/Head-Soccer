import pygame

from globals import RIGHT_GOAL_IMAGE, LEFT_GOAL_IMAGE, WIDTH, HEIGHT
from objects import GameObject


class Goal(GameObject):
    right_goal_image = pygame.transform.scale(RIGHT_GOAL_IMAGE, (RIGHT_GOAL_IMAGE.get_width()*0.75,
                                                                 RIGHT_GOAL_IMAGE.get_height()))
    left_goal_image = pygame.transform.scale(LEFT_GOAL_IMAGE, (RIGHT_GOAL_IMAGE.get_width() * 0.75,
                                                               LEFT_GOAL_IMAGE.get_height()))

    goal_y_weight = 1.9    # 1.75 / 1.67
    right_goal_pos = (0, HEIGHT // goal_y_weight)
    left_goal_pos = (WIDTH - right_goal_image.get_width(), HEIGHT // goal_y_weight)

    def __init__(self, side, screen):
        self.side = side
        pos = Goal.right_goal_pos if side == "right" else Goal.left_goal_pos
        image = Goal.right_goal_image if side == "right" else Goal.left_goal_image
        super().__init__(pos, image, screen)

    @property
    def rect(self):
        y = self.y
        w = self.image.get_width()
        h = self.image.get_height()
        x = (WIDTH - w) if self.side == "right" else 0
        return pygame.Rect(x, y, w, h)

    @classmethod
    def right_goal(cls, goal1, goal2):
        if goal1.rect.right > goal2.rect.right:
            return goal1
        return goal2

    @classmethod
    def left_goal(cls, goal1, goal2):
        if goal1.rect.left < goal2.rect.left:
            return goal1
        return goal2

    def draw(self):
        # pygame.draw.rect(self.screen, BLACK, self.rect)
        super().draw()
