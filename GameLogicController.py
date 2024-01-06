import constants
from Player import Player, BotPlayer
from GameErrors import NotSuchShipToPlaceError, ShipPlacingError, CellAlreadyShotError
from datetime import timedelta
import pygame


class GameLogicController:
    """handles logic of the game, turns, phases etc

    :param _board_height: how many cells does board have vertically
    :type _board_height: int
    :param _board_width: how many cells does board have horizontally
    :type _board_width: int
    :param _ship_configuration: represents how many ships of a kind player should place
    :type _ship_configuration: dict
    :param _game_is_running: if is's True game is running
    :type _game_is_running: bool
    :param _gamemode: stors id of gamemode (PVP or PVC)
    :type _gamemode: int
    :param _player1: player of the game(always human)
    :type _player1: Player.Player
    :param _player2: second player of game(human in PVP and bot in PVC)
    :type _player2: Player.Player
    :param _current_player: equal to currently playing player
    :type _current_player: Player.Player
    :param _player_attacked: equal to player that's not playing now (could be attacked)
    :type _player_attacked: Player.Player
    :param _phase_to_return: to which phase should game return after leaving blackscreen
    :type _phase_to_return: int
    :param _phase: represents current phase of game (start screen, poistioning..)
    :type _phase: int
    :param _prompts: list of prompts to display to user
    :type _prompts: list
    :param _game_start_time: stores moment in time when shooting phase started
    :type _game_start_time: int
    :param _game_play_time: how long has game been in game phase
    :type _game_play_time: datetime.timedelta
    :param _rounds_played: how many rounds have been played(round=player has attacked)
    :type _rounds_played: int
    :param _winner: instance of player that has won the game
    :type _winner: Player.Player
    :param _total_ship_segments: represents how many segments in total ships can have
    :type _total_ship_segments: int
    """

    def __init__(
        self,
        board_height=constants.BOARD_CELL_SIZE,
        board_width=constants.BOARD_CELL_SIZE,
        ship_configuration=constants.STANDARD_SHIP_QUANTITIES,
    ):
        self._board_height = board_height
        self._board_width = board_width
        self._ship_configuration = ship_configuration

        self._game_is_running = True
        self._gamemode = None
        self._player1 = None
        self._player2 = None
        self._current_player = None
        self._player_attacked = None

        self._phase_to_return = constants.POSITIONING_PHASE
        self._phase = constants.GAME_START_SCREEN

        self._prompts = []

        # variables for statistics
        self._game_start_time = pygame.time.get_ticks()
        self._game_play_time = timedelta(milliseconds=0)
        self._total_ship_segments = None
        self._rounds_played = 0
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

    @property
    def game_is_running(self):
        return self._game_is_running

    @property
    def rounds_played(self):
        return self._rounds_played

    @property
    def winner(self):
        return self._winner

    @property
    def winner_name(self):
        """returns winners name or None"""
        if self._winner is None:
            return None

        if self._gamemode == constants.PVP:
            if self._winner == self._player1:
                return "Player1"
            else:
                return "Player2"
        else:
            if self._winner == self._player1:
                return "Player"
            else:
                return "Bot"

    @property
    def game_play_time(self):
        """returns timedelta object with time spend on playing game"""
        if self._phase == constants.GAME_RESULT_PHASE:
            return timedelta(milliseconds=self._game_play_time)

        time = pygame.time.get_ticks() - self._game_start_time
        return timedelta(milliseconds=time)

    def get_play_time_as_str(self):
        """returns time spend playing as a formated str"""
        time_played = int(self.game_play_time.total_seconds())
        minutes, seconds = divmod(time_played, 60)
        hours, minutes = divmod(minutes, 60)

        output_text = ""
        if hours != 0:
            if hours == 1:
                output_text += str(hours) + " hour, "
            else:
                output_text += str(hours) + " hours, "
        if minutes != 0:
            if minutes == 1:
                output_text += str(minutes) + " minute, "
            else:
                output_text += str(minutes) + " minutes, "
        if seconds == 1:
            output_text += str(seconds) + " second"
        else:
            output_text += str(seconds) + " seconds"
        return output_text

    def get_player_names(self):
        """returns tuple of (current players name, opponent name)
        mainly for labeling tables"""
        if self._gamemode == constants.PVC:
            return ("Player", "Bot")
        else:
            if self._current_player == self._player1:
                return ("You - Player1", "Opponent - Player2")
            else:
                return ("You - Player2", "Opponent - Player1")

    def generate_statistics(self):
        """returns a dictionary of statistics"""
        statistics = {}
        statistics["Time of gameplay"] = str(self.get_play_time_as_str())
        statistics["Rounds played"] = str(self.rounds_played)
        statistics["Percentage of winners fleet intact"] = str(
            self.calculate_percentage_state_of_players_fleet(self.winner)
        )

        return statistics

    def fetch_prompt(self):
        """returns propt to display and removes it from queue
        or returns None if there are none."""
        if not self._prompts:
            return None
        prompt = self._prompts[0]
        self._prompts.remove(prompt)
        return prompt

    def calculate_players_alive_segments(self, player):
        """returns how many alive ship segments does player have"""
        player_alive_segments_counter = 0
        for ship in player.fleet:
            player_alive_segments_counter += ship.length - ship.hit_counter

        return player_alive_segments_counter

    def get_total_ship_segments(self):
        """retuns how many ship segments on player can have
        calculates this value if it has not been done previously"""
        if self._total_ship_segments is None:
            self._total_ship_segments = self.calculate_total_ship_segments
        return self._total_ship_segments()

    def calculate_total_ship_segments(self):
        """returns how many ship segments are in total"""
        total_segment_counter = 0
        for ship_name in constants.STANDARD_SHIP_QUANTITIES:
            quantity = constants.STANDARD_SHIP_QUANTITIES[ship_name]
            length = constants.SHIP_LENGTHS[ship_name]
            total_segment_counter += quantity * length

        return total_segment_counter

    def calculate_percentage_state_of_players_fleet(self, player):
        """returns percentage equal to total not shot ship segments
        divided by total amount of segments"""

        player_alive_segments_counter = self.calculate_players_alive_segments(player)
        total_segment_counter = self.get_total_ship_segments()

        try:
            return (player_alive_segments_counter * 100) // total_segment_counter
        except ZeroDivisionError:
            return 0

    def switch_current_player(self):
        """handles switching users in PVP"""
        if self._current_player == self._player1:
            self._current_player = self._player2
            self._player_attacked = self._player1
        else:
            self._current_player = self._player1
            self._player_attacked = self._player2

        self._phase = constants.BLACKSCREEN_PHASE

    def game_mode_selected(self, gamemode):
        """trigged when user(s) have selected gamemode, initializes players
        and in case of PVC bot places ships"""
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

        # setting phase and gamemode
        self._gamemode = gamemode
        self._phase = constants.POSITIONING_PHASE

        self._game_start_time = pygame.time.get_ticks()

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
            self._prompts.append("Not such ship to place")
        except ShipPlacingError:
            self._prompts.append("Cannot place ship here")

    def position_ships_phase(self, start_row, start_column, end_row, end_column):
        """handles game positioning phase"""
        # current player postions ships
        self.player_positions_ships(
            self._current_player, start_row, start_column, end_row, end_column
        )

        # switch phase if all players have placed ships
        if (not self._player1.ships_to_place) and (not self._player2.ships_to_place):
            self._prompts.append("All ships positioned")
            self._phase = constants.GAME_PHASE
            self._phase_to_return = constants.GAME_PHASE
            return

        # current player has placed all the ships and other player has not
        elif (
            not self._current_player.ships_to_place
        ) and self._gamemode == constants.PVP:
            self._phase = constants.READY_TO_SWITCH_PHASE
            self._prompts.append("All ships positioned")

    def play_game_phase(self, shot_row, shot_column):
        """handles main game phase(when player(s) shoot)"""
        # current player performs attack
        attack_status = None
        try:
            attack_status = self._current_player.perform_attack(
                opponent=self._player_attacked,
                target_x=shot_column,
                target_y=shot_row,
            )
        except CellAlreadyShotError:
            self._prompts.append("Already shot here, try elsewhere")
            return

        self._rounds_played += 1

        # check if current player has won
        if self._player_attacked.is_defeated:
            # current player has won
            self._game_play_time = pygame.time.get_ticks() - self._game_start_time
            self._winner = self._current_player
            self._phase = constants.GAME_RESULT_PHASE
            return

        # prompting user attack status
        if attack_status == constants.SHIP_HIT:
            self._prompts.append("You hit!")
        elif attack_status == constants.ATTACK_UNSUCCESSFUL:
            self._prompts.append("You missed!")
        elif attack_status == constants.SHIP_SUNK:
            self._prompts.append("You have shot down ship!")

        # swithcing current player or computer attacks
        if self._gamemode == constants.PVP:
            self._phase = constants.READY_TO_SWITCH_PHASE
        else:
            # computer performs attack
            self._player2.perform_attack(self._player1)
            # increment round counter
            self._rounds_played += 1
            # check if bot has won
            if self._current_player.is_defeated:
                self._winner = self._player2
                self._phase = constants.GAME_RESULT_PHASE
                self._game_play_time = pygame.time.get_ticks() - self._game_start_time
                return

    def exit_black_screen_phase(self):
        """method trigged when user have switch in real world
        and current user is ready to proceed"""
        self._phase = self._phase_to_return

    def players_cells_selected(self, start_row, start_column, end_row, end_column):
        """method trigger when user has selected cells on his own(left) board"""
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

    def exit_game(self):
        """method triggered to exit game"""
        self._game_is_running = False
