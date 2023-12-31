def print_boards_to_console(board1, board2):
    print("top - was shot, down - ship position")

    for row in range(10):
        print()
        for column in range(10):
            if board1[row, column].was_shot:
                print("x", end=" ")
            else:
                print(".", end=" ")

        print(10 * " ", end=" ")
        for column in range(10):
            if board2[row, column].was_shot:
                print("x", end=" ")
            else:
                print(".", end=" ")
    print()
    for row in range(10):
        print()
        for column in range(10):
            if not board1[row, column].is_free:
                print("s", end=" ")
            else:
                print(".", end=" ")

        print(10 * " ", end=" ")
        for column in range(10):
            if not board2[row, column].is_free:
                print("s", end=" ")
            else:
                print(".", end=" ")
    print()
