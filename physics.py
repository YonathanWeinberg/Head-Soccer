import pygame

from objects import MovingGameObject
from player import Player


class Physics:

    
    def right_collides(self, player: Player, obj2: MovingGameObject):
        obj1_rect = player.get_moved_rect(player.vel_x, player.vel_y)
        obj2_rect = obj1.get_moved_rect(obj2.vel_x, obj2.vel_y)
        check = obj1.rect.get_width() -
        return obj1_rect.colliderect(obj2_rect) or



