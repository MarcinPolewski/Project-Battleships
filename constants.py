# ship attack status codes
ATTACK_UNSUCCESSFUL = 0
SHIP_HIT = 1
SHIP_SUNK = 2

# ship sizes
CARRIER_LENGTH = 5
BATTLESHIP_LENGTH = 4
CRUISER_LENGTH = 3
PATROL_SHIP_LENGTH = 2
SHIP_LENGTHS = {
    "Carrier": CARRIER_LENGTH,
    "Battleship": BATTLESHIP_LENGTH,
    "Cruiser": CARRIER_LENGTH,
    "PatrolShip": PATROL_SHIP_LENGTH,
}

# ship orientations
SHIP_HORIZONTAL = 1
SHIP_VERTICAL = 2

# game configurations
STANDARD_SHIP_QUANTITIES = {
    "Carrier": 1,
    "Battleship": 1,
    "Cruiser": 4,
    "PatrolShip": 3,
}

# table configurations
BOARD_CELL_SIZE = 10  # how many cells in a row or a column

# game phases
GAME_START_SCREEN = 3
POSITIONING_PHASE = 10
GAME_PHASE = 5
BLACKSCREEN_PHASE = 20
GAME_RESULT_PHASE = 15

# gamemodes
PVP = 10  # player vs player
PVC = 50  # player vs computer
