import pygame


def get_text_image(text, text_size, text_color):
    """returns image with text provided text"""
    text_font = pygame.font.SysFont("Arial", text_size)

    image = text_font.render(text, True, text_color)

    return image


def calculate_positioning_in_the_middle_of_image(
    image_height, image_width, text_height, text_width
):
    # @TODO handle situation where x or y is negative
    y = (image_height - text_height) // 2
    x = (image_width - text_width) // 2

    return (x, y)


def calculate_text_position_for_logo(
    image_height, image_width, text_height, text_width
):
    """logo image is divided horizonatally to 2 equal rectangles,
    where lower on is ship image and top one is text"""
    # @TODO handle situation where x or y is negative
    y = ((image_height) // 2 - text_height) // 2
    x = (image_width - text_width) // 2
    return (x, y)
