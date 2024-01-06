import pygame

# modules created for this project
from MemoryAccess import AssetLoader
from GameLogicController import GameLogicController
from Images import ImageHandler
from UserInterface import (
    GameBoardVisualizer,
    PromptVisualizer,
    ScreenVisualizer,
    StatusBarVisualizer,
    InputHandler,
)
from Buttons import ButtonHandler
import constants


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # configurating screen
    game_screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Battleships")

    # initializing controllers
    game_controller = GameLogicController()
    asset_loader = AssetLoader()
    image_handler = ImageHandler(
        asset_loader=asset_loader, game_controller=game_controller
    )
    game_board_visualizer = GameBoardVisualizer(
        screen=game_screen, game_controller=game_controller, image_handler=image_handler
    )
    screen_visualizer = ScreenVisualizer(
        screen=game_screen, game_controller=game_controller, image_handler=image_handler
    )
    button_handler = ButtonHandler(
        screen=game_screen, game_controller=game_controller, image_handler=image_handler
    )
    prompt_visualizer = PromptVisualizer(
        screen=game_screen, game_controller=game_controller, image_handler=image_handler
    )
    status_bar_visualizer = StatusBarVisualizer(
        screen=game_screen, game_controller=game_controller, image_handler=image_handler
    )
    input_handler = InputHandler(
        game_controller=game_controller, button_handler=button_handler
    )

    # main game loop, checks for event
    while game_controller.game_is_running:
        # setting frames per second
        clock.tick(constants.FPS)

        # UPDATE ELEMENTS
        screen_visualizer.update()
        game_board_visualizer.update()
        button_handler.update()
        prompt_visualizer.update()
        status_bar_visualizer.update()

        # DRAW ELEMENTS
        screen_visualizer.draw()
        game_board_visualizer.draw()
        button_handler.draw()
        prompt_visualizer.draw()
        status_bar_visualizer.draw()

        pygame.display.update()

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_controller.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_handler.mouse_button_interaction(
                    mouse_position=pygame.mouse.get_pos(), is_pressed=True
                )
            if event.type == pygame.MOUSEBUTTONUP:
                input_handler.mouse_button_interaction(
                    mouse_position=pygame.mouse.get_pos(), is_pressed=False
                )
    pygame.quit()


if __name__ == "__main__":
    main()
