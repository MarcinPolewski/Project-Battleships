""" memory access layer of programm"""
import pygame
import constants


class AssetLoader:
    """loads all assets"""

    def __init__(self):
        # loading see images
        self.see_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/see/background{i}.png")
            self.see_images.append(temp)

        # loading table image
        self.table_image = pygame.image.load("assets/table/table.png")

        # loading backround for game result
        self.game_result_background = pygame.image.load(
            "assets/Game_result_backround.png"
        )

        # loading logo image
        self.logo_background = pygame.image.load("assets/Logo.png")

        # load status bar background
        self.status_bar_background = pygame.image.load("assets/StatusBar.png")

        # load small ship icon
        self.small_ship_icon = pygame.image.load("assets/ships/SmallShipIcon.png")

        # loading cloud images
        self.cloud_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/clouds/Cloud{i}.png")
            self.cloud_images.append(temp)

        # loading ship images
        self.ship_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/ships/Ship{i}.png")
            self.ship_images.append(temp)

        # loading button images
        self.button_image = pygame.image.load("assets/Button.png")

        # loading fonts
        self.pixel_font_for_buttons = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.BUTTON_TEXT_SIZE
        )
        self.pixel_font_for_logo = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.LOGO_TEXT_SIZE
        )
        self.pixel_font_for_status_bar = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.STATUS_BAR_FONT_SIZE
        )
        self.pixel_font_for_message_to_switch = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf",
            constants.MESSAGE_TO_SWITCH_FONT_SIZE,
        )
        self.pixel_font_for_prompt = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.PROMPT_TEXT_SIZE
        )
        self.pixel_font_for_statistics = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.STATISTICS_TEXT_SIZE
        )
        self.pixel_font_for_winner = pygame.font.Font(
            "assets/fonts/PixelifySans-Regular.ttf", constants.WINNER_TEXT_SIZE
        )
