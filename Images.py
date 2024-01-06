import constants
from copy import copy


class ImageHandler:
    """class provided simple functionality for using images(generating from text
    calulating right position), move complex operations on images are done outside"""

    def __init__(self, asset_loader, game_controller):
        # loading images from memory
        self._assets = asset_loader
        self._game_controller = game_controller

        self._blackscreen_prompt = None
        self._logo_image = None

    @property
    def see_images(self):
        return copy(self._assets.see_images)

    @property
    def table_image(self):
        return copy(self._assets.table_image)

    @property
    def game_result_background(self):
        return copy(self._assets.game_result_background)

    @property
    def logo_background(self):
        return copy(self._assets.logo_background)

    @property
    def small_ship_icon(self):
        return copy(self._assets.small_ship_icon)

    @property
    def cloud_images(self):
        return copy(self._assets.cloud_images)

    @property
    def ship_images(self):
        return copy(self._assets.ship_images)

    @property
    def status_bar_background(self):
        return copy(self._assets.status_bar_background)

    @property
    def logo_image(self):
        """returns game logo image (generates on if needed)"""
        if self._logo_image is None:
            self._logo_image = self.generate_logo_image()
        return copy(self._logo_image)

    @property
    def blackscreen_prompt(self):
        """retruns blackscreen prompt image (generates one if needed)"""
        if self._blackscreen_prompt is None:
            self._blackscreen_prompt = self.generate_blackscreen_prompt
        return copy(self.generate_blackscreen_prompt())

    # @TODO handle situation where x or y is negative
    def calculate_x_to_fit_in_the_middle(self, outer_image, inner_image):
        return (outer_image.get_width() - inner_image.get_width()) // 2

    def calculate_y_to_fit_in_the_middle(self, outer_image, inner_image):
        return (outer_image.get_height() - inner_image.get_height()) // 2

    def calculate_x_and_y_to_centre_in_image(self, outer_image, inner_image):
        """returns position where to position inner image in outer image to
        make it centre"""
        x = (outer_image.get_width() - inner_image.get_width()) // 2
        y = (outer_image.get_height() - inner_image.get_height()) // 2
        return (x, y)

    def calculate_x_and_y_to_centre_on_screen(self, image):
        pass
        x = (constants.SCREEN_WIDTH - image.get_width()) // 2
        y = (constants.SCREEN_HEIGHT - image.get_height()) // 2
        return (x, y)

    def calculate_position_for_top_half_of_image(self, outer_image, inner_image):
        """logo image is divided horizonatally to 2 equal rectangles,
        where lower on is ship image and top one is text"""
        y = ((outer_image.get_height()) // 2 - inner_image.get_height()) // 2
        x = (outer_image.get_width() - inner_image.get_width()) // 2
        return (x, y)

    def get_image_from_text(self, text, font, text_color):
        """returns pygame.image created from text"""
        return font.render(text, True, text_color)

    def get_button_image(self, button_text):
        """returns right button image with button_text"""
        image = copy(self._assets.button_image)
        text_image = self.get_image_from_text(
            button_text,
            self._assets.pixel_font_for_buttons,
            text_color=constants.BUTTON_TEXT_COLOR,
        )
        position = self.calculate_x_and_y_to_centre_in_image(image, text_image)
        image.blit(text_image, position)

        return image

    def get_winner_image(self):
        winner = self._game_controller.winner_name + " has won!!!"
        winner_image = self.get_image_from_text(
            text=winner,
            font=self._assets.pixel_font_for_winner,
            text_color=constants.WINNER_TEXT_COLOR,
        )
        return winner_image

    def get_statistic_image_from_text(self, text):
        return self.get_image_from_text(
            text=text,
            font=self._assets.pixel_font_for_statistics,
            text_color=constants.STATISTICS_TEXT_COLOR,
        )

    def get_status_bar_image_from_text(self, text):
        return self.get_image_from_text(
            text=text,
            font=self._assets.pixel_font_for_status_bar,
            text_color=constants.STATISTICS_TEXT_COLOR,
        )

    def get_prompt_image(self, text):
        font = self._assets.pixel_font_for_prompt
        return self.get_image_from_text(
            text=text, font=font, text_color=constants.PROMPT_COLOR
        )

    def generate_logo_image(self):
        image = self._assets.logo_background
        text = "Battleship"
        font = self._assets.pixel_font_for_logo
        text_image = self.get_image_from_text(text, font, constants.LOGO_TEXT_COLOR)
        position = self.calculate_position_for_top_half_of_image(image, text_image)
        image.blit(text_image, position)

        return image

    def generate_blackscreen_prompt(self):
        return self.get_image_from_text(
            text=constants.MESSAGE_TO_SWITCH,
            font=self._assets.pixel_font_for_message_to_switch,
            text_color=constants.MESSAGE_TO_SWITCH_COLOR,
        )
