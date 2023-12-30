import constants


class Ship:
    """represents single ship on gameboard

    :param length: represents how many board cells does this ship occupy
    :param is_segemnt_hit: list representing if part of ship was shot
    """

    def __init__(self, length):
        self._length = length
        self._hit_counter = 0
        self._is_positioned = False

    @property
    def length(self):
        return self._length

    @property
    def hit_counter(self):
        return self._hit_counter

    @property
    def is_positioned(self):
        return self._is_positioned

    def is_down(self):
        return self._hit_counter == self._length

    def take_damage(self):
        self._hit_counter += 1
        self._hit_counter = min(self._hit_counter, self._length)

        # check if whole ship is down(return true if it is)
        return True if self.is_down() else False

    def position_ship(self):
        self._is_positioned = True


class Carrier(Ship):
    def __init__(self):
        super().__init__(length=constants.CARRIER_LENGTH)


class Battleship(Ship):
    def __init__(self):
        super().__init__(length=constants.BATTLESHIP_LENGTH)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(length=constants.CRUISER_LENGTH)


class PatrolShip(Ship):
    def __init__(self):
        super().__init__(length=constants.PATROL_SHIP_LENGTH)
