import constants
from Player import Player, BotPlayer
from GameErrors import NotSuchShipToPlaceError, ShipPlacingError


# @TODO delete, only for testing
from print_board_to_console import print_boards_to_console


class GameLogicController:
    """handles logic of the game, turns, phases etc"""

    def __init__(
        self,
        board_height=constants.BOARD_CELL_SIZE,
        board_width=constants.BOARD_CELL_SIZE,
        ship_configuration=constants.STANDARD_SHIP_QUANTITIES,
    ):
        self._board_height = board_height
        self._board_width = board_width
        self._ship_configuration = ship_configuration

        self._gamemode = None
        self._player1 = None
        self._player2 = None
        self._current_player = None
        self._player_attacked = None

        self._phase = constants.GAME_START_SCREEN

        self._winner = None

    @property
    def phase(self):
        return self._phase

    @property
    def gamemode(self):
        return self._gamemode

    @property
    def player1(self):
        return self._player1

    @property
    def player2(self):
        return self._player2

    @property
    def current_player(self):
        return self._current_player

    @property
    def player_attacked(self):
        return self._player_attacked

    def switch_current_player(self):
        if self._current_player == self._player1:
            self._current_player = self._player2
            self._player_attacked = self._player1
        else:
            self._current_player = self._player1
            self._player_attacked = self._player2

        self._phase = constants.BLACKSCREEN_PHASE

    def game_mode_selected(self, gamemode):
        # initializing players
        self._player1 = Player(
            board_height=self._board_height, board_width=self._board_width
        )
        if gamemode == constants.PVP:
            self._player2 = Player(
                board_height=self._board_height, board_width=self._board_width
            )
        else:
            self._player2 = BotPlayer(
                board_height=self._board_height, board_width=self._board_width
            )
            # bot places ships
            self._player2.position_ships()

        # setting up current player
        self._current_player = self._player1
        self._player_attacked = self._player2

        self._gamemode = gamemode
        self._phase = constants.POSITIONING_PHASE

    def player_positions_ships(
        self, player, start_row, start_column, end_row, end_column
    ):
        """method handles positioning of ships for one player"""

        # calculate orientation
        new_ship_orientation = (
            constants.SHIP_HORIZONTAL
            if start_row == end_row
            else constants.SHIP_VERTICAL
        )

        # selected cells are in one line, we try adding ship to player
        new_ship_length = abs((end_row - start_row) + (end_column - start_column)) + 1
        try:
            # taking min(), because add_ship takes top left corrner of ship
            player.add_ship(
                new_ship_length,
                new_ship_orientation,
                min(start_column, end_column),
                min(start_row, end_row),
            )
        except NotSuchShipToPlaceError:
            pass
            # @TODO add prompting user
        except ShipPlacingError:
            pass
            # @TODO add prompting user

    def position_ships_phase(self, start_row, start_column, end_row, end_column):
        # current player postions ships
        self.player_positions_ships(
            self._current_player, start_row, start_column, end_row, end_column
        )

        # switch phase if all players have placed ships
        if (not self._player1.ships_to_place) and (not self._player2.ships_to_place):
            self._phase = constants.GAME_PHASE
            return

        # current player has placed all the ships and other player has not
        elif (
            not self._current_player.ships_to_place
        ) and self._gamemode == constants.PVP:
            self.switch_current_player()

    def play_game_phase(self, shot_row, shot_column):
        # current player performs attack
        self._current_player.perform_attack(
            opponent=self._player_attacked,
            target_x=shot_column,
            target_y=shot_row,
        )

        # check if game is won
        if self._player1.is_defeated:
            # player 2 has won
            self._winner = self._player2
            self._phase = constants.GAME_RESULT_PHASE
            return
        elif self._player2.is_defeated:
            # player1 has won
            self._winner = self._player1
            self._phase = constants.GAME_RESULT_PHASE
            return

        # swithcing current player or computer attacks
        if self._gamemode == constants.PVP:
            self.switch_current_player()
        else:
            # computer performs attack
            self._player2.perform_attack(self._player1)

    def exit_black_screen_phase(self):
        self._phase = constants.GAME_PHASE

    def game_result_phase(self, mouse_was_pressed, mouse_was_released, mouse_position):
        pass
        # @TODO

    def button_pressed(self, button_type):
        # @FIXME nie trzeba dwa razy sprawdzać, juz kontroler patrzy
        # jaka jest faza
        if self._phase == constants.GAME_START_SCREEN:
            if button_type == constants.PVP_BUTTON:
                self.game_mode_selected(constants.PVP)
            elif button_type == constants.PVC_BUTTON:
                self.game_mode_selected(constants.PVC)
        elif self._phase == constants.GAME_RESULT_PHASE:
            if button_type == constants.PLAY_AGAIN_BUTTON:
                # @TODO
                pass
            elif button_type == constants.QUIT_BUTTON:
                # @TODO
                pass

        elif self._phase == constants.BLACKSCREEN_PHASE:
            # switching users at computer, switch screens
            pass

    def players_cells_selected(self, start_row, start_column, end_row, end_column):
        """method trigger when user has selected cells"""
        if self._phase == constants.POSITIONING_PHASE:
            self.position_ships_phase(
                start_row=start_row,
                start_column=start_column,
                end_row=end_row,
                end_column=end_column,
            )

    def enemys_board_mouse_pressed(self, row, column):
        """method trigger when user has clicked on enemys board"""
        if self._phase == constants.GAME_PHASE:
            self.play_game_phase(row, column)
