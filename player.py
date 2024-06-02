from objects import MovingGameObject, GameObject
from globals import RIGHT_CHAR_IMAGE, RIGHT_CHAR_KICK1_IMAGE, RIGHT_CHAR_KICK2_IMAGE, \
                    LEFT_CHAR_IMAGE, LEFT_CHAR_KICK1_IMAGE, LEFT_CHAR_KICK2_IMAGE, \
                    WIDTH, HEIGHT, BLACK, WHITE, player_moves, current_move


class Player(MovingGameObject):
    right_char_images = (RIGHT_CHAR_IMAGE, RIGHT_CHAR_KICK1_IMAGE, RIGHT_CHAR_KICK2_IMAGE)
    left_char_images = (LEFT_CHAR_IMAGE, LEFT_CHAR_KICK1_IMAGE, LEFT_CHAR_KICK2_IMAGE)

    players_start_y = (HEIGHT - right_char_images[0].get_height()) * 0.77  # 0.75
    right_start_pos = (855, players_start_y)
    left_start_pos = (255, players_start_y)

    jump_count = 12
    kick_count = 10

    bounciness = 1.01

    def __init__(self, side, screen):
        self.side = side

        if side == "right":
            start_pos: tuple = Player.right_start_pos
            self.images: tuple = Player.right_char_images
            self.front_direction: int = -1
        else:
            start_pos: tuple = Player.left_start_pos
            self.images: tuple = Player.left_char_images
            self.front_direction: int = 1

        self.vel = 10
        self.x_moving_direction = 0

        self.is_jumping = False
        self.jump_count = Player.jump_count        # How long will the jump be (10)
        self.jump_increment = 0.8                  # How high will the jump be / acceleration (1)
        self.jump_delta = 0
        self.height_delta = 0

        self.is_kicking = False
        self.is_kicked = False                     # Has the ball already been kicked
        self.kick_count = 0

        self.image_index = 0
        image = self.images[0]

        super().__init__(start_pos, image, screen)

    @property
    def vel_y(self):
        if self.is_jumping is False:
            return 0
        return -0.5 * (self.jump_count * abs(self.jump_count)) * self.jump_increment

    @property
    def vel_x(self):
        return self.vel * self.x_moving_direction

    @property
    def current_vels(self):
        return self.vel_x, self.vel_y

    def switch_image(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
        else:
            self.image_index = 0

        self.image = self.images[self.image_index]

    def collide(self, obj):
        player_rect = self.get_moved_rect(self.vel_x, self.vel_y)
        obj_rect = obj.get_moved_rect(obj.vel_x, obj.vel_y)
        print(player_rect.colliderect(obj_rect), obj_rect, player_rect)
        return player_rect.colliderect(obj_rect)

    # For goal/wall collision
    def collide_right_wall(self, right_goal: GameObject):
        return self.rect.right + self.vel > right_goal.rect.left

    def collide_left_wall(self, left_goal: GameObject):
        return self.rect.left - self.vel < left_goal.rect.right

    # For opponent collision
    def collides_from_left(self, obj: MovingGameObject, move=True):
        vel_x = - self.vel if move else self.x_moving_direction * self.vel
        player_rect = self.get_moved_rect(vel_x, self.vel_y)
        opponent_rect = obj.get_moved_rect(obj.vel_x, obj.vel_y)
        # check = False
        # if pnz(vel_x) == - pnz(obj.vel_x) and vel_x:
        #     # delta_vel = obj.vel_x - (-self.vel if move else 0)
        #     delta_dest = abs(self.rect.left - obj.rect.right)
        #     partially_moved = obj.get_moved_rect(delta_dest + 1)
        #     check = partially_moved.colliderect(self.rect)
        #     if check:
        #         print("opposite_directions (lp) collide")
        if player_rect.colliderect(opponent_rect):
            print("collide l")
        return player_rect.colliderect(opponent_rect) # or check

    def collides_from_right(self, obj: MovingGameObject, move=True):
        vel_x = self.vel if move else self.x_moving_direction * self.vel
        player_rect = self.get_moved_rect(vel_x, self.vel_y)
        opponent_rect = obj.get_moved_rect(obj.vel_x, obj.vel_y)

        # check = False
        # if pnz(vel_x) == - pnz(obj.vel_x) and vel_x:
        #     # delta_vel = obj.vel_x - (-self.vel if move else 0)
        #     delta_dest = abs(self.rect.left - obj.rect.right)
        #     partially_moved = self.get_moved_rect(delta_dest + 1)
        #     check = partially_moved.colliderect(obj.rect)
        #     if check:
        #         print("opposite_directions (rp) collide")

        # delta_vel = (self.vel if move else 0) - obj.vel_x
        # delta_dest = abs(self.rect.right - obj.rect.left)
        # partially_moved = self.get_moved_rect(vel_x=delta_dest+0.1)
        # check = partially_moved.colliderect(obj.rect) #and abs(delta_vel) >= delta_dest
        # # check_moved = player_rect.right >= opponent_rect.left and self.rect.right <= opponent_rect.left
        if player_rect.colliderect(opponent_rect):
            print("collide r")
        return player_rect.colliderect(opponent_rect) # r check

    def collides_from_bottom(self, obj: MovingGameObject):
        player_rect = self.get_moved_rect(self.vel_x, self.vel_y)
        opponent_rect = obj.get_moved_rect(obj.vel_x, obj.vel_y)
        # check_moved = player_rect.bottom >= opponent_rect.top and self.rect.bottom <= opponent_rect.top
        return player_rect.colliderect(opponent_rect) or player_rect.colliderect(obj.rect) \
               or self.rect.colliderect(opponent_rect)

    def collides_from_top(self, obj: MovingGameObject):
        player_rect = self.get_moved_rect(self.vel_x, -self.vel_y)
        opponent_rect = obj.get_moved_rect(obj.vel_x, obj.vel_y)
        # check_moved = player_rect.top <= opponent_rect.bottom and self.rect.top >= opponent_rect.bottom
        return player_rect.colliderect(opponent_rect) or player_rect.colliderect(obj.rect) \
               or self.rect.colliderect(opponent_rect)

    # For ball collision
    def front_collides(self, obj: MovingGameObject):
        if self.side == 'right':
            return self.collides_from_left(obj)
        return self.collides_from_right(obj)

    def back_collides(self, obj: MovingGameObject):
        if self.side == 'right':
            return self.collides_from_right(obj)
        return self.collides_from_left(obj)

    def head_collides(self, obj: MovingGameObject):
        return self.collides_from_top(obj)

    def legs_collide(self, obj: MovingGameObject):
        return self.collides_from_bottom(obj)

    # Player movement
    def move_left(self, opponent, left_goal):
        collisions = [self.collide_left_wall(left_goal),
                      self.collides_from_left(opponent, move=True)]

        if not any(collisions):
            self.x -= self.vel
            self.x_moving_direction = -1
            current_move.append("left")

    def move_right(self, opponent, right_goal):
        collisions = [self.collide_right_wall(right_goal),
                      self.collides_from_right(opponent, move=True)]

        if not any(collisions):
            self.x += self.vel
            self.x_moving_direction = 1
            current_move.append("right")

    def move_down(self, opponent):
        global current_move
        self.height_delta = self.rect.bottom - opponent.rect.top
        self.y -= self.height_delta
        current_move.append("down")

    def fall_back_down(self):
        if not self.is_jumping:
            self.y = Player.players_start_y

    def jump(self):
        global current_move
        if not self.is_jumping:

            if self.is_jumping is None:
                self.y += self.height_delta
                self.jump_delta = self.jump_count
                self.jump_count = Player.jump_count

            self.is_jumping = True
            self.do_jump()
            current_move.append("jump")

    def do_jump(self):
        if self.is_jumping:
            if not self.jump_count < - Player.jump_count:
                self.y -= 0.5 * (self.jump_count * abs(self.jump_count)) * self.jump_increment
                self.jump_count -= 1
            else:
                if self.jump_delta != 0:
                    self.jump_count = self.jump_delta
                    self.jump_delta = 0
                else:
                    self.jump_count = Player.jump_count
                    self.is_jumping = False

    def kick(self):
        global current_move
        if not self.is_kicking:
            self.is_kicking = True
            self.is_kicked = False
            self.kick_count = 0
            self.do_kick()
            current_move.append("kick")

    def do_kick(self):
        if self.is_kicking:
            if self.kick_count == 0:
                self.switch_image()
                if self.image_index == 0:
                    self.is_kicking = False

            self.kick_count += 1
            if self.kick_count == Player.kick_count:
                self.kick_count = 0
