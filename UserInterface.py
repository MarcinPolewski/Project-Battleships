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

