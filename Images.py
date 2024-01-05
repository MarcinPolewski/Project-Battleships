import pygame




class ImageLoader:
    """loads images from memory"""

    def __init__(self):
        # loading see images
        self.see_images = []
        for i in range(1, 6):
            temp = pygame.image.load(f"assets/see/background{i}.png")
            self.see_images.append(temp)

        # loading table image
        self.table_image = pygame.image.load("assets/table/table.png")

        # loading backround for game result
        self.game_result_backgrounds = pygame.image.load(
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


class ImageHandler:
    def __init__(self):
        # loading images from memory
        self._images = ImageLoader()

        self._logo_image = None

    @property
    def images(self):
        """returns ImageLoader class containging all loaded images"""
        return self._images

    @property
    def logo_image(self):
        if self._logo_image is None:
            self._logo_image = self.generate_logo_image()
        return self._logo_image

    @property 
    def game_result_screen(self):
        

    def generate_logo_image(self): 
        pass #@TODO 

    def generate_game_result_screen(self):
        pass #@TODO
    

def get_text_image(text, text_size, text_color):
    """returns image with text provided text"""
    # text_font = pygame.font.SysFont("Arial", text_size)
    text_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", text_size)
    image = text_font.render(text, True, text_color)

    return image