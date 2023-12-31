from GameErrors import ShipPlacingError, NotSuchShipToPlaceError
from BoardCell import BoardCell
from Player import Player, BotPlayer
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


def test_BotPlayer_init():
    bot = BotPlayer(board_height=10, board_width=15)
    assert bot.previous_attack() == (False, None, None)


def test_BotPlayer_find_new_target(monkeypatch):
    bot = BotPlayer(board_height=10, board_width=15)

    def return_previous(_):
        return (True, 1, 1)

    monkeypatch.setattr("Player.BotPlayer.previous_attack", return_previous)
    bot._previous_attack = (True, 1, 1)
    new_target = bot.find_new_target()

    assert (
        new_target == (0, 1)
        or new_target == (1, 0)
        or new_target == (1, 2)
        or new_target == (2, 1)
    )


def test_BotPlayer_find_new_target_corner(monkeypatch):
    bot = BotPlayer(board_height=5, board_width=5)

    def return_previous(_):
        return (True, 4, 4)

    monkeypatch.setattr("Player.BotPlayer.previous_attack", return_previous)
    bot._previous_attack = (True, 1, 1)
    new_target = bot.find_new_target()

    assert new_target == (4, 3) or new_target == (3, 4)


def test_BotPlayer_find_new_target_random():
    bot = BotPlayer(board_height=5, board_width=5)
    coordinate_y, coordinate_x = bot.find_new_target()
    assert (coordinate_y, coordinate_x) in bot.potential_targets


def test_BotPlayer_preform_attack(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    bot = BotPlayer(board_height=3, board_width=1)
    player = Player(3, 1)
    player.add_ship(3, constants.SHIP_VERTICAL, 0, 0)
    ship_handle = player.board[0, 0].ship_handle

    bot.perform_attack(player)
    assert ship_handle.hit_counter == 1
    assert len(bot.potential_targets) == 2

    bot.perform_attack(player)
    assert ship_handle.hit_counter == 2
    assert len(bot.potential_targets) == 1

    bot.perform_attack(player)
    assert ship_handle.hit_counter == 3
    assert len(bot.potential_targets) == 0


def test_BotPlayer_perform_attack_adjusting_potential_targets(monkeypatch):
    def return_new_target(_):
        return (2, 2)

    monkeypatch.setattr("Player.BotPlayer.find_new_target", return_new_target)

    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    bot = BotPlayer(board_height=10, board_width=10)
    player = Player(board_height=10, board_width=10)

    player.add_ship(5, constants.SHIP_HORIZONTAL, 2, 2)
    bot.perform_attack(player)

    assert (2, 2) not in bot.potential_targets
    assert len(bot.potential_targets) == 99


def test_BotPlayer_position_ships(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        # "Battleship": 0,
        # "Cruiser": 0,
        # "PatrolShip": 0,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    bot = BotPlayer(5, 1)
    bot.position_ships()
    assert len(bot.fleet) == 1
    for i in range(5):
        assert not bot.board[i, 0].is_free


def test_BotPlayer_position_ships_standard_size(monkeypatch):
    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    bot = BotPlayer(10, 10)
    assert len(bot.ships_to_place) == 9

    bot.position_ships()
    assert len(bot.ships_to_place) == 0
    assert len(bot.fleet) == 9
