""" this file handles interaction with user"""
import pygame

# modules created for this game
from GameErrors import OutOfTableError
import constants
from BoardPositionCalculations import (
    calculate_row_and_column,
    calculate_x_y_cooridantes,
)
from Buttons import (
    PlayPVPButton,
    PlayPVCButton,
    ExitStartScreenButton,
    ExitEndScreenButton,
    MainMenuButton,
    SwitchUserButton,
)


class UIObject:
    def __init__(self, screen, game_controller, image_handler):
        self._screen = screen
        self._game_controller = game_controller
        self._image_handler = image_handler

    @property
    def phase(self):
        return self._game_controller.phase


class ScreenVisualizer(UIObject):
    """handles static elements - background, logo, prompt in blackscreen phase
    and statistics on the end of game screen

    :param _image_handler: class used for getting images
    :type _image_hanlder: Images.ImageHandler
    :param  _screen: screen where elements will be displayed
    :type _screen: pygame.Surface
    :param _game_controller: controlls game - used for getting phases
    :type _game_controller: GameLogicController.GameLogicController
    :param _see_images: list of see images
    :type _see_images: list
    :param _logo: image of logo displayed on start screen
    :type _logo: pygame.Surface
    :param _blackscreen_prompt: image of prompt to switch users
    :type _blackscreen_prompt: pygame.Surface
    :param _blackscreen_prompt_position: stores position of this prompt
    :type _blackscreen_prompt_position: tuple
    :param _background_idx: index of image in self._see_images for animations
    :type _background_idx: int
    :param _current_background: this background will be displed when draw() is called
    :type _current_background: pygame.Surface
    :param _game_result_image: image displayed when game ends(winner and statistics)
    :type _game_result_image: pygame.Surface
    :param _last_background_change: moment when background has changed
    :type _last_background_change: int
    """

    def __init__(self, screen, game_controller, image_handler):
        super().__init__(screen, game_controller, image_handler)

        # loading right images
        self._see_images = image_handler.see_images
        self._logo = image_handler.logo_image
        self._blackscreen_prompt = image_handler.blackscreen_prompt

        # loading positions
        self._blackscreen_prompt_position = (
            image_handler.calculate_x_and_y_to_centre_on_screen(
                self._blackscreen_prompt
            )
        )
        self._game_result_image = None

        self._background_idx = 0
        self._current_background = self._image_handler.see_images[0]
        self._game_result_image = None
        self._last_background_change = pygame.time.get_ticks()

    def update(self):
        """updates animations"""

        # if enough time has passed since last update
        if (
            pygame.time.get_ticks() - self._last_background_change
            >= constants.BACKGROUND_COOLDOWN
        ):
            # incrementing idx, after exceeding array's length, going back to 0
            self._background_idx = (self._background_idx + 1) % len(self._see_images)
            self._current_background = self._see_images[self._background_idx]
            self._last_background_change = pygame.time.get_ticks()

        # resets game result image if neccessary
        if (
            self._game_result_image is not None
            and self.phase != constants.GAME_RESULT_PHASE
        ):
            self._game_result_image = None

    def draw_backroung(self):
        """draws background on screen"""
        self._screen.blit(self._current_background, (0, 0))

    def draw_logo(self):
        """draw logo on screen"""
        self._screen.blit(self._logo, constants.LOGO_POSITION)

    def draw_message_to_switch(self):
        """draws message to switch users at computer"""
        self._screen.blit(self._blackscreen_prompt, self._blackscreen_prompt_position)

    def generate_game_result_image(self):
        """generates game result image"""
        game_result = self._image_handler.game_result_background

        # adding winner to game_result image
        winner_image = self._image_handler.get_winner_image()
        winner_y = constants.WINNER_VERTICAL_OFFSET
        winner_x = self._image_handler.calculate_x_to_fit_in_the_middle(
            outer_image=game_result, inner_image=winner_image
        )
        game_result.blit(winner_image, (winner_x, winner_y))

        # adding statistics to game result image
        y = winner_image.get_height() + constants.STATISTICS_VERTICAL_OFFSET
        x = constants.STATISTICS_HORIZONTAL_OFFSET

        statistics = self._game_controller.generate_statistics()
        for statistic_key in statistics:
            statistic_value = statistics[statistic_key]
            statistic_text = statistic_key + ": " + statistic_value

            statistic_image = self._image_handler.get_statistic_image_from_text(
                statistic_text
            )

            y += statistic_image.get_height() + constants.STATISTIC_SPACING
            game_result.blit(statistic_image, (x, y))

        return game_result

    def draw_game_result(self):
        """method draws game result(winner and statistics) in the middle of screen"""

        if self._game_result_image is None:
            self._game_result_image = self.generate_game_result_image()
            self._game_result_image_position = (
                self._image_handler.calculate_x_and_y_to_centre_on_screen(
                    self._game_result_image
                )
            )
        self._screen.blit(self._game_result_image, self._game_result_image_position)

    def draw(self):
        """method draws backround and tables"""
        self.draw_backroung()

        if self.phase == constants.GAME_START_SCREEN:
            self.draw_logo()
        elif self.phase == constants.BLACKSCREEN_PHASE:
            self.draw_message_to_switch()

        elif self.phase == constants.GAME_RESULT_PHASE:
            self.draw_game_result()


