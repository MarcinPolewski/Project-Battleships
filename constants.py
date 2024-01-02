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

# screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# screen positioning
TABLE_HORIZONTAL_OFFSET = 150
TABLE_VERTICAL_OFFSET = 100
TABLE_SIZE = 600  # board is  600pxx600px
CELL_SIZE = 60  # each cell of table is 60px x 60px

FPS = 60

# button id-s
PLAY_AGAIN_BUTTON = 5
QUIT_BUTTON = 10
PVP_BUTTON = 15
PVC_BUTTON = 20

# background animation cooldown (ms)
BACKGROUND_COOLDOWN = 900
CLOUD_COOLDOWN = 900

# button positions
PVP_BUTTON_POSITION = (600, 450)
PVC_BUTTON_POSITION = (600, 575)
START_SCREEN_EXIT_BUTTON_POSITION = (600, 700)

END_SCREEN_EXIT_BUTTON_POSITION = (100, 100)
REPLAY_BUTTON_POSITION = (200, 200)

LOGO_POSITION = (500, 100)

# button text settings
BUTTON_TEXT_SIZE = 40
BUTTON_TEXT_COLOR = (0, 0, 0)
