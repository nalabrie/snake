# made by very loosely following the tutorial made by "Clear Code" at https://youtu.be/QFvqStqPCRU

import pickle
import sys
from random import randint

import pygame
from pygame.math import Vector2

# ---- GLOBAL CONSTANTS ----

DEBUG = False
CELL_SIZE = 40
CELL_NUMBER = 20
WIDTH = CELL_NUMBER * CELL_SIZE  # screen width
HEIGHT = WIDTH  # screen height
FPS = 60
FONT_SIZE = 25
FONT_AA = True  # enable antialiasing for fonts
FONT_COLOR = (56, 74, 12)
BACK_COLOR = (175, 215, 70)  # screen background color
GRASS_COLOR = (167, 209, 61)


# ---- CLASSES ----

class Fruit:
    """
    The fruit that the snake tries to collect around the game board. Takes a 'Vector2' to be used as its starting
    position on the board. Ensure that pygame has been initialized before using this class.
    """

    # ---- FUNCTIONS ----

    def __init__(self, starting_pos=Vector2(15, 10)):
        """
        Initializes the Fruit class.
        @param starting_pos: Starting "Vector2" position for the fruit.
        """
        # assign starting position of fruit
        self.pos = starting_pos

        # load fruit image
        self.apple_img = pygame.image.load("Graphics/apple.png").convert_alpha()

    def draw_fruit(self, surface):
        """
        Draws the fruit object to the supplied pygame surface.
        @param surface: Pygame "Surface" to draw onto.
        """
        # create a rectangle
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        # draw the apple image
        surface.blit(self.apple_img, fruit_rect)
        # pygame.draw.rect(surface, FRUIT_COLOR, fruit_rect)  # old

    def move_fruit(self):
        """
        Moves the fruit to a random position on the board. Does not check if the fruit will be placed in an illegal
        position (inside the snake, for example). This must be handled elsewhere if desired.
        """
        self.pos = Vector2(randint(0, CELL_NUMBER - 1),
                           randint(0, CELL_NUMBER - 1))


