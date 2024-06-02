import pygame

from objects import MovingGameObject
from globals import BALL_IMAGE, WIDTH, HEIGHT, PAD_X, PAD_Y, BLACK, WHITE
from player import Player
from goal import Goal


class Ball(MovingGameObject):

    radius = BALL_IMAGE.get_width() / 2
    start_pos = ((WIDTH - radius * 2)//2, HEIGHT * 0.3)
    start_velocities = (0, 0)
    kick_speeds = (15, -15)

    # mass = 100
    floor = HEIGHT * 0.75
    friction = 0.8

    gravity = 1         # Gravitational force
    g_count_max = 10    # How long does the fall take

    bounce_stop_speed = 1
    x_stop_speed = 0.4
    bounciness_x = 0.8
    bounciness_y = 0.8

    def __init__(self, screen):
        self.vel_x, self.vel_y = Ball.start_velocities
        self.new_vel_x, self.new_vel_y = self.vel_x, self.vel_y
        self.gravity_count = 0
        # self.p_bounced = False

        super().__init__(Ball.start_pos, BALL_IMAGE, screen)

    @property
    def center_x(self):
        return self.x + self.radius

    @property
    def center_y(self):
        return self.y + self.radius

    def bounce_x(self, bounciness=None):
        if bounciness is None:
            bounciness = Ball.bounciness_x
        # self.new_vel_x += -Ball.friction if self.new_vel_x > 0 else Ball.friction
        self.new_vel_x *= -1 * bounciness

    def bounce_y(self, bounciness=None):
        if bounciness is None:
            bounciness = Ball.bounciness_y
        self.new_vel_y *= -1 * bounciness

    def kicked(self, player: Player):
        self.new_vel_x = player.front_direction * Ball.kick_speeds[0]
        self.new_vel_y = Ball.kick_speeds[1]

    def handle_gravity_and_bounce(self):
        # If touches ceiling
        if self.center_y + self.vel_y <= PAD_Y:
            self.y -= self.vel_y
            self.bounce_y()

        # If touches floor
        if self.center_y + self.vel_y >= self.floor:

            # If needs to bounce
            if self.vel_y > self.bounce_stop_speed:
                self.bounce_y()

            # If doesn't need to bounce
            else:
                self.new_vel_y = 0

        # If ball is in the air
        else:
            if self.gravity_count == 0:
                self.new_vel_y += self.gravity
            elif self.gravity_count == Ball.g_count_max:
                self.gravity_count = 0
            else:
                self.gravity_count += 1

    def handle_player_collision(self, player: Player):
        if player.front_collides(self) and player.is_kicking:
            self.kicked(player)

        elif player.head_collides(self):
            self.bounce_y(player.bounciness)

        elif player.legs_collide(self):
            pass

        elif player.front_collides(self) or player.back_collides(self):
            if self.vel_x: #and not self.p_bounced:
                self.bounce_x(player.bounciness)
                self.p_bounced = True
            else:
                if player.front_collides(self):
                    self.new_vel_x = player.front_direction * player.vel * 1.1 # * (player.x_moving_direction if player.x_moving_direction else 1)
                else:
                    self.new_vel_x = - player.front_direction * player.vel * 1.1 # * (player.x_moving_direction if player.x_moving_direction else 1)

        else:
            self.p_bounced = False

    def handle_walls_collision(self):
        collision_right_wall = self.rect.right + self.vel_x >= WIDTH - PAD_X
        collision_left_wall = self.rect.left + self.vel_x <= PAD_X
        if collision_right_wall or collision_left_wall:
            self.bounce_x()
            self.bounce_y(1)

    def handle_goals_collision(self, goal1: Goal, goal2: Goal):
        if self.get_moved_rect().colliderect(goal1.rect) or self.get_moved_rect().colliderect(goal2.rect):
            if self.rect.top > Goal.right_goal_pos[1]:
                if self.get_moved_rect().colliderect(goal1.rect):
                    return goal2.side
                return goal1.side
            else:
                self.bounce_y()

    def handle_min_x_speed(self):
        if self.new_vel_x <= Ball.x_stop_speed:
            self.new_vel_x = 0

    def update_position(self):
        self.y += self.new_vel_y
        self.x += self.new_vel_x

    def update_velocities(self):
        self.vel_x = self.new_vel_x
        self.vel_y = self.new_vel_y

    def reset_velocities(self):
        self.vel_x, self.vel_y = Ball.start_velocities
        self.new_vel_x, self.new_vel_y = self.vel_x, self.vel_y
