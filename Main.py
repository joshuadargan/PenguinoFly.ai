import pygame
from src.Game import Game
from src.Window import Window
from src.Menu import Menu
from src.State import State

if __name__ == '__main__':
    pygame.init()

    window = Window()
    current_state = Menu(window)
    while window.is_open():
        window.fill_base()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or State.is_key_pressed(pygame.K_ESCAPE):
                window.close()
                pygame.quit()

                print("UPDATE: Game window closed")
                break
            state_name = current_state.state
            current_state.keys_pressed_reaction()
            if state_name != current_state.state:
                if current_state.state == State.GAME_STATE or current_state.state == State.RESTART_STATE:
                    # Create new game
                    current_state = Game(window)
                elif current_state.state == State.MENU_STATE:
                    current_state = Menu(window)

        if window.is_open():
            current_state.continuous_action()
            pygame.display.update()
