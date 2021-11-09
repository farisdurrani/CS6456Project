import pygame
from Spaceship import Spaceship
import Colors
import Constants


class Main:
    def __init__(self):
        screen = self.initiate_game()
        self.run_game(screen)
        self.spaceship = None

    def initiate_game(self):
        pygame.init()
        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                         Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")
        self.spaceship = Spaceship()
        return screen

    def run_game(self, screen):
        clock = pygame.time.Clock()
        run = True
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            screen.fill(Colors.BLACK)
            self.spaceship.update_spaceship(screen)
            pygame.display.update()
            clock.tick(Constants.FPS)

        pygame.quit()


def main():
    Main()


if __name__ == "__main__":
    main()
