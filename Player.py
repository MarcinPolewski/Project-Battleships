from GameErrors import CellAlreadyShotError, ShipPlacingError
from BoardCell import BoardCell
import constants
from Ships import Ship, Carrier, Battleship, Cruiser, PatrolShip

import numpy as np
import copy


class Player:
    """handles functionality of a player(mostly board)
    top left corner has coordinates equal to zero,
    they grow to the right and down

    :param board: stores array of BoardCell 's
    :param board_width: represents how many columns does the board have
    :param board_height: represent how many rows does the board have
    :param ship_configuration: specifies how many ships of particular class
    should be placed of board
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

        # initializing set of (column, row) representing
        # cooridnates of cells, where attack  wasn't performed
        for y_it in range(board_height):
            for x_it in range(board_width):
                self._potential_targets.append((y_it, x_it))

        # initializing ships
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
        for ship in self._fleet:
            if not ship.is_down():
                return False
        return True

    def Check_if_ship_can_be_placed(
        self, new_ship_length, orientation, coordinate_x, coordinate_y
    ):
        """
        raises errors if player does not have such ship to plac
        or if it is out of the board or if ther's a colision
        returns new_ship instance
        """
        # check if provided orientation is correct
        if (
            orientation != constants.SHIP_HORIZONTAL
            and orientation != constants.SHIP_VERTICAL
        ):
            raise ShipOrientationError()

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
        return attack_status

    def perform_attack(self, opponent, target_x, target_y):
        if (target_y, target_x) not in self._potential_targets:
            raise CellAlreadyShotError()
        attack_status = opponent.take_attack(target_x, target_y)
        return attack_status


class BotPlayer(Player):
    """automates some functionality of Player class, to create a game Bot"""
