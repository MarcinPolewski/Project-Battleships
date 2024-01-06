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
    :type _image: pygame.Surface
    """

    def __init__(self, position, screen, image):
        self._position = position
        self._height = image.get_height()
        self._width = image.get_width()
        self._image = image
        self._screen = screen

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

    def was_pressed(self, mouse_position):
        """returns True if button was pressed"""
        if self.check_if_mouse_on_button(mouse_position):
            return True
        return False

    def draw(self):
        """draws button on the screen"""
        self._screen.blit(self._image, self._position)


class ButtonHandler:
    """displays buttons on screen and checks if they have been pressed

    :param _screen: screen where button will be drawn
    :type _screen: pygame.Surface
    :param _game_controller: used here only for checking game phase
    :type _game_controller: GameLogicController.GameLogicController
    :param _start_buttons: list of button classes to be drawns on start screen
    :type _start_buttons: list
    :param _end_buttons: list of button classes to be drawn during game result phase
    :type _end_buttons: list
    :param _ready_to_switch_button: list of a single button to be drawn to switch users
    :type _ready_to_switch_button: list
    :param _buttons_to_draw: buttons from this list will be drawn when draw() is called
    :type _buttons_to_draw: list

    """

    def __init__(self, screen, game_controller, image_handler):
        self._screen = screen
        self._game_controller = game_controller

        # initialsing buttons for start screen
        self._start_buttons = [
            PlayPVPButton(screen=screen, image_handler=image_handler),
            PlayPVCButton(screen=screen, image_handler=image_handler),
            ExitStartScreenButton(screen=screen, image_handler=image_handler),
        ]
        # initialising buttons for end game screen
        self._end_buttons = [
            ReplayButton(screen=screen, image_handler=image_handler),
            ExitEndScreenButton(screen=screen, image_handler=image_handler),
        ]
        # initialisinng button for switching users
        self._ready_to_switch_button = [
            SwitchUserButton(screen=screen, image_handler=image_handler)
        ]

        self._buttons_to_draw = []

    @property
    def phase(self):
        """returns current game phase"""
        return self._game_controller.phase

    def check_button_press(self, mouse_press_position, mouse_release_position):
        """if button was pressed returns corresponding button
        else return None"""

        # button was pressed if mouse was pressed and released on it
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
        elif self.phase == constants.READY_TO_SWITCH_PHASE:
            self._buttons_to_draw = self._ready_to_switch_button
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
    def __init__(self, screen, image_handler):
        image = image_handler.get_button_image("Play PVP")
        position = constants.PVP_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class PlayPVCButton(Button):
    def __init__(self, screen, image_handler):
        # loading button image
        image = image_handler.get_button_image("Play PVC")
        position = constants.PVC_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ExitStartScreenButton(Button):
    def __init__(self, screen, image_handler):
        # loading button image
        image = image_handler.get_button_image("Exit Game")
        position = constants.START_SCREEN_EXIT_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ExitEndScreenButton(Button):
    def __init__(self, screen, image_handler):
        # loading button image
        image = image_handler.get_button_image("Exit Game")
        position = constants.END_SCREEN_EXIT_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class ReplayButton(Button):
    def __init__(self, screen, image_handler):
        # loading button image
        image = image_handler.get_button_image("Main Menu")
        position = constants.REPLAY_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)


class SwitchUserButton(Button):
    def __init__(self, screen, image_handler):
        image = image_handler.get_button_image("Switch User")
        position = constants.SWITCH_USER_BUTTON_POSITION
        super().__init__(position=position, screen=screen, image=image)
