from Ships import Ship, Battleship, Carrier, Cruiser, PatrolShip
import constants


def test_Ship_init():
    lajba = Ship(5)
    assert lajba.length == 5


def test_is_down():
    lajba = Ship(5)
    assert not lajba.is_down()


def test_position_ship():
    lajba = Ship(5)
    lajba.position_ship()
    assert lajba.is_positioned


def test_Ship_take_damage():
    lajba = Ship(2)

    assert lajba.hit_counter == 0

    lajba.take_damage()
    assert lajba.hit_counter == 1

    lajba.take_damage()
    assert lajba.hit_counter == 2

    lajba.take_damage()
    assert lajba.hit_counter == 2


def test_Ship_is_down():
    lajba = Ship(3)
    assert not lajba.is_down()

    for _ in range(3):
        lajba.take_damage()
    assert lajba.is_down()


def test_Carrier():
    c = Carrier()
    assert c.length == constants.CARRIER_LENGTH


def test_Battleship():
    b = Battleship()
    assert b.length == constants.BATTLESHIP_LENGTH


def test_Cruiser():
    c = Cruiser()
    assert c.length == constants.CRUISER_LENGTH


def test_PatrolShip():
    p = PatrolShip()
    assert p.length == constants.PATROL_SHIP_LENGTH
