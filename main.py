import pygame
from Spaceship import update_spaceship
import Colors
import Constants


def initiate_game():
    pygame.init()
    screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT))
    pygame.display.set_caption("Spaceship Battle")
    return screen


def run_game():
    screen = initiate_game()
    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(Colors.BLACK)
        update_spaceship(screen)
        pygame.display.update()
        clock.tick(Constants.FPS)

    pygame.quit()


def main():
    run_game()


if __name__ == "__main__":
    main()