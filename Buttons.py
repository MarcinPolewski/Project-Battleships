import pygame
import constants


class Button:
    """base class for more specific buttons

    :param _position: (x,y) coordinates of top left corner
    :type _position: tuple(int, int)
    :param _hegiht: height of button in pixels
    :type _height: int
    :param _width: witdh of button in pixels
    :type _width: int
    :param _image: image displayed as button
    :type _image: pygame.image
    :param _is_displayed: True if button is displayed on board
    :type _is_displayed: bool
    """

    def __init__(self, position, screen, image):
        self._position = position
        self._height = image.get_height()
        self._width = image.get_width()
        self._image = image
        self._screen = screen

        self._is_visible = False

    def is_visible(self):
        """returns true if button is displayed on screen"""
        return self._is_visible

    def check_if_mouse_on_button(self, mouse_position):
        """checks if mouse was on button"""
        mouse_x, mouse_y = mouse_position
        image_x, image_y = self._position  # position of top left corner

        if (
            image_x <= mouse_x
            and mouse_x <= image_x + self._width
            and image_y <= mouse_y
            and mouse_y <= image_y + self._height
        ):
            return True
        return False

    def make_visible(self):
        self._is_visible = True

    def remove_from_screen(self):
        self._is_visible = False

    def was_pressed(self, mouse_position):
        """returns True if button was pressed"""
        if self.is_visible and self.check_if_mouse_on_button(mouse_position):
            return True
        return False

    def draw(self):
        """draws button on the screen"""
        self._screen.blit(self._image, self._position)


class ButtonHandler:
    """displays buttons on screen and checks if they have been pressed"""

    def __init__(self, screen, game_controller):
        self._screen = screen
        self._game_controller = game_controller

        # initialsing buttons for start screen
        self._start_buttons = [
            PlayPVPButton(screen=screen),
            PlayPVCButton(screen=screen),
            ExitStartScreenButton(screen=screen),
        ]
        # initialising buttons for end game screen
        self._end_buttons = [
            ReplayButton(screen=screen),
            ExitEndScreenButton(screen=screen),
        ]

        self._buttons_to_draw = []

    @property
    def phase(self):
        """returns current game phase"""
        return self._game_controller.phase

    def check_button_press(self, mouse_press_position, mouse_release_position):
        """if button was pressed returns corresponding button
        else return None"""
        # button was pressed if it's displayed and mouse was pressed and released on it

        for button in self._buttons_to_draw:
            if button.check_if_mouse_on_button(
                mouse_press_position
            ) and button.check_if_mouse_on_button(mouse_release_position):
                return button

        return None

    def update(self):
        """sets visibility of buttons according to
        current phase"""
        if self.phase == constants.GAME_START_SCREEN:
            self._buttons_to_draw = self._start_buttons
        elif self.phase == constants.GAME_RESULT_PHASE:
            self._buttons_to_draw = self._end_buttons
        else:
            self._buttons_to_draw = []

    def draw(self):
        """draws right buttons on screen"""
        if not self._buttons_to_draw:
            return

        for button in self._buttons_to_draw:
            button.draw()


class PlayPVPButton(Button):
    def __init__(self, screen):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        position = constants.PVP_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class PlayPVCButton(Button):
    def __init__(self, screen):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        position = constants.PVC_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ExitStartScreenButton(Button):
    def __init__(self, screen):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        position = constants.START_SCREEN_EXIT_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ExitEndScreenButton(Button):
    def __init__(self, screen):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        position = constants.END_SCREEN_EXIT_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ReplayButton(Button):
    def __init__(self, screen):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        position = constants.REPLAY_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)
