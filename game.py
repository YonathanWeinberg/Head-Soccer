# # # IMPORTS # # #
import pygame
import time
from threading import Thread

from globals import WIDTH, HEIGHT, INTRO_IMAGE, INTRO2_IMAGE, BG_IMAGE, BALL_IMAGE, WHITE, BLACK
from globals import player_moves, opponent_moves, current_move
from player import Player
from ball import Ball
from goal import Goal
from communication import Communication

# # # CONSTANTS # # #

FPS = 60


class Game:
    max_score = 4

    def __init__(self, width=WIDTH, height=HEIGHT, fps=FPS):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Define fonts
        self.winner_font = pygame.font.SysFont('Comic Sans MS', 70)
        self.score_font = pygame.font.SysFont('Comic Sans MS', 30)

        # Define screen settings
        self.width, self.height = width, height
        self.fps = fps

        # Define params
        self.winner = None
        self.player_score, self.opponent_score = 0, 0

        # Create game objects
        self.player_side = "right"
        self.player = None
        self.opponent = None
        self.ball = None
        self.player_goal = None
        self.opponent_goal = None

        # Define pygame objects
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Socket object
        self.socket = Communication()

        # Set screen settings
        pygame.display.set_caption("Head Soccer")
        pygame.display.set_icon(BALL_IMAGE)

        # Start the game
        self.start()

    @property
    def opponent_side(self):
        if self.player_side:
            return "left" if self.player_side == "right" else "right"

        return None

    def start(self):
        print("[START] Game is starting")
        # Intro screen
        self.screen.blit(INTRO_IMAGE, (0, 0))
        pygame.display.update()

        self.socket.start()

        print("[WAITING] Waiting for player side")
        self.player_side = self.socket.get_side()
        print(f"[SIDE] Player side is {self.player_side}")

        self.screen.blit(INTRO2_IMAGE, (0, 0))
        pygame.display.update()
        time.sleep(3)

        thread = Thread(target=self.socket.play)
        thread.start()

        self.create_game_objects()
        self.play()
        pygame.quit()

    def create_game_objects(self):
        self.player: Player = Player(self.player_side, self.screen)
        self.opponent: Player = Player(self.opponent_side, self.screen)
        self.ball: Ball = Ball(self.screen)
        self.player_goal: Goal = Goal(self.player_side, self.screen)
        self.opponent_goal: Goal = Goal(self.opponent_side, self.screen)

    def play(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.winner is None:
                        break

            if self.winner is None:
                self.player_movement()
                self.opponent_movement()
                scorer = self.ball_movement()
                self.draw_screen()
                self.handle_score(scorer)

            else:
                self.handle_winning()

    def handle_score(self, scorer):
        if scorer:
            self.update_scores(scorer)
            self.reset_match()

    def handle_winning(self):
        global player_moves
        player_moves.append("won")
        if self.winner == self.player_side:
            pass
        else:
            pass

    def update_scores(self, scorer):
        # Update scores
        if scorer == self.player_side:
            self.player_score += 1
        else:
            self.opponent_score += 1

        # Check if someone has won
        if self.player_score == Game.max_score:
            self.winner = self.player_side
        elif self.opponent_score == Game.max_score:
            self.winner = self.opponent_side

    def reset_match(self):
        self.ball.update_position()
        self.draw_screen()
        self.draw_objects()
        self.draw_goals()
        self.draw_score()
        self.screen.blit(self.winner_font.render("GOAL!", False, WHITE), (500, 230))
        pygame.display.update()

        time.sleep(3)

        self.ball.reset_velocities()
        self.ball.reset_coordinates()
        self.player.reset_coordinates()
        self.opponent.reset_coordinates()

    def player_movement(self):
        # Handle jumping
        if self.player.is_jumping is not False:
            players_collide = self.player.collides_from_bottom(self.opponent)

            if self.player.is_jumping and players_collide:
                self.player.is_jumping = None
                self.player.move_down(self.opponent)

            elif self.player.is_jumping is None and not players_collide:
                self.player.is_jumping = True

        # Implement jumping & kicking
        self.player.do_jump()
        self.player.do_kick()

        # Handle key presses
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            left_goal = Goal.left_goal(self.player_goal, self.opponent_goal)
            self.player.move_left(self.opponent, left_goal)

        if keys_pressed[pygame.K_RIGHT]:
            right_goal = Goal.right_goal(self.player_goal, self.opponent_goal)
            self.player.move_right(self.opponent, right_goal)

        if keys_pressed[pygame.K_UP]:
            self.player.jump()

        elif keys_pressed[pygame.K_DOWN]:
            self.player.fall_back_down()

        if keys_pressed[pygame.K_SPACE]:
            self.player.kick()

        # Reset player x_moving_direction
        if self.player.x_moving_direction:
            if not keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
                self.player.x_moving_direction = 0

    def opponent_movement(self):
        # Handle jumping
        if self.opponent.is_jumping is not False:
            players_collide = self.opponent.collides_from_bottom(self.player)

            if self.opponent.is_jumping and players_collide:
                self.opponent.is_jumping = None
                self.opponent.move_down(self.opponent)

            elif self.opponent.is_jumping is None and not players_collide:
                self.opponent.is_jumping = True

        # Implement jumping & kicking
        self.opponent.do_jump()
        self.opponent.do_kick()

        # Handle key presses
        if len(opponent_moves):
            moves = opponent_moves.pop(0)

            if "left" in moves:
                left_goal = Goal.left_goal(self.player_goal, self.opponent_goal)
                self.opponent.move_left(self.player, left_goal)

            if "right" in moves:
                right_goal = Goal.right_goal(self.player_goal, self.opponent_goal)
                self.opponent.move_right(self.player, right_goal)

            if "jump" in moves:
                self.opponent.jump()

            elif "down" in moves:
                self.opponent.fall_back_down()

            if "kick" in moves:
                self.opponent.kick()

            # Reset player x_moving_direction
            if self.opponent.x_moving_direction:
                if not "left" in moves and not "right" in moves:
                    self.opponent.x_moving_direction = 0

    def ball_movement(self):
        self.ball.update_velocities()
        self.ball.handle_gravity_and_bounce()
        self.ball.handle_walls_collision()
        self.ball.handle_player_collision(self.player)
        self.ball.handle_player_collision(self.opponent)
        # self.ball.handle_min_x_speed()
        scorer = self.ball.handle_goals_collision(self.player_goal, self.opponent_goal)
        if scorer:
            print(f"{scorer = }")

        self.ball.update_position()
        return scorer

    def draw_screen(self):
        self.draw_background()
        self.draw_objects()
        self.draw_goals()
        self.draw_score()
        pygame.display.update()

    def draw_background(self):
        self.screen.blit(BG_IMAGE, (0, 0))

    def draw_goals(self):
        self.player_goal.draw()
        self.opponent_goal.draw()

    def draw_objects(self):
        self.ball.draw()
        self.opponent.draw()
        self.player.draw()

    def draw_score(self):
        left_player_score = self.player_score if self.player_side == "left" else self.opponent_score
        right_player_score = self.opponent_score if self.player_side == "left" else self.player_score

        left_score = self.score_font.render(str(left_player_score), False, WHITE)
        right_score = self.score_font.render(str(right_player_score), False, WHITE)

        self.screen.blit(left_score, (565, 20))
        self.screen.blit(right_score, (615, 20))
