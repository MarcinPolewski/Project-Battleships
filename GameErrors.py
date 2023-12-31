"""contains all custom errors"""


class OcupiedCellError(Exception):
    def __init__(self):
        super().__init__("Ship cannot be placed on ocupied cell")


class CellAlreadyShotError(Exception):
    def __init__(self):
        super().__init__("Shot at this cell was already performed")


class ShipPlacingError(Exception):
    def __init__(self):
        super().__init__(
            "ship cannot be placed at this position(colision or outside the board)"
        )


class NotSuchShipToPlaceError(Exception):
    def __init__(self, lenght):
        super().__init__("player does not have a ship of length={lenght} to place")
        self._lenght = lenght