class StatusBarVisualizer(UIObject):
    """class handles displaying status bar with informations

    :param _image_handler: class used for getting images
    :type _image_hanlder: Images.ImageHandler
    :param  _screen: screen where elements will be displayed
    :type _screen: pygame.Surface
    :param _game_controller: controlls game - used for getting phases
    :type _game_controller: GameLogicController.GameLogicController
    :param _background: image used as background for status bar
    :type _background: pygame.Surface
    :param _small_ship_icon: image representing on segment of ship
    :type _small_ship_icon: pygame.Surface

    """

    def __init__(self, screen, game_controller, image_handler):
        super().__init__(screen, game_controller, image_handler)

        # load background
        self._background = image_handler.status_bar_background

        # load small ship icon
        self._small_ship_icon = image_handler.small_ship_icon

    def update(self):
        pass

    def draw_background(self):
        """draws backround of status bar"""
        self._screen.blit(self._background, (0, 0))

    def draw_fleet_of_player(self, player, on_the_left):
        """draws fleet of one player above corresponding
        table"""

        # start drawing over corresponding table and end 600 px
        x = constants.TABLE_HORIZONTAL_OFFSET
        y = constants.FLEET_STATUS_VERTICAL_OFFSET
        if not on_the_left:
            x = (
                constants.SCREEN_WIDTH
                - constants.TABLE_SIZE
                - constants.TABLE_HORIZONTAL_OFFSET
            )

        for ship_name in constants.STANDARD_SHIP_QUANTITIES:
            quantity = constants.STANDARD_SHIP_QUANTITIES[ship_name]
            length = constants.SHIP_LENGTHS[ship_name]

            # drawing ship icon
            for i in range(length):
                self._screen.blit(self._small_ship_icon, (x, y))
                x += (
                    constants.SMALL_SHIP_ICON_SIZE
                    - constants.SMALL_SHIP_ICON_OFFSET_TO_OVERLAP
                )
                # subtracting to make icons overlap = looks better

            # calculate player's amount of this kind of ship
            ship_counter = 0
            for ship in player.fleet:
                if ship.length == length:
                    ship_counter += 1

            # generate image of text representing how many ships of kind are on board
            text = f"{ship_counter}/{quantity}"
            text_image = self._image_handler.get_status_bar_image_from_text(text)

            # adding spacing between ship icon and value
            x += constants.STATUS_BAR_INFORMATION_SPACING

            self._screen.blit(text_image, (x, y))

            # added spacing between information about this ship and another
            x += constants.SMALL_SHIP_ICON_SIZE * 2

    def draw_fleet_status(self):
        """hadnles drawing fleet status on status bar"""
        self.draw_fleet_of_player(
            player=self._game_controller.current_player, on_the_left=True
        )
        self.draw_fleet_of_player(
            player=self._game_controller.player_attacked, on_the_left=False
        )

    def calculate_x_position_of_name(self, image, for_left_table):
        """returns x position of text image so it is in the middle of table
        if for_left_table is True is's above left table
        """
        image_width = image.get_width()
        board_width = constants.TABLE_SIZE
        x = (board_width - image_width) // 2
        if for_left_table:
            x += constants.TABLE_HORIZONTAL_OFFSET
        else:
            x += (
                constants.SCREEN_WIDTH
                - constants.TABLE_HORIZONTAL_OFFSET
                - constants.TABLE_SIZE
            )

        return x

    def draw_name_above_table(self, name, above_left_table):
        """draws players name above corresponing table"""
        # loading player's name image
        image = self._image_handler.get_status_bar_image_from_text(name)

        # calculating position
        x = self.calculate_x_position_of_name(image, above_left_table)
        y = constants.PLAYER_NAME_VERTICAL_OFFSET

        self._screen.blit(image, (x, y))

    def draw_player_names(self):
        """handles drawing names of players in the status bar"""
        players_name, opponents_name = self._game_controller.get_player_names()
        self.draw_name_above_table(players_name, True)
        self.draw_name_above_table(opponents_name, False)

    def draw(self):
        """handles drawing screen bar"""
        if self.phase in [
            constants.GAME_PHASE,
            constants.POSITIONING_PHASE,
            constants.READY_TO_SWITCH_PHASE,
        ]:
            self.draw_background()
            self.draw_fleet_status()
            self.draw_player_names()