class Snake:
    """
    The snake that the player controls. Use the arrow keys to move.
    Ensure that pygame has been initialized before using this class.
    """

    # ---- VARIABLES ----

    # movement direction constants
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)

    # ---- FUNCTIONS ----

    def __init__(self):
        """
        Initializes the Snake class.
        """
        # list of the snake's body (placed in starting position)
        self.body = [Vector2(3, 10), Vector2(2, 10), Vector2(1, 10)]

        # give snake a starting direction
        self.direction = self.RIGHT

        # when true, the snake is able to grow the next time it moves
        self.add_new_block = False

        # load snake eating sound
        self.eating_sound = pygame.mixer.Sound("Sound/crunch.wav")

        # load snake images

        # head images
        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        # tail images
        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        # body images
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()

        # turning images
        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()

    def draw_snake(self, surface):
        """
        Draws the snake to the supplied pygame surface.
        @param surface: Pygame "Surface" to draw onto.
        """
        # loop through each block in the snake's body list
        # also grab the index of each block
        for index, block in enumerate(self.body):
            # create a rectangle (for image positioning)
            snake_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # find what direction snake is heading
            if index == 0:
                # this is the head block

                # blit image that matches snake's direction
                if self.direction == self.UP:
                    surface.blit(self.head_up, snake_rect)
                elif self.direction == self.DOWN:
                    surface.blit(self.head_down, snake_rect)
                elif self.direction == self.RIGHT:
                    surface.blit(self.head_right, snake_rect)
                elif self.direction == self.LEFT:
                    surface.blit(self.head_left, snake_rect)
            elif index == len(self.body) - 1:
                # this is the end block of the snake

                # calculate the direction of the tail
                tail_direction = self.body[index] - self.body[index - 1]

                # blit image that matches snake's tail direction
                if tail_direction == self.UP:
                    surface.blit(self.tail_up, snake_rect)
                elif tail_direction == self.DOWN:
                    surface.blit(self.tail_down, snake_rect)
                elif tail_direction == self.RIGHT:
                    surface.blit(self.tail_right, snake_rect)
                elif tail_direction == self.LEFT:
                    surface.blit(self.tail_left, snake_rect)
            else:
                # this is any block of the body in between the head and end block

                # find the blocks before and after the current block
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # blit the correct image for each condition
                if previous_block.x == next_block.x:
                    # surrounding blocks are both vertical
                    # current block must be going vertical as well
                    surface.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    # surrounding blocks are both horizontal
                    # current block must be going horizontal as well
                    surface.blit(self.body_horizontal, snake_rect)
                else:
                    # this block must be a corner block
                    # calculate which corner block to use and blit it
                    # @formatter:off
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        surface.blit(self.body_tl, snake_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        surface.blit(self.body_bl, snake_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        surface.blit(self.body_tr, snake_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        surface.blit(self.body_br, snake_rect)
                    # @formatter:on

    def move_snake(self):
        """
        Moves the snake (internally, does not draw the snake).
        """
        if self.add_new_block:
            body_copy = self.body[:]
            self.add_new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def grow_snake(self):
        """
        Grows the snake by one block.
        """
        # snake does not actually grow in this method
        # by setting this variable to 'True' it will grow the next time the snake moves
        self.add_new_block = True


class MainGame:
    """
    Main game logic class. The 'surface' argument is the main pygame surface to draw the game onto.
    Ensure that pygame has been initialized before using this class.
    """

    # ---- FUNCTIONS ----

    def __init__(self, surface):
        """
        Initializes the "MainGame" class.
        @param surface: The main pygame "Surface" to draw the game onto
        """
        self.snake = Snake()
        # store previous snake direction to prevent it from reversing
        self.old_direction = self.snake.direction
        self.fruit = Fruit()
        self.game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", FONT_SIZE)
        self.score = 0  # player's score
        self.is_game_over = False
        self.main_screen = surface
        self.load_high_scores()

    def update(self):
        """
        Updates the internal state of the game (as long as the game isn't over).
        """
        if self.is_game_over:
            return

        if self.old_direction != -self.snake.direction:
            # safe for snake to change direction
            self.old_direction = self.snake.direction
        else:
            # not safe for snake to change direction, prevent it
            self.snake.direction = self.old_direction
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        """
        Draws all items to the main screen surface (as long as the game isn't over).
        """
        if self.is_game_over:
            return

        self.main_screen.fill(BACK_COLOR)
        self.draw_grass()
        self.fruit.draw_fruit(self.main_screen)
        self.snake.draw_snake(self.main_screen)
        self.draw_score()

    def check_collision(self):
        """
        Checks the collision between the snake and fruit/walls/itself and handles what should occur when that happens.
        """
        if self.fruit.pos == self.snake.body[0]:
            # snake eats fruit
            self.snake.eating_sound.play()
            self.snake.grow_snake()
            self.score += 1
            self.safely_move_fruit()
        if (not 0 <= self.snake.body[0].x < CELL_NUMBER) or (not 0 <= self.snake.body[0].y < CELL_NUMBER):
            # snake hit the wall
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                # snake hit itself
                self.game_over()

    def game_over(self):
        """
        Handles what happens when the snake dies and the game is over.
        Draws the game over messages onto the 'main_screen'.
        """
        self.is_game_over = True
        self.update_high_scores()
        self.save_high_scores()

        # store game over text, final score, and high scores to be displayed
        game_over_messages = [
            "GAME OVER", "Final Score: " + str(self.score), "HIGH SCORES",
            str(self.high_scores[0]),
            str(self.high_scores[1]),
            str(self.high_scores[2]),
            str(self.high_scores[3]),
            str(self.high_scores[4])
        ]

        # calculate (x,y) to place the first line of game over text
        x = WIDTH // 2
        y = HEIGHT // 3

        # loop through all messages to be drawn to the screen
        for index, msg in enumerate(game_over_messages):
            # render msg
            message_surface = self.game_font.render(msg, FONT_AA, FONT_COLOR)
            # place rect around msg
            message_rect = message_surface.get_rect(center=(x, y))
            # blit msg
            self.main_screen.blit(message_surface, message_rect)
            # offset y for next msg
            y += CELL_SIZE
            if index == 1:
                # offset again to visually split the high score list
                y += CELL_SIZE

    def draw_grass(self):
        """
        Draws the grass on the 'main_screen' (the game board) in a checkerboard pattern.
        """
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.main_screen, GRASS_COLOR, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.main_screen, GRASS_COLOR, grass_rect)

    def draw_score(self):
        """
        Draws the player's score onto the 'main_screen'.
        """
        # score is the length of the snake minus its starting length
        score_text = str(self.score)

        # render the score onto its own surface
        score_surface = self.game_font.render(score_text, FONT_AA, FONT_COLOR)

        # calculate (x,y) to place score text and draw a rectangle around the score surface
        x = CELL_SIZE * CELL_NUMBER - 60
        y = CELL_SIZE * CELL_NUMBER - 40
        score_rect = score_surface.get_rect(center=(x, y))

        # draw the score to the screen
        self.main_screen.blit(score_surface, score_rect)

    def safely_move_fruit(self):
        """
        Moves the fruit so that it is never spawned in an illegal position (inside the snake).
        """
        safe = False
        while not safe:
            self.fruit.move_fruit()
            safe = True
            for block in self.snake.body:
                if block == self.fruit.pos:
                    safe = False

    def load_high_scores(self):
        """
        Loads a list of previous high scores from a file.
        If the file does not exist then a dummy list is used instead.
        The list always has a length of 5.
        """
        try:
            with open("high_scores.pkl", mode="rb") as f:
                self.high_scores = pickle.load(f)
        except FileNotFoundError:
            self.high_scores = [0, 0, 0, 0, 0]

    def update_high_scores(self):
        """
        Updates and reverse-sorts the current list of high scores.
        """
        self.high_scores.sort(reverse=True)
        if self.score > self.high_scores[-1]:
            # new top 5 high score, replace the smallest old high score and re-sort
            self.high_scores[-1] = self.score
            self.high_scores.sort(reverse=True)

    def save_high_scores(self):
        """
        Saves the current list of high scores to a file.
        """
        try:
            with open("high_scores.pkl", mode="wb") as f:
                pickle.dump(self.high_scores, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            # just print a warning to the console, it is ok if a high score file cannot be saved
            print("WARNING: a high score file cannot be saved to disk due to an unknown error")
            print(f"Exception output:\n{e}")

    def draw_debug(self, clock):
        """
        Draws debug messages to the main screen.
        Needs a pygame clock to calculate FPS.
        Does nothing when the game is over.
        @param clock: A "pygame.time.Clock()" object.
        @return: Returns "None" when the game is over.
        """
        if self.is_game_over:
            return

        # draw current FPS
        fps_text = "FFS: "
        fps_value_text = str(round(clock.get_fps(), 1))
        fps_surface = self.game_font.render(fps_text, FONT_AA, FONT_COLOR)
        fps_value_surface = self.game_font.render(fps_value_text, FONT_AA, FONT_COLOR)
        fps_rect = fps_surface.get_rect(center=(40, 40))
        fps_value_rect = fps_value_surface.get_rect(midleft=fps_rect.midright)
        self.main_screen.blit(fps_surface, fps_rect)
        self.main_screen.blit(fps_value_surface, fps_value_rect)


# ---- MAIN ----

def main():
    """
    Main method. Runs the game.
    """
    # create pygame-related variables
    pygame.mixer.pre_init(buffer=512)  # reduce sound delay (potentially)
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    SCREEN_UPDATE = pygame.USEREVENT  # updates screen at time interval
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    # create instance of the game logic
    main_game = MainGame(screen)

    ready = False
    while not ready:
        # pre-game loop, loops until user presses a key

        # check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # user closed window
                pygame.quit()  # quit pygame
                sys.exit()  # quit python
            if event.type == pygame.KEYDOWN:
                # user pressed a key
                # start game
                ready = True

        main_game.draw_elements()

        pygame.display.update()  # updates screen
        clock.tick(FPS)  # limits frame rate
    del ready

    # game has begun

    new_game = False  # starts a new game when True
    while True:
        # game loop, draw all elements here

        if new_game:
            # starts a new game by creating a fresh game logic instance
            main_game = MainGame(screen)
            new_game = False

        # check for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # user closed window
                pygame.quit()  # quit pygame
                sys.exit()  # quit python
            if event.type == SCREEN_UPDATE:
                # 'SCREEN_UPDATE' timer went off
                main_game.update()  # update game state
                main_game.draw_elements()  # update graphics
                if DEBUG:
                    # draw debug messages
                    main_game.draw_debug(clock)
            if event.type == pygame.KEYDOWN:
                # user pressed a key
                if event.key == pygame.K_UP:
                    # attempt to change snake direction up
                    main_game.snake.direction = main_game.snake.UP
                if event.key == pygame.K_DOWN:
                    # attempt to change snake direction down
                    main_game.snake.direction = main_game.snake.DOWN
                if event.key == pygame.K_RIGHT:
                    # attempt to change snake direction right
                    main_game.snake.direction = main_game.snake.RIGHT
                if event.key == pygame.K_LEFT:
                    # attempt to change snake direction left
                    main_game.snake.direction = main_game.snake.LEFT
                if event.key == pygame.K_r:
                    # starts a new game when player presses 'r'
                    new_game = True

        pygame.display.update()  # refresh game window
        clock.tick(FPS)  # limits frame rate


if __name__ == "__main__":
    # run game
    main()
