import pygame


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

    def __init__(self, position, height, width, image):
        self._position = position
        self._height = height
        self._width = width
        self._image = image

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


class PlayPVPButton(Button):
    def __init__(self, position):
        # loading button image
        image = pygame.image.load("assets/Button.png")
        # calculating dimensions from image
        height = self._image.get_height()
        width = self._image.get_width()
        super().__init__(position=position, height=height, width=width, image=image)


# class PlayPVCButton(Button):
#     pass


# class ExitButton(Button):
#     pass


# class ReplayButton(Button):
#     pass
