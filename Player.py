from GameErrors import CellAlreadyShotError, ShipPlacingError, NotSuchShipToPlaceError
from BoardCell import BoardCell
import constants
from Ships import Carrier, Battleship, Cruiser, PatrolShip

import numpy as np
import copy
import random


class Player:
    """handles functionality of a player(mostly board)
    top left corner has coordinates equal to zero,
    they grow to the right and down

    :param _board: stores array of BoardCell 's
    :type _board: numpy array
    :param _board_width: represents how many columns does the board have
    :type _board_width: int
    :param _board_height: represent how many rows does the board have
    :type _board_height: int
    :param _potential_targets: list of (row, colum) where player didn't shoot
    :type _potential_targets: list
    :param _fleet: list of ships that player has currently on the board
    :type _fleet: list
    :param _ships_to_place: list of ships that user should place
    :type _ships_to_place: list


    """

    def __init__(
        self,
        board_height=constants.BOARD_CELL_SIZE,
        board_width=constants.BOARD_CELL_SIZE,
    ):
        self._board_height = board_height
        self._board_width = board_width
        self._potential_targets = []
        self._fleet = []
        self._ships_to_place = []

        # initializing board array - can be done neeter???
        boardcell = BoardCell()
        self._board = np.full((board_height, board_width), boardcell)
        for row in range(board_height):
            for column in range(board_width):
                self._board[row][column] = copy.deepcopy(boardcell)

        # initializing potential targets
        for y_it in range(board_height):
            for x_it in range(board_width):
                self._potential_targets.append((y_it, x_it))

        # initializing ships to place
        for ship_name in constants.STANDARD_SHIP_QUANTITIES:
            quantity = constants.STANDARD_SHIP_QUANTITIES[ship_name]
            if ship_name == "Carrier":
                for _ in range(quantity):
                    self._ships_to_place.append(Carrier())
            elif ship_name == "Battleship":
                for _ in range(quantity):
                    self._ships_to_place.append(Battleship())
            elif ship_name == "Cruiser":
                for _ in range(quantity):
                    self._ships_to_place.append(Cruiser())
            elif ship_name == "PatrolShip":
                for _ in range(quantity):
                    self._ships_to_place.append(PatrolShip())

    @property
    def potential_targets(self):
        return self._potential_targets

    @property
    def board(self):
        return self._board

    @property
    def board_height(self):
        return self._board_height

    @property
    def board_width(self):
        return self._board_width

    @property
    def fleet(self):
        """returns list of player's ships"""
        return self._fleet

    @property
    def ships_to_place(self):
        return self._ships_to_place

    @property
    def is_defeated(self):
        """returns True if player is defeated"""
        return False if self._fleet else True

    def Check_if_ship_can_be_placed(
        self, new_ship_length, orientation, coordinate_x, coordinate_y
    ):
        """
        raises errors if player does not have such ship to plac
        or if it is out of the board or if ther's a colision
        if ship can be placed returns new_ship instance
        """

        # check if ship fits on the board
        if orientation == constants.SHIP_VERTICAL and (
            coordinate_x < 0
            or coordinate_x > self.board_width
            or coordinate_y < 0
            or coordinate_y + new_ship_length > self.board_height
        ):
            raise ShipPlacingError()

        if orientation == constants.SHIP_HORIZONTAL and (
            coordinate_x < 0
            or coordinate_x + new_ship_length > self.board_width
            or coordinate_y < 0
            or coordinate_y > self.board_height
        ):
            raise ShipPlacingError()

        # check if there aren't any colisions with other ships
        if orientation == constants.SHIP_HORIZONTAL:
            for cell in self.board[
                coordinate_y, coordinate_x : coordinate_x + new_ship_length
            ]:
                if not cell.is_free:
                    raise ShipPlacingError()
        else:  # orientation vertical
            for cell in self.board[
                coordinate_y : coordinate_y + new_ship_length, coordinate_x
            ]:
                if not cell.is_free:
                    raise ShipPlacingError()

        # chcecks if player has such ship to place
        new_ship = None
        for ship in self._ships_to_place:
            if ship.length == new_ship_length:
                new_ship = ship
                self._ships_to_place.remove(ship)
                break
        if new_ship is None:
            raise NotSuchShipToPlaceError(new_ship_length)

        return new_ship

    def add_ship(self, length, orientation, coordinate_x, coordinate_y):
        """
        places ship of length on to the GameBoard,
        if player has not such ship to place, raises
        NotSuchShipToPlaceError
        """

        # raises SHipPlacingError or NotSuchShipToPlaceError
        new_ship = self.Check_if_ship_can_be_placed(
            length, orientation, coordinate_x, coordinate_y
        )

        new_ship_length = new_ship.length
        if orientation == constants.SHIP_HORIZONTAL:
            for cell in self.board[
                coordinate_y, coordinate_x : coordinate_x + new_ship_length
            ]:
                cell.position_ship(new_ship=new_ship)

        else:  # orientation vertical
            for cell in self.board[
                coordinate_y : coordinate_y + new_ship_length, coordinate_x
            ]:
                cell.position_ship(new_ship=new_ship)

        new_ship.position_ship()
        self._fleet.append(new_ship)

    def take_attack(self, coordinate_x, coordinate_y):
        """
        performs an atack on a single cell, it returns values
        constants.ATTACK_UNSUCCESSFUL - when water was hit
        constants.SHIP_HIT - when ship was hit, but not sunk
        constants.SHIP_SUNK - when ship was hit and sunk
        """
        cell = self._board[coordinate_y, coordinate_x]
        attack_status = cell.handle_attack()
        if attack_status == constants.SHIP_SUNK:
            self._fleet.remove(cell.ship_handle)
        return attack_status

    def perform_attack(self, opponent, target_x, target_y):
        """handles performing attack, raised CellAlreadyShotError
        or returns attack_status"""
        if (target_y, target_x) not in self._potential_targets:
            raise CellAlreadyShotError()
        attack_status = opponent.take_attack(target_x, target_y)
        return attack_status


