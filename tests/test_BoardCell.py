import pytest

from BoardCell import BoardCell
from Ships import Ship
import constants
from GameErrors import OcupiedCellError


def test_BoardCell_init():
    a = BoardCell()
    assert a.is_free
    assert a.ship_handle is None
    assert not a.was_shot


def test_BoardCell_position_ship_and_remove_ship():
    a = BoardCell()
    s = Ship(5)

    assert a.is_free
    assert a.ship_handle is None

    a.position_ship(s)
    assert not a.is_free
    assert a.ship_handle == s

    a.remove_ship()
    assert a.is_free
    assert a.ship_handle is None


def test_BoardCell_position_ship_ocupied_cell():
    a = BoardCell()
    s1 = Ship(5)
    s2 = Ship(5)

    a.position_ship(s1)
    with pytest.raises(OcupiedCellError):
        a.position_ship(s2)


def test_BoardCell_handle_attack():
    a = BoardCell()
    s = Ship(5)
    a.position_ship(s)

    attack_status = a.handle_attack()
    assert attack_status == constants.SHIP_HIT

    b = BoardCell()
    attack_status = b.handle_attack()
    assert attack_status == constants.ATTACK_UNSUCCESSFUL

    c = BoardCell()
    s = Ship(1)
    c.position_ship(s)

    attack_status = c.handle_attack()
    assert attack_status == constants.SHIP_SUNK
