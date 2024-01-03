from GameLogicController import GameLogicController
import constants
from Player import Player, BotPlayer
from GameErrors import NotSuchShipToPlaceError

import pytest


def test_GameLogicController_init(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()

    assert controller.phase == constants.GAME_START_SCREEN


def test_GameLogicController_gamemode_PVC(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVC)

    player = controller.player1
    bot = controller.player2

    assert controller.phase == constants.POSITIONING_PHASE
    assert controller.gamemode == constants.PVC
    assert isinstance(player, Player)
    assert isinstance(bot, BotPlayer)
    assert controller.current_player == player
    assert controller.player_attacked == bot

    # checking if bot has placed ships
    ship_segment_counter = 0
    bot_board = controller.player2.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = bot_board[row_idx, column_idx]
            if not board_cell.is_free:
                ship_segment_counter += 1

    assert ship_segment_counter == 9
    # checking if bot's ships have not been placed on players board
    ship_segment_counter = 0
    players_board = controller.player1.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players_board[row_idx, column_idx]
            if not board_cell.is_free:
                ship_segment_counter += 1

    assert ship_segment_counter == 0


def test_GameLogicController_gamemode_PVP(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVP)

    player1 = controller.player1
    player2 = controller.player2

    assert controller.phase == constants.POSITIONING_PHASE
    assert controller.gamemode == constants.PVP
    assert isinstance(player1, Player)
    assert isinstance(player2, Player)
    assert controller.current_player == player1
    assert controller.player_attacked == player2
    assert player1 != player2


def test_GameLogicController_switch_current_player(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
        "Battleship": 1,
        "Cruiser": 4,
        "PatrolShip": 3,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVP)

    player1 = controller.current_player
    player2 = controller.player_attacked

    assert controller.phase == constants.POSITIONING_PHASE

    controller.switch_current_player()
    assert controller.current_player == player2
    assert controller.player_attacked == player1
    assert player1 != player2
    assert controller.phase == constants.BLACKSCREEN_PHASE


def test_player_positions_ships_PVP(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVP)

    controller.player_positions_ships(
        player=controller.current_player,
        start_row=0,
        start_column=0,
        end_row=4,
        end_column=0,
    )

    # testing if ship is places correctly  on the board
    players1_board = controller.player1.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players1_board[row_idx, column_idx]
            if column_idx == 0 and row_idx >= 0 and row_idx <= 4:
                assert not board_cell.is_free
            else:
                assert board_cell.is_free

    # testing if ship has not been place on player2 noard
    players2_board = controller.player2.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players2_board[row_idx, column_idx]
            assert board_cell.is_free


def test_player_positions_ships_PVC(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVC)

    controller.player_positions_ships(
        player=controller.current_player,
        start_row=0,
        start_column=0,
        end_row=4,
        end_column=0,
    )

    # testing if ship is places correctly  on the board
    players1_board = controller.player1.board
    player_ship = None
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players1_board[row_idx, column_idx]
            if column_idx == 0 and row_idx >= 0 and row_idx <= 4:
                assert not board_cell.is_free
                player_ship = board_cell.ship_handle
            else:
                assert board_cell.is_free

    # testing if ship has not been place on player2 board
    bot_board = controller.player2.board
    bot_ship = None
    bot_ship_segment_counter = 0
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = bot_board[row_idx, column_idx]
            if not board_cell.is_free:
                bot_ship_segment_counter += 1
                bot_ship = board_cell.ship_handle
    assert bot_ship != player_ship
    assert bot_ship_segment_counter == 5

    # testing if current player has changes


def test_player_positions_ships_no_such_ship_to_place(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVC)

    # nie ma takiego statku do postawienia
    controller.player_positions_ships(
        player=controller.current_player,
        start_row=0,
        start_column=0,
        end_row=1,
        end_column=0,
    )

    # @TODO finish test


def test_player_positions_ships_ship_placing_error(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 2,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVC)

    # @TODO finish test (colision or out of the board)


def test_position_ship_phase_PVC(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVC)

    controller.position_ships_phase(
        start_row=0, start_column=0, end_column=0, end_row=4
    )

    # this function calls player_positions_ships so no need for further tests

    assert controller._phase == constants.GAME_PHASE


def test_position_ship_phase_PVP(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVP)

    controller.position_ships_phase(
        start_row=0, start_column=0, end_column=0, end_row=4
    )

    # player 1 should have placed ship and player 2 should not
    players1_board = controller.player1.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players1_board[row_idx, column_idx]
            if column_idx == 0 and row_idx >= 0 and row_idx <= 4:
                assert not board_cell.is_free
            else:
                assert board_cell.is_free

    players2_board = controller.player2.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players2_board[row_idx, column_idx]
            assert board_cell.is_free

    # testing if player2 has ships to place
    assert len(controller.player2.ships_to_place) == 1
    assert len(controller.player1.ships_to_place) == 0

    # testing if current player has changed
    assert controller.current_player == controller.player2
    assert controller.player_attacked == controller.player1
    assert controller.phase == constants.BLACKSCREEN_PHASE

    controller.exit_black_screen_phase()
    assert controller.phase == constants.POSITIONING_PHASE

    controller.position_ships_phase(
        start_row=0, start_column=9, end_column=9, end_row=4
    )

    # player 2 should have placed ships here and player 1 should not
    players1_board = controller.player1.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players1_board[row_idx, column_idx]
            if column_idx == 0 and row_idx >= 0 and row_idx <= 4:
                assert not board_cell.is_free
            else:
                assert board_cell.is_free

    players2_board = controller.player2.board
    for row_idx in range(board_cell_size):
        for column_idx in range(board_cell_size):
            board_cell = players2_board[row_idx, column_idx]
            if column_idx == 9 and row_idx >= 0 and row_idx <= 4:
                assert not board_cell.is_free
            else:
                assert board_cell.is_free

    # all ships have been placed, game phase should start
    assert controller._phase == constants.GAME_PHASE


def test_play_game_phase_PVP(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "Carrier": 1,
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    controller = GameLogicController()
    controller.game_mode_selected(gamemode=constants.PVP)

    # positioning player1 ships
    controller.position_ships_phase(
        start_row=0, start_column=0, end_column=0, end_row=4
    )

    controller.exit_black_screen_phase()

    # positioning player2 ships
    controller.position_ships_phase(
        start_row=0, start_column=9, end_column=9, end_row=4
    )

    assert controller.phase == constants.GAME_PHASE
    assert controller.current_player == controller.player2

    # player 2 is attacking
    assert not controller.player1.board[0, 0].was_shot
    controller.play_game_phase(shot_row=0, shot_column=0)
    # phase and current player should change
    assert controller.phase == constants.READY_TO_SWITCH_PHASE
    assert controller.current_player == controller.player2

    controller.switch_current_player()

    assert controller.phase == constants.BLACKSCREEN_PHASE
    assert controller.current_player == controller.player1
    # checking if attack was successful
    assert controller.player1.board[0, 0].was_shot

    controller.exit_black_screen_phase()

    # player 1 is attacking
    assert not controller.player2.board[0, 9].was_shot
    controller.play_game_phase(shot_row=0, shot_column=9)

    assert controller.phase == constants.READY_TO_SWITCH_PHASE
    assert controller.current_player == controller.player1

    controller.switch_current_player()
    # phase and current player should change
    assert controller.phase == constants.BLACKSCREEN_PHASE
    assert controller.current_player == controller.player2
    # checking if attack was successful
    assert controller.player2.board[0, 9].was_shot


def test_play_game_phase_PVC(monkeypatch):
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    standard_ship_quantities = {
        "PatrolShip": 1,  # lenght=2
    }
    monkeypatch.setattr("constants.STANDARD_SHIP_QUANTITIES", standard_ship_quantities)

    # custom board that fits only one patrol ship
    controller = GameLogicController(board_height=2, board_width=1)
    controller.game_mode_selected(gamemode=constants.PVC)

    # positioning player1 ships
    controller.position_ships_phase(
        start_row=0, start_column=0, end_column=0, end_row=1
    )

    player = controller.player1
    bot = controller.player2
    bot_hit_counter = 0

    # player1 attacks and bot does too
    controller.play_game_phase(shot_row=0, shot_column=0)
    # testing if bot was shot
    assert bot.board[0, 0].was_shot
    assert not bot.board[1, 0].was_shot

    # testing if bot shot player
    for row_idx in range(2):
        if player.board[row_idx, 0].was_shot:
            bot_hit_counter += 1

    # checking if phase and current player didnt change
    assert controller.phase == constants.GAME_PHASE
    assert controller.current_player == controller.player1


def test_game_result_phase(monkeypatch):
    assert False


def test_players_cells_selected(monkeypatch):
    assert False


def test_enemys_board_mouse_pressed(monkeypatch):
    assert False
