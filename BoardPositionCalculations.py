""" provides functions translating row and column to
x,y coordinates on screen(or the other way around)"""
import constants
from GameErrors import OutOfTableError


def verify_row_and_column(row, column):
    """raises error when invalid row or column is provided"""
    if (
        row < 0
        or column < 0
        or column > constants.BOARD_CELL_SIZE - 1
        or row > constants.BOARD_CELL_SIZE - 1
    ):
        raise OutOfTableError(row, column)


def calculate_x_y_cooridantes(row, column, from_left_table=True):
    """converts row and column to (x,y) coordinates of top left
    corner of cell on screen, raises OutOfTableError is row or
    column doesn't exist in table

    if from_left_table is True, returns result for left table,
    otherwise for right table"""

    verify_row_and_column(row, column)

    y = constants.TABLE_VERTICAL_OFFSET + row * constants.CELL_SIZE
    x = constants.TABLE_HORIZONTAL_OFFSET + column * constants.CELL_SIZE

    if not from_left_table:
        distance_from_left_edge = (
            constants.SCREEN_WIDTH
            - (2 * constants.TABLE_HORIZONTAL_OFFSET)
            - constants.TABLE_SIZE
        )
        x += distance_from_left_edge
    return (x, y)


def calculate_row_and_column(coordinates, from_left_table=True):
    """
    returns (row, column) converted from coordinate system
    from pygame
    only right and bottom edges belong to particaulr cell(
    to achieve that, we subtract 1 while calculating rows/columns)
    if from_left_table is True, returns result for left table,
    otherwise for right table
    """
    column = None
    row = None
    coordinate_x, cooridnate_y = coordinates
    if from_left_table:
        column = (
            coordinate_x - constants.TABLE_HORIZONTAL_OFFSET - 1
        ) // constants.CELL_SIZE
    else:  # calculating for right table
        # distance between table and left edge(only x value)
        distance_from_left_edge = (
            constants.SCREEN_WIDTH
            - constants.TABLE_HORIZONTAL_OFFSET
            - constants.TABLE_SIZE
        )
        column = (coordinate_x - distance_from_left_edge - 1) // constants.CELL_SIZE

    row = (cooridnate_y - constants.TABLE_VERTICAL_OFFSET - 1) // constants.CELL_SIZE

    verify_row_and_column(row, column)

    return (row, column)
