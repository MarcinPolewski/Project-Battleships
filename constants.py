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
    "Cruiser": CRUISER_LENGTH,
    "PatrolShip": PATROL_SHIP_LENGTH,
}

# ship orientations
SHIP_HORIZONTAL = 1
SHIP_VERTICAL = 2

# game configurations
STANDARD_SHIP_QUANTITIES = {
    "Carrier": 1,
    # "Battleship": 1,
    # "Cruiser": 4,
    # "PatrolShip": 3,
}

# table configurations
BOARD_CELL_SIZE = 10  # how many cells in a row or a column

# game phases
GAME_START_SCREEN = 3
POSITIONING_PHASE = 10
GAME_PHASE = 5
READY_TO_SWITCH_PHASE = 40
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
TABLE_VERTICAL_OFFSET = 150
TABLE_SIZE = 600  # board is  600px x 600px
CELL_SIZE = 60  # each cell of table is 60px x 60px

FPS = 60

# button id-s
PLAY_AGAIN_BUTTON = 5
QUIT_BUTTON = 10
PVP_BUTTON = 15
PVC_BUTTON = 20

# background animation cooldown (ms)
BACKGROUND_COOLDOWN = 900
BOARD_ANIMATION_COOLDOWN = 900


BUTTON_WIDTH = 400
# button positions
# @TODO - do dynamically ?
PVP_BUTTON_POSITION = (600, 450)
PVC_BUTTON_POSITION = (600, 575)
START_SCREEN_EXIT_BUTTON_POSITION = (600, 700)


END_SCREEN_EXIT_BUTTON_POSITION = ((SCREEN_WIDTH) // 2 - BUTTON_WIDTH - 25, 625)
REPLAY_BUTTON_POSITION = ((SCREEN_WIDTH) // 2 + 25, 625)

SWITCH_USER_BUTTON_POSITION = (600, 775)

LOGO_POSITION = (500, 100)

GAME_RESULT_BUTTONS_HORIZONTAL_OFFSET = 50


# button text settings
BUTTON_TEXT_SIZE = 40
BUTTON_TEXT_COLOR = (0, 0, 0)
LOGO_TEXT_SIZE = 80
MESSAGE_TO_SWITCH_FONT_SIZE = 40

PROMPT_TEXT_SIZE = 50
PROMPT_COLOR = (255, 0, 0)
PROMPT_COOLDOWN = 30

# Positioning on screen bar
FLEET_STATUS_VERTICAL_OFFSET = 50
SMALL_SHIP_ICON_SIZE = 24  # in pixels

STATUS_BAR_FONT_SIZE = 20
STATUS_BAR_TEXT_COLOR = (0, 0, 0)
PLAYER_NAME_VERTICAL_OFFSET = 10

# statistics
STATISTICS_TEXT_SIZE = 30
STATISTICS_TEXT_COLOR = (255, 255, 255)
STATISTICS_HORIZONTAL_OFFSET = 20
STATISTICS_VERTICAL_OFFSET = 20
WINNER_TEXT_COLOR = 30
WINNER_TEXT_SIZE = 80
WINNER_VERTICAL_OFFSET = 50
STATISTIC_SPACING = 10
