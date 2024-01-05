import pygame
import constants


def get_text_image(text, text_size, text_color):
    """returns image with text provided text"""
    # text_font = pygame.font.SysFont("Arial", text_size)
    text_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", text_size)
    image = text_font.render(text, True, text_color)

    return image


def calculate_x_in_the_middle_of_image(image_width, text_width):
    x = (image_width - text_width) // 2
    return x


def calculate_y_in_the_middle_of_image(image_height, text_height):
    y = (image_height - text_height) // 2
    return y


def calculate_positioning_in_the_middle_of_image(
    image_height, image_width, text_height, text_width
):
    """returns (x,y) coordinates to positin image, so its exactly
    if the middle of image/screen"""
    # @TODO handle situation where x or y is negative
    x = calculate_x_in_the_middle_of_image(image_width, text_width)
    y = calculate_y_in_the_middle_of_image(image_height, text_height)
    return (x, y)


def calculate_text_position_for_top_half_of_image(
    image_height, image_width, text_height, text_width
):
    """logo image is divided horizonatally to 2 equal rectangles,
    where lower on is ship image and top one is text"""
    # @TODO handle situation where x or y is negative
    y = ((image_height) // 2 - text_height) // 2
    x = (image_width - text_width) // 2
    return (x, y)
