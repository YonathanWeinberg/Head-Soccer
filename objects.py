import pygame


class GameObject:
    def __init__(self, pos, image, screen):
        self.x, self.y = pos
        self.image = image
        self.screen = screen

    @property
    def coordinates(self):
        return self.x, self.y

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.coordinates
        return rect

    def get_moved_rect(self, vel_x=0, vel_y=0):
        x, y, w, h = self.rect
        return pygame.Rect(x + vel_x, y + vel_y, w, h)

    def draw(self):
        self.screen.blit(self.image, self.coordinates)


class MovingGameObject(GameObject):
    def __init__(self, start_pos, image, screen):
        self.start_x, self.start_y = start_pos

        super().__init__(start_pos, image, screen)

    def reset_coordinates(self):
        self.x, self.y = self.start_x, self.start_y

    def collides(self, obj: GameObject, vel_x=0, vel_y=0, obj_vel_x=0, obj_vel_y=0):
        self_rect = self.get_moved_rect(vel_x=vel_x, vel_y=vel_y)
        obj_rect = obj.get_moved_rect(vel_x=obj_vel_x, vel_y=obj_vel_y)
        return self_rect.colliderect(obj_rect)

    def collides_from_left(self, obj: GameObject, vels, obj_vels):
        collides = self.collides(obj, vel_x=vels[0], vel_y=vels[1], obj_vel_x=obj_vels[0], obj_vel_y=obj_vels[1])
        print(f"{vels = } {obj_vels = }")
        return collides and self.rect.left > obj.rect.left

    def collides_from_right(self, obj: GameObject, vels, obj_vels):
        collides = self.collides(obj, vel_x=vels[0], vel_y=vels[1], obj_vel_x=obj_vels[0], obj_vel_y=obj_vels[1])
        return collides and self.rect.right < obj.rect.right

    def collides_from_top(self, obj: GameObject, vels, obj_vels):
        collides = self.collides(obj, vel_x=vels[0], vel_y=vels[1], obj_vel_x=obj_vels[0], obj_vel_y=obj_vels[1])
        return collides and self.rect.top < obj.rect.top

    def collides_from_bottom(self, obj: GameObject, vels, obj_vels):
        collides = self.collides(obj, vel_x=vels[0], vel_y=vels[1], obj_vel_x=obj_vels[0], obj_vel_y=obj_vels[1])
        return collides and self.rect.bottom > obj.rect.bottom
