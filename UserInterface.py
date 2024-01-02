""" this file handles interaction with user"""

from GameErrors import OutOfTableError
import constants
import pygame
from GameLogicController import GameLogicController
from BoardPositionCalculations import (
    calculate_row_and_column,
    calculate_x_y_cooridantes,
)

from Buttons import (
    PlayPVPButton,
    PlayPVCButton,
    ExitStartScreenButton,
    ExitEndScreenButton,
    ReplayButton,
    ButtonHandler,
)


class ScreenHandler:
    """handles background animations and table images"""

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
        """updated backround animations"""

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

    def draw_backroung(self):
        """draws background on screen"""
        self._screen.blit(self._current_background, (0, 0))

    def draw_tables(self):
        """draws tables on screen"""
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

    def draw(self):
        """method draws backround and tables"""
        self.draw_backroung()

        if self.phase == constants.GAME_START_SCREEN:
            # @TODO write title on screen
            # @TODO draw buttons on screen
            pass
        elif self.phase in [constants.GAME_PHASE, constants.POSITIONING_PHASE]:
            self.draw_tables()
        elif self.phase == constants.BLACKSCREEN_PHASE:
            # @TODO write promp on screen
            pass

        elif self.phase == constants.GAME_RESULT_PHASE:
            # @TODO write winner on screen
            # @TODO draw buttons
            pass


class Visualizer:
    """handles visualising game situation on boards"""

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
        """draws view of player on the board
        if for_left_table is True draws player's fleet on left table (ships)
        else draws what player's opponent sees on right table (clouds and ships)
        """
        # @TODO add animation support for this methods
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


class InputHandler:
    """handles interaction with user and triggers
    corresponding methods in GameLogicController

    class has methods, which check if particular event has occured
    if so they trigger right method in GameLogicController and return True,
    so mouse_button_interaction does not have to check further
    """

    def __init__(self, game_controller, button_handler):
        self._game_controller = game_controller
        self._button_handler = button_handler
        self._mouse_press_start_column = None
        self._mouse_press_start_row = None
        self._mouse_mouse_pressed_position = None

    def players_board_pressed(self, mouse_position):
        """checks if players board was pressed. If so saves row and column
        and returns True else False"""
        try:
            row_and_column = calculate_row_and_column(
                coordinates=mouse_position, from_left_table=True
            )

            # player's board is pressed
            row, column = row_and_column
            self._mouse_press_start_column = column
            self._mouse_press_start_row = row

        except OutOfTableError:
            return False

    def players_board_released(self, mouse_position):
        """checks if mouse button was released on players board and if
        user has selected cells in one line. If so triggers right GameLogicController method
        and return True. Else return False
        """
        try:
            row_and_column = calculate_row_and_column(
                coordinates=mouse_position, from_left_table=True
            )
            # mouse on player's board has been released and press
            # has definitely occured on his board

            start_row = self._mouse_press_start_row
            start_column = self._mouse_press_start_column
            end_row, end_column = row_and_column

            # check if in one dimension
            if (start_row != end_row) and (start_column != end_column):
                return False

            self._game_controller.players_cells_selected(
                start_row=start_row,
                start_column=start_column,
                end_row=end_row,
                end_column=end_column,
            )

            return True

        except OutOfTableError:
            return False

    def enemys_board_pressed(self, mouse_position):
        """checks if enemy's board was pressed if so triggers right GameLogicController method
        and return True. Else returns False"""
        try:
            row_and_column = calculate_row_and_column(
                coordinates=mouse_position, from_left_table=False
            )
            # enemy's board is pressed
            row, column = row_and_column
            self._game_controller.enemys_board_mouse_pressed(row, column)

            return True

        except OutOfTableError:
            return False

    def end_blackscreen_phase_pressed(self):
        """checks if user has pressed mouse, to proceed with game
        and return True. Else returns False"""
        if self._game_controller.phase == constants.BLACKSCREEN_PHASE:
            self._game_controller.exit_black_screen_phase()
            return True
        return False

    def button_was_pressed(self, mouse_position):
        """checks if button was pressed, if so triggers right GameLogicController method
        and return True. Else returns False"""

        self._mouse_pressed_position

        button = self._button_handler.check_button_press(
            mouse_press_position=mouse_position,
            mouse_release_position=self._mouse_pressed_position,
        )

        if button is None:
            return False
        # calling right method
        if isinstance(button, PlayPVPButton):
            self._game_controller.game_mode_selected(constants.PVP)
        elif isinstance(button, PlayPVCButton):
            self._game_controller.game_mode_selected(constants.PVC)

        elif isinstance(button, ExitStartScreenButton):
            self._game_controller.exit_game()
        elif isinstance(button, ExitEndScreenButton):
            self._game_controller.exit_game()
        elif isinstance(button, ReplayButton):
            pass  # @TODO how to restart game??? game_controller.__init__() ???

        return True

    def mouse_button_interaction(self, mouse_position, is_pressed):
        """method checks which interaction has been performed"""
        if is_pressed:  # mouse button has been pressed
            self._mouse_pressed_position = mouse_position
            if self.end_blackscreen_phase_pressed():
                pass
            elif self.players_board_pressed(mouse_position):
                pass
            elif self.enemys_board_pressed(mouse_position):
                pass
        else:  # mouse button has been released
            if self.players_board_released(mouse_position):
                pass
            elif self.button_was_pressed(mouse_position):
                pass


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # configurating screen
    game_screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Battleships")

    # initializing controllers
    game_controller = GameLogicController()
    visualizer = Visualizer(screen=game_screen, game_controller=game_controller)
    screen_handler = ScreenHandler(screen=game_screen, game_controller=game_controller)
    button_handler = ButtonHandler(screen=game_screen, game_controller=game_controller)
    input_handler = InputHandler(
        game_controller=game_controller, button_handler=button_handler
    )

    # main game loop, checks for event
    while game_controller.game_is_running:
        # setting frames per second
        clock.tick(constants.FPS)

        # UPDATE ELEMENTS
        screen_handler.update()
        visualizer.update()
        button_handler.update()

        # DRAW ELEMENTS
        screen_handler.draw()
        visualizer.draw()
        button_handler.draw()

        pygame.display.update()

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_controller.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_handler.mouse_button_interaction(
                    mouse_position=pygame.mouse.get_pos(), is_pressed=True
                )
            if event.type == pygame.MOUSEBUTTONUP:
                input_handler.mouse_button_interaction(
                    mouse_position=pygame.mouse.get_pos(), is_pressed=False
                )

    pygame.quit()


if __name__ == "__main__":
    main()
