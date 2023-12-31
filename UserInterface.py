""" this file handles interaction with user"""

from GameErrors import OutOfTableError
import constants
import pygame
from GameLogicController import GameLogicController
from BoardPositionCalculations import (
    calculate_row_and_column,
    calculate_x_y_cooridantes,
)


class ScreenHandler:
    """handles background animations, tables and buttons"""

    def __init__(self, screen, game_controller):
        # loading background images
        self._background_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/see/background{i}.png")
            self._background_images.append(temp)

        # loading table images
        self._table_image = pygame.image.load("assets/table/table.png")

        self._screen = screen
        self._game_controller = game_controller
        self._background_idx = 0
        self._current_background = self._background_images[0]
        self._last_background_change = pygame.time.get_ticks()

    @property
    def phase(self):
        return self._game_controller.phase

    def update(self):
        # updating backround animation
        # if enough time has passed since last update
        if (
            pygame.time.get_ticks() - self._last_background_change
            >= constants.BACKGROUND_COOLDOWN
        ):
            # incrementing idx, after exceeding array's length, going back to 0
            self._background_idx = (self._background_idx + 1) % len(
                self._background_images
            )
            self._current_background = self._background_images[self._background_idx]
            self._last_background_change = pygame.time.get_ticks()

    def draw(self):
        # drawing see
        self._screen.blit(self._current_background, (0, 0))

        if self.phase == constants.GAME_START_SCREEN:
            # @TODO write title on screen
            # @TODO draw buttons on screen
            pass
        elif self.phase in [constants.GAME_PHASE, constants.POSITIONING_PHASE]:
            # drawing left table
            self._screen.blit(
                self._table_image,
                (constants.TABLE_HORIZONTAL_OFFSET, constants.TABLE_VERTICAL_OFFSET),
            )
            # drawing right table
            self._screen.blit(
                self._table_image,
                (
                    constants.SCREEN_WIDTH
                    - constants.TABLE_HORIZONTAL_OFFSET
                    - constants.TABLE_SIZE,
                    constants.TABLE_VERTICAL_OFFSET,
                ),
            )
        elif self.phase == constants.BLACKSCREEN_PHASE:
            # @TODO write promp on screen
            pass

        elif self.phase == constants.GAME_RESULT_PHASE:
            # @TODO write winner on screen
            # @TODO draw buttons
            pass

class Visualizer:
    """handles visualising game status on the board(clouds, ships)"""

    def __init__(self, screen, game_controller):
        self._screen = screen
        self._game_controller = game_controller

        # loading cloud images
        self._cloud_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/clouds/Cloud{i}.png")
            self._cloud_images.append(temp)

        # loading ship images
        self._ship_images = []
        for i in range(1, 5):
            temp = pygame.image.load(f"assets/ships/Ship{i}.png")
            self._ship_images.append(temp)

        # initialize cloud animation dict
        self._cloud_animation_status = dict()
        for row in range(constants.BOARD_CELL_SIZE):
            for column in range(constants.BOARD_CELL_SIZE):
                self._cloud_animation_status[(row, column)] = 1

        # initialize ship animation dict
        self._ship_animation_status = dict()
        for row in range(constants.BOARD_CELL_SIZE):
            for column in range(constants.BOARD_CELL_SIZE):
                self._ship_animation_status[(row, column)] = 1

    @property
    def player1(self):
        return self._game_controller.player1

    @property
    def player2(self):
        return self._game_controller.player2

    @property
    def phase(self):
        return self._game_controller.phase

    def update(self):
        """updates animations of ships and clouds"""
        # @TODO only one cell at the start of round in players board
        # after shot animation at enemys board
        pass

    def draw_one_player(self, player, for_left_table):
        # @TODO add animation support for this method
        """displays only players fleet"""
        players_board = player.board
        board_height = player.board_height
        board_width = player.board_width

        for row_index in range(board_height):
            for column_index in range(board_width):
                # calculate ship image position
                position = calculate_x_y_cooridantes(
                    row=row_index,
                    column=column_index,
                    from_left_table=for_left_table,
                )
                board_cell = player.board[row_index, column_index]

                # left table (normal ship or hit ship)
                if for_left_table:
                    if not board_cell.is_free:
                        if board_cell.was_shot:
                            # drawing shot ship
                            self._screen.blit(self._ship_images[3], position)
                        else:
                            # drawing normal ship
                            self._screen.blit(self._ship_images[0], position)

                # right (cloud or shot ship)
                else:
                    if not board_cell.was_shot:
                        # drawing cloud
                        self._screen.blit(self._cloud_images[0], position)
                    elif not board_cell.is_free:
                        # drawing hit ship
                        self._screen.blit(self._ship_images[3], position)

    def draw(self):
        """draws player1's view on the board"""
        if self.phase in [constants.GAME_PHASE, constants.POSITIONING_PHASE]:
            self.draw_one_player(player=self.player1, for_left_table=True)
            self.draw_one_player(player=self.player2, for_left_table=False)
