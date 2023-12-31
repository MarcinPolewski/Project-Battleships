from GameErrors import ShipPlacingError, NotSuchShipToPlaceError
from BoardCell import BoardCell
from Player import Player
import constants
from Ships import Ship, Carrier, Battleship, Cruiser, PatrolShip

import pytest


def test_Player_init(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)
    player1 = Player()
    assert player1.board_height == 10
    assert player1.board_width == 10

    # sprawdzamy czy tablica ma 10 wierszy
    assert len(player1.board) == 10
    # sprawdzamy czy tablica ma 10 kolumn
    assert len(player1.board[0]) == 10

    # czy elementy są odpowiedniego typu
    assert isinstance(player1.board[0, 0], BoardCell)

    # czy elementy nie wskazują na ten sam obiekt
    s = Ship(5)
    player1.board[0, 0].position_ship(s)
    assert player1.board[0, 0].is_free == False
    assert player1.board[1, 0].is_free == True


def test_Player_init_ships_to_position(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)
    player1 = Player(10, 10)

    assert len(player1.ships_to_place) == 9

    carrier_couter = 0
    battleship_counter = 0
    cruiser_counter = 0
    patrol_ship_counter = 0
    set_of_ship_instances = set()
    for ship in player1.ships_to_place:
        set_of_ship_instances.add(ship)
        if isinstance(ship, Carrier):
            carrier_couter += 1
        elif isinstance(ship, Battleship):
            battleship_counter += 1
        elif isinstance(ship, Cruiser):
            cruiser_counter += 1
        elif isinstance(ship, PatrolShip):
            patrol_ship_counter += 1

    # check if all ships point to other instances
    assert len(set_of_ship_instances) == 9
    assert carrier_couter == 1
    assert battleship_counter == 1
    assert cruiser_counter == 4
    assert patrol_ship_counter == 3


