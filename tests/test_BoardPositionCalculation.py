from BoardPositionCalculations import (
    verify_row_and_column,
    calculate_row_and_column,
    calculate_x_y_cooridantes,
)
from GameErrors import OutOfTableError
import pytest


def test_verify_row_and_column(monkeypatch):
    # monkeypatching constants
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)

    verify_row_and_column(5, 5)
    verify_row_and_column(0, 5)
    verify_row_and_column(5, 0)
    verify_row_and_column(0, 0)
    verify_row_and_column(9, 9)

    with pytest.raises(OutOfTableError):
        verify_row_and_column(10, 0)
    with pytest.raises(OutOfTableError):
        verify_row_and_column(0, 10)
    with pytest.raises(OutOfTableError):
        verify_row_and_column(10, 10)
    with pytest.raises(OutOfTableError):
        verify_row_and_column(15, 15)
    with pytest.raises(OutOfTableError):
        verify_row_and_column(-1, 0)
    with pytest.raises(OutOfTableError):
        verify_row_and_column(10, -10)


def test_calculate_row_and_column(monkeypatch):
    # monkeypatching constants
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)
    screen_height = 900
    monkeypatch.setattr("constants.SCREEN_HEIGHT", screen_height)
    screen_width = 1600
    monkeypatch.setattr("constants.SCREEN_WIDTH", screen_width)
    table_horizontal_offset = 150
    monkeypatch.setattr("constants.TABLE_HORIZONTAL_OFFSET", table_horizontal_offset)
    table_vertical_offset = 100
    monkeypatch.setattr("constants.TABLE_VERTICAL_OFFSET", table_vertical_offset)
    table_size = 600
    monkeypatch.setattr("constants.TABLE_SIZE", table_size)
    cell_size = 60
    monkeypatch.setattr("constants.CELL_SIZE", cell_size)

    # test 1
    coordinates = (150 + 10, 100 + 10)
    row, column = calculate_row_and_column(
        coordinates=coordinates, from_left_table=True
    )
    assert row == 0
    assert column == 0

    # test 2
    coordinates = (150 + 60 + 60 + 10, 100 + 10)
    row, column = calculate_row_and_column(
        coordinates=coordinates, from_left_table=True
    )
    assert row == 0
    assert column == 2

    # test 3
    coordinates = (150 + 60 + 60 + 10, 100 + 60 + 10)
    row, column = calculate_row_and_column(
        coordinates=coordinates, from_left_table=True
    )
    assert row == 1
    assert column == 2

    # test 4
    coordinates = (150 + 60 + 60 + 10 + 600 + 100, 100 + 60 + 10)
    row, column = calculate_row_and_column(
        coordinates=coordinates, from_left_table=False
    )
    assert row == 1
    assert column == 2


def test_calculate_x_y_coordinates(monkeypatch):
    # monkeypatching constants
    board_cell_size = 10
    monkeypatch.setattr("constants.BOARD_CELL_SIZE", board_cell_size)
    screen_height = 900
    monkeypatch.setattr("constants.SCREEN_HEIGHT", screen_height)
    screen_width = 1600
    monkeypatch.setattr("constants.SCREEN_WIDTH", screen_width)
    table_horizontal_offset = 150
    monkeypatch.setattr("constants.TABLE_HORIZONTAL_OFFSET", table_horizontal_offset)
    table_vertical_offset = 100
    monkeypatch.setattr("constants.TABLE_VERTICAL_OFFSET", table_vertical_offset)
    table_size = 600
    monkeypatch.setattr("constants.TABLE_SIZE", table_size)
    cell_size = 60
    monkeypatch.setattr("constants.CELL_SIZE", cell_size)

    x, y = calculate_x_y_cooridantes(row=0, column=0, from_left_table=True)
    assert x == 150
    assert y == 100

    x, y = calculate_x_y_cooridantes(row=0, column=0, from_left_table=False)
    assert x == 150 + 600 + 100
    assert y == 100

    x, y = calculate_x_y_cooridantes(row=5, column=5, from_left_table=True)
    assert x == 150 + (5 * 60)
    assert y == 100 + (5 * 60)

    x, y = calculate_x_y_cooridantes(row=5, column=5, from_left_table=False)
    assert x == 150 + 600 + 100 + (5 * 60)
    assert y == 100 + (5 * 60)