class BotPlayer(Player):
    """automates some functionality of Player class, to create a game Bot

    Inherited from player class:
    :param _board: stores array of BoardCell 's
    :type _board: numpy array
    :param _board_width: represents how many columns does the board have
    :type _board_width: int
    :param _board_height: represent how many rows does the board have
    :type _board_height: int
    :param _potential_targets: list of (row, colum) where player didn't shoot
    :type _potential_targets: list
    :param _fleet: list of ships that player has currently on the board
    :type _fleet: list
    :param _ships_to_place: list of ships that user should place
    :type _ships_to_place: list

    Bot specyfic:
    :param _first_hit_of_ship_position: stores (row, column) of first ship hit
    :type _first_hit_of_ship_position: tuple
    :param _next_targets: list of next targets of bot - there will attack
    :type _next_targets: list
    """

    def __init__(
        self,
        board_height=constants.BOARD_CELL_SIZE,
        board_width=constants.BOARD_CELL_SIZE,
    ):
        super().__init__(board_height=board_height, board_width=board_width)
        self._first_hit_of_ship_position = None
        self._next_targets = []

    @property
    def next_targets(self):
        return self._next_targets

    def find_new_target(self):
        """returns (y,x) coordinates of next targeted BoardCell"""

        if self._next_targets:
            return random.choice(self._next_targets)

        new_target_y, new_target_x = random.choice(self._potential_targets)
        return (new_target_y, new_target_x)

    def add_next_target(self, next_target):
        """adds next target to bot's list"""
        if next_target is not None:
            self._next_targets.append(next_target)

    def look_for_target_above(self, target_y, target_x, opponents_board):
        """adds potential targets in line, above current shot"""
        # from target_y-1  to 0 inclusive
        for new_target_y in range(target_y - 1, -1, -1):
            if (new_target_y, target_x) in self._potential_targets:
                self._next_targets.append((new_target_y, target_x))
                return
            elif opponents_board[new_target_y, target_x].is_free:
                # we shot here and it is see
                return

    def look_for_target_below(self, target_y, target_x, opponents_board):
        """adds potential targets in line, below current shot"""
        # from target_y + 1 to the board_height-1 inclusive
        for new_target_y in range(target_y + 1, self._board_height):
            if (new_target_y, target_x) in self._potential_targets:
                self._next_targets.append((new_target_y, target_x))
                return
            elif opponents_board[new_target_y, target_x].is_free:
                # we shot here and it is see
                return

    def look_for_target_to_the_left(self, target_y, target_x, opponents_board):
        """adds potential targets in line, to the left of current shot"""
        # from target_x-1  to 0 inclusive
        for new_target_x in range(target_x - 1, -1, -1):
            if (target_y, new_target_x) in self._potential_targets:
                self._next_targets.append((target_y, new_target_x))
                return
            elif opponents_board[target_y, new_target_x].is_free:
                # we shot here and it is see
                return

    def look_for_target_to_the_right(self, target_y, target_x, opponents_board):
        """adds potential targets in line, to the right of current shot"""
        # from target_y-1  to 0 inclusive
        for new_target_x in range(target_x + 1, self._board_width):
            if (target_y, new_target_x) in self._potential_targets:
                self._next_targets.append((target_y, new_target_x))
                return
            elif opponents_board[target_y, new_target_x].is_free:
                # we shot here and it is see
                return

    def look_for_targets_in_line(self, target_y, target_x, line_vertical, opponent):
        """looks for targets in line with previous
        shots(after bot got two shots in line)"""
        self._next_targets = []
        opponents_board = opponent.board
        if line_vertical:  # two ship segments have been shot in vertical line
            self.look_for_target_above(target_y, target_x, opponents_board)
            self.look_for_target_below(target_y, target_x, opponents_board)
        else:  # line horizontal
            self.look_for_target_to_the_right(target_y, target_x, opponents_board)
            self.look_for_target_to_the_left(target_y, target_x, opponents_board)

    def handle_next_targets(self, attack_status, target_y, target_x, opponent):
        """handled next targets for bot"""
        if attack_status == constants.SHIP_SUNK:
            self._next_targets = []
        elif attack_status == constants.SHIP_HIT:
            if not self._next_targets:
                # first shot of ship - bot will try shooting around until hits

                # adding next targets
                if (target_y + 1, target_x) in self._potential_targets:
                    self._next_targets.append((target_y + 1, target_x))
                if (target_y, target_x + 1) in self._potential_targets:
                    self._next_targets.append((target_y, target_x + 1))
                if (target_y - 1, target_x) in self._potential_targets:
                    self._next_targets.append((target_y - 1, target_x))
                if (target_y, target_x - 1) in self._potential_targets:
                    self._next_targets.append((target_y, target_x - 1))

                self._first_hit_of_ship_position = (target_y, target_x)
            else:
                # second hit of ship next targets should be performed in line
                first_hit_y, first_hit_x = self._first_hit_of_ship_position
                if first_hit_y == target_y:
                    # ship is horizontal - updating next targets
                    self.look_for_targets_in_line(
                        target_y=target_y,
                        target_x=target_x,
                        line_vertical=False,
                        opponent=opponent,
                    )
                else:
                    # ship is vertical - updating next targets
                    self.look_for_targets_in_line(
                        target_y=target_y,
                        target_x=target_x,
                        line_vertical=True,
                        opponent=opponent,
                    )

        if (target_y, target_x) in self._next_targets:
            self._next_targets.remove((target_y, target_x))
        self._potential_targets.remove((target_y, target_x))

    def perform_attack(self, opponent):
        """
        if previous attack was success full, bot will shoot
        at surrounding cells
        """

        # bot has no potential targes, so it cannot perform
        if not self._potential_targets:
            return

        new_target_y, new_target_x = self.find_new_target()

        # performing an attack
        attack_status = opponent.take_attack(
            coordinate_x=new_target_x, coordinate_y=new_target_y
        )

        self.handle_next_targets(attack_status, new_target_y, new_target_x, opponent)

    def position_ships(self):
        """handles positioning ships on the board"""
        while self._ships_to_place:
            ship_to_position = self._ships_to_place[0]
            is_positioned = False
            while not is_positioned:
                try:
                    rand_x = random.randint(0, self.board_width - 1)
                    rand_y = random.randint(0, self.board_height - 1)
                    rand_orientation = random.choice(
                        [constants.SHIP_VERTICAL, constants.SHIP_HORIZONTAL]
                    )
                    self.add_ship(
                        ship_to_position.length, rand_orientation, rand_x, rand_y
                    )
                    is_positioned = True
                except Exception:
                    """we do not want to do anything, when bot cannot place ship
                    where it can't"""
                    pass