def test_Player_fleet(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(10, 10)
    assert player1.fleet == []

    player1.add_ship(5, constants.SHIP_VERTICAL, coordinate_x=0, coordinate_y=0)
    assert len(player1.fleet) == 1
    assert isinstance(player1.fleet[0], Carrier)
    for ship in player1.ships_to_place:
        assert not isinstance(ship, Carrier)

    player1.add_ship(4, constants.SHIP_VERTICAL, coordinate_x=1, coordinate_y=0)
    assert len(player1.fleet) == 2
    assert isinstance(player1.fleet[0], Carrier)
    assert isinstance(player1.fleet[1], Battleship)
    for ship in player1.ships_to_place:
        assert not isinstance(ship, Carrier)
        assert not isinstance(ship, Battleship)


def test_Player_is_defeated(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(board_height=5, board_width=10)

    player1.add_ship(3, constants.SHIP_VERTICAL, 0, 0)
    assert player1.is_defeated == False
    player1.take_attack(0, 0)
    assert player1.is_defeated == False
    player1.take_attack(0, 1)
    assert player1.is_defeated == False
    player1.take_attack(0, 2)
    assert player1.is_defeated == True


def test_Player_potential_targets():
    player1 = Player(board_height=2, board_width=3)

    assert len(player1.potential_targets) == 6

    assert (0, 0) in player1._potential_targets
    assert (0, 1) in player1._potential_targets
    assert (0, 2) in player1._potential_targets
    assert (1, 0) in player1._potential_targets
    assert (1, 1) in player1._potential_targets
    assert (1, 2) in player1._potential_targets


def test_Player_add_ship_that_player_does_not_have(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(10, 10)

    player1.add_ship(
        length=5, orientation=constants.SHIP_HORIZONTAL, coordinate_x=0, coordinate_y=0
    )

    with pytest.raises(NotSuchShipToPlaceError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_HORIZONTAL,
            coordinate_x=0,
            coordinate_y=1,
        )

    with pytest.raises(NotSuchShipToPlaceError):
        player1.add_ship(
            length=3,
            orientation=constants.SHIP_HORIZONTAL,
            coordinate_x=0,
            coordinate_y=1,
        )


def test_Player_add_ship_Vertical(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(board_height=10, board_width=15)

    player1.add_ship(
        5,
        orientation=constants.SHIP_VERTICAL,
        coordinate_x=1,
        coordinate_y=1,
    )

    for row_index in range(10):
        for column_index in range(15):
            if (
                column_index == 1
                and 1 <= row_index
                and row_index <= constants.CARRIER_LENGTH
            ):
                # there should be carrier
                assert player1.board[row_index, column_index].is_free == False
                assert isinstance(
                    player1.board[row_index, column_index].ship_handle, Carrier
                )
            else:
                assert player1.board[row_index, column_index].is_free == True
                assert player1.board[row_index, column_index].ship_handle == None


def test_Player_add_ship_Horizontal(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(board_height=10, board_width=15)

    player1.add_ship(
        length=5,
        orientation=constants.SHIP_HORIZONTAL,
        coordinate_x=1,
        coordinate_y=1,
    )

    for row_index in range(10):
        for column_index in range(15):
            if row_index == 1 and column_index >= 1 and column_index <= 5:
                # there should be carrier
                assert player1.board[row_index, column_index].is_free == False
                assert isinstance(
                    player1.board[row_index, column_index].ship_handle, Carrier
                )
            else:
                assert player1.board[row_index, column_index].is_free == True
                assert player1.board[row_index, column_index].ship_handle == None


def test_Player_add_ship_out_of_board(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)
    player1 = Player(board_height=6, board_width=4)

    with pytest.raises(ShipPlacingError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_VERTICAL,
            coordinate_x=0,
            coordinate_y=6,
        )

    with pytest.raises(ShipPlacingError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_VERTICAL,
            coordinate_x=4,
            coordinate_y=5,
        )

    with pytest.raises(ShipPlacingError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_HORIZONTAL,
            coordinate_x=2,
            coordinate_y=5,
        )

    with pytest.raises(ShipPlacingError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_HORIZONTAL,
            coordinate_x=1,
            coordinate_y=0,
        )

    with pytest.raises(ShipPlacingError):
        player1.add_ship(
            length=5,
            orientation=constants.SHIP_VERTICAL,
            coordinate_x=1,
            coordinate_y=3,
        )


def test_Player_add_ship_coilsion(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(board_height=4, board_width=4)
    ps1 = 3
    ps2 = 3
    player1.add_ship(ps1, constants.SHIP_VERTICAL, 0, 0)

    with pytest.raises(ShipPlacingError):
        player1.add_ship(ps2, constants.SHIP_HORIZONTAL, 0, 1)
    with pytest.raises(ShipPlacingError):
        player1.add_ship(ps2, constants.SHIP_HORIZONTAL, 0, 0)


def test_Player_take_attack(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(board_height=4, board_width=4)
    ps1 = 3
    ps2 = 3
    player1.add_ship(ps1, constants.SHIP_VERTICAL, 0, 0)
    player1.add_ship(ps2, constants.SHIP_VERTICAL, 1, 0)

    assert player1.board[0, 0].ship_handle.is_down() == False

    # testing return staus and if BoardCell and Ship behave correctyl
    assert player1.take_attack(0, 0) == constants.SHIP_HIT
    assert player1.board[0, 0].ship_handle.hit_counter == 1  # is_segment_hit(0)

    assert player1.take_attack(0, 1) == constants.SHIP_HIT
    assert player1.board[0, 0].ship_handle.hit_counter == 2  # is_segment_hit(1)

    assert player1.take_attack(0, 2) == constants.SHIP_SUNK
    assert player1.board[0, 0].ship_handle.hit_counter == 3  # is_segment_hit(2)

    assert player1.board[0, 0].ship_handle.is_down()

    # testing if attacking 1st ship hadn't impact on second one
    assert (
        player1.board[0, 1].ship_handle.hit_counter == 0
    )  # is_segment_hit(0) == False
    assert (
        player1.board[1, 1].ship_handle.hit_counter == 0
    )  # is_segment_hit(1) == False
    assert player1.board[1, 1].ship_handle.is_down() == False


def test_Player_perform_attack(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    player1 = Player(10, 10)
    player2 = Player(10, 10)

    # adding two ships of length 3
    player1.add_ship(3, constants.SHIP_VERTICAL, 0, 0)
    player2.add_ship(3, constants.SHIP_VERTICAL, 0, 0)

    attack_status = player2.perform_attack(player1, 0, 0)
    assert attack_status == constants.SHIP_HIT
    assert player2.board[0, 0].ship_handle.hit_counter == 0
    assert player1.board[0, 0].ship_handle.hit_counter == 1

    attack_status = player2.perform_attack(player1, 0, 1)
    assert attack_status == constants.SHIP_HIT
    assert player2.board[0, 0].ship_handle.hit_counter == 0
    assert player1.board[0, 0].ship_handle.hit_counter == 2

    attack_status = player2.perform_attack(player1, 0, 2)
    assert attack_status == constants.SHIP_SUNK
    assert player2.board[0, 0].ship_handle.hit_counter == 0
    assert player1.board[0, 0].ship_handle.hit_counter == 3

    assert player1.board[0, 0].ship_handle.is_down()
