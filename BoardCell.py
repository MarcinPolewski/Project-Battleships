from GameErrors import OcupiedCellError, CellAlreadyShotError
import constants


class BoardCell:
    """represents a single cell/tile on game board

    :param _is_free: True if cell is empty(no ship on it)
    :type _is_free: bool
    :param _was_shot: True if cell has already been shot
    :type _was_shot: bool
    :param _ship_handle: pointer to instance of Ship class position here
    :type _ship_handle: Ships.Ship
    """

    def __init__(self):
        self._is_free = True
        self._was_shot = False

        self._ship_handle = None

    @property
    def is_free(self):
        return self._is_free

    @property
    def was_shot(self):
        return self._was_shot

    @property
    def ship_handle(self):
        return self._ship_handle

    def position_ship(self, new_ship):
        """positions provided ship on cell; accepts ONLY Ship class
        raises OcupiedCellError if cell isn't free"""
        if not self.is_free:
            raise OcupiedCellError()

        self._ship_handle = new_ship
        self._is_free = False

    def remove_ship(self):
        """removes ship from cell"""
        self._is_free = True
        self._ship_handle = None

    def handle_attack(self):
        """
        handles attack on signe cell, returns values:
        constants.ATTACK_UNSUCCESSFUL - when water was hit
        constants.SHIP_HIT - when ship was hit, but not sunk
        constants.SHIP_SUNK - when ship was hit and sunk

        raises CellAlreadyShotError if attack on this cell was
        already performed
        """

        if self.was_shot:
            raise CellAlreadyShotError

        self._was_shot = True

        if self.is_free:
            return constants.ATTACK_UNSUCCESSFUL
        # there's a ship
        is_ship_sunk = self.ship_handle.take_damage()

        # ship was definitely shot, we need to check if it's down

        return constants.SHIP_SUNK if is_ship_sunk else constants.SHIP_HIT
