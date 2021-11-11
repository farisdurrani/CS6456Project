import pygame
from SpaceshipDir import Spaceship
from EvilSpaceshipDir import EvilShip
from ConstantVars import Colors, Constants
import MouseInstance


class Main:
    def __init__(self):
        screen = self.initiate_game()
        self.run_game(screen)
        self.spaceship = None
        self.evil_ship = None

    def initiate_game(self):
        pygame.init()
        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                         Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")
        self.spaceship = Spaceship.Spaceship(screen)
        self.evil_ship = EvilShip.EvilShip()
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
            mouse_instance = MouseInstance.MouseInstance()

            # pygame.draw.rect(screen, Colors.WHITE, (ConstantVars.CENTER_X, ConstantVars.CENTER_Y, 2, 2))
            self.spaceship.update_spaceship(screen, mouse_instance)
            self.evil_ship.update_evil_ship(screen, mouse_instance)
            for evil_bullet in self.evil_ship.bullets:
                self.spaceship.analyze_hit(evil_bullet.get_coord(),
                                           evil_bullet.get_damage())
            # pygame.draw.rect(screen, Colors.WHITE,
            #                  (center[0], center[1], 2, 2))

            pygame.display.update()
            clock.tick(Constants.FPS)

        pygame.quit()


def main():
    Main()


if __name__ == "__main__":
    main()
