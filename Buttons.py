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

        self._is_displayed = False

    def check_if_mouse_on_button(self, mouse_position):
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
        pass
        # check if button was visible
        # check if start of click and end are on button


# class EndButton(Button):
#     def __init__(self):
#         # load end button image
#         # getting dimensions from image
#         super().__init__()