class Prompt(pygame.sprite.Sprite):
    """class handles dispalying single message to user

    :param _image_handler: class used for getting images
    :type _image_hanlder: Images.ImageHandler
    :param  _screen: screen where elements will be displayed
    :type _screen: pygame.Surface
    :param _prompt_text: text of prompt
    :type _prompt_text: str
    :param _alpha: alpha value of prompt image
    :type _alpha: int
    :param _last_update_time: moment when prompt was last updated
    :type _last_update_time: int
    :param _cooldown: alpha update cooldown
    :type _cooldown: int
    :param _image: image displayed as this prompt
    :type _image: pygame.Surface
    :param _position: position of prompt on screen
    :type _positon: tuple
    """

    def __init__(self, screen, prompt_text, image_handler):
        pygame.sprite.Sprite.__init__(self)
        self._prompt_text = prompt_text
        self._screen = screen
        self._alpha = 255
        self._last_update_time = pygame.time.get_ticks()

        # @TODO? make dependent on length of prompts
        self._cooldown = constants.PROMPT_COOLDOWN

        # load image
        self._image = image_handler.get_prompt_image(prompt_text)
        # calculate position
        self._position = image_handler.calculate_x_and_y_to_centre_on_screen(
            self._image
        )

    def update(self):
        """if enough time has passed updates fade of image or removes itself
        from list if it's gone"""
        current_time = pygame.time.get_ticks()
        if current_time - self._last_update_time >= self._cooldown:
            self._alpha -= 10
            self._last_update_time = current_time
            if self._alpha <= 0:
                # remove prompt from sprite list
                self.kill()
            self._image.set_alpha(self._alpha)

    def draw(self):
        """draw prompt on screen"""
        self._screen.blit(self._image, self._position)


class PromptVisualizer(UIObject):
    """reads fetches propts from game controller,
    creates instance of Prompt and updates all currently visible prompts

    :param _image_handler: class used for getting images
    :type _image_hanlder: Images.ImageHandler
    :param  _screen: screen where elements will be displayed
    :type _screen: pygame.Surface
    :param _game_controller: controlls game - used for getting phases
    :type _game_controller: GameLogicController.GameLogicController
    :param _active_prompts: list of currently displayed prompts
    :type _actve_prompts: pygame.sprite.Group
    """

    def __init__(self, screen, game_controller, image_handler):
        super().__init__(screen, game_controller, image_handler)
        self._active_prompts = pygame.sprite.Group()

    def update(self):
        """checks if there are new prompts and updated previous ones"""
        fetched_prompt = self._game_controller.fetch_prompt()
        if fetched_prompt is not None:
            # create instance of Prompt class and add to list
            prompt = Prompt(
                screen=self._screen,
                prompt_text=fetched_prompt,
                image_handler=self._image_handler,
            )
            self._active_prompts.add([prompt])
        # udpate existing prompts
        for prompt in self._active_prompts:
            prompt.update()

    def draw(self):
        """draws prommpts on screen"""
        for prompt in self._active_prompts:
            prompt.draw()


class GameBoardVisualizer(UIObject):
    """handles visualising game situation on boards/tables

    :param _image_handler: class used for getting images
    :type _image_hanlder: Images.ImageHandler
    :param  _screen: screen where elements will be displayed
    :type _screen: pygame.Surface
    :param _game_controller: controlls game - used for getting phases
    :type _game_controller: GameLogicController.GameLogicController
    :param _cloud_images: list of cloud images
    :type _cloud_images: list
    :param _ship_images: list of ship images
    :type _ship_images: list
    :param _table_image: stores image of table
    :type _table_image: pygame.Surface
    """

    def __init__(self, screen, game_controller, image_handler):
        super().__init__(screen, game_controller, image_handler)

        self._cloud_images = image_handler.cloud_images
        self._ship_images = image_handler.ship_images
        self._table_image = image_handler.table_image

    @property
    def player1(self):
        return self._game_controller.player1

    @property
    def player2(self):
        return self._game_controller.player2

    def update(self):
        """updates animations of ships and clouds"""
        # @TODO only one cell at the start of round in players board
        # after shot animation at enemys board
        pass

    def draw_table(self, is_left):
        """draws single table either on the left or right"""
        y = constants.TABLE_VERTICAL_OFFSET
        x = 0
        if is_left:
            x = constants.TABLE_HORIZONTAL_OFFSET
        else:
            x = (
                constants.SCREEN_WIDTH
                - constants.TABLE_HORIZONTAL_OFFSET
                - constants.TABLE_SIZE
            )
        self._screen.blit(self._table_image, (x, y))

    def draw_one_player(self, player, for_left_table):
        """draws view of player on the board
        if for_left_table is True draws player's fleet on left table (ships)
        else draws what player's opponent sees on right table (clouds and ships)
        """
        # @TODO add animation support for this methods

        # draw game situation
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
        # draw table image
        self.draw_table(for_left_table)

    def draw(self):
        """draws current player's view on the board"""
        if self.phase in [
            constants.GAME_PHASE,
            constants.POSITIONING_PHASE,
            constants.READY_TO_SWITCH_PHASE,
        ]:
            current_player = self._game_controller.current_player
            player_attacked = self._game_controller.player_attacked
            self.draw_one_player(player=current_player, for_left_table=True)
            self.draw_one_player(player=player_attacked, for_left_table=False)


class InputHandler:
    """handles interaction with user and triggers
    corresponding methods in GameLogicController

    class has methods, which check if particular event has occured
    if so they trigger right method in GameLogicController and return True,
    so mouse_button_interaction does not have to check further


    :param _game_controller: controlls game - used for getting phases
    :type _game_controller: GameLogicController.GameLogicController
    :param _button_handler: class responsible for handling buttons
    :type _button_handler: Buttons.ButtonHandler
    :param _mouse_press_start_column: column where mouse was pressed
    :type _mouse_press_start_column: int
    :param _mouse_press_start_row: row where mouse was pressed
    :type _mouse_press_start_row: int
    :param _mouse_press_phase: phase when mouse was pressed
    :type _mouse_press_phase: int
    :param _mouse_press_position: position of mouse press
    :type _mouse_press_position: tuple
    """

    def __init__(self, game_controller, button_handler):
        self._game_controller = game_controller
        self._button_handler = button_handler
        self._mouse_press_start_column = None
        self._mouse_press_start_row = None
        self._mouse_press_phase = None
        self._mouse_press_position = None

    @property
    def phase(self):
        return self._game_controller.phase

    def did_phase_change(self):
        """checks if phase has changed between mouse press and release"""
        return self.phase != self._mouse_press_phase

    def players_board_pressed(self, mouse_position):
        """checks if players board was pressed. If so saves row and column
        and returns True else False"""

        if self.phase not in [constants.GAME_PHASE, constants.POSITIONING_PHASE]:
            return False

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
        user has selected cells in one line. If so triggers right
        GameLogicController method and return True. Else return False"""

        if self.did_phase_change() or (
            self.phase not in [constants.GAME_PHASE, constants.POSITIONING_PHASE]
        ):
            return False

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
        """checks if enemy's board was pressed if so triggers right
        GameLogicController method and return True. Else returns False"""

        if self.phase not in [constants.GAME_PHASE, constants.POSITIONING_PHASE]:
            return False

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

        if self.did_phase_change():
            return False

        # checking if mouse press and release have occured on button
        button = self._button_handler.check_button_press(
            mouse_press_position=mouse_position,
            mouse_release_position=self._mouse_press_position,
        )

        if button is None:
            return False
        # calling right method
        if isinstance(button, PlayPVPButton):
            self._game_controller.game_mode_selected(constants.PVP)
        elif isinstance(button, PlayPVCButton):
            self._game_controller.game_mode_selected(constants.PVC)

        elif isinstance(button, SwitchUserButton):
            self._game_controller.switch_current_player()

        elif isinstance(button, ExitStartScreenButton):
            self._game_controller.exit_game()
        elif isinstance(button, ExitEndScreenButton):
            self._game_controller.exit_game()
        elif isinstance(button, MainMenuButton):
            self._game_controller.__init__()

        return True

    def mouse_button_interaction(self, mouse_position, is_pressed):
        """method checks which interaction has been performed"""
        if is_pressed:  # mouse button has been pressed
            self._mouse_press_position = mouse_position
            self._mouse_press_phase = self.phase

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
