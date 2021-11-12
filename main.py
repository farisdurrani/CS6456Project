import pygame
from ship.SpaceshipDir import Spaceship
from ship.EvilSpaceshipDir import EvilShip
from ConstantVars import Colors, Constants, GenFunctions
import MouseInstance
from dollar_recognizer import DollarRecognizer


class Main:
    def __init__(self):
        self.spaceship = None
        self.evil_ship = None
        self.all_ships = None
        self.bullets = []
        self.finger_x_array = []
        self.finger_y_array = []
        self.finger_id = set()

        screen = self.initiate_game()
        self.run_game(screen)

    def initiate_game(self):
        pygame.init()
        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                          Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")
        self.spaceship = Spaceship.Spaceship()
        self.evil_ship = EvilShip.EvilShip()
        self.all_ships = [self.spaceship, self.evil_ship]
        return screen

    def run_game(self, screen):
        clock = pygame.time.Clock()
        run = True

        while run:
            pygame.time.delay(100)

            screen.fill(Colors.BLACK)
            mouse_instance = MouseInstance.MouseInstance()

            run = self.update_components(screen, mouse_instance)

            pygame.display.update()
            clock.tick(Constants.FPS)

        pygame.quit()

    def update_components(self, screen, mouse_instance):
        run = True
        self.spaceship.update_ship(screen, mouse_instance, self)
        self.evil_ship.update_ship(screen, mouse_instance, self)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # elif event.type == pygame.FINGERDOWN:
            #     # Citation: https://www.patreon.com/posts/
            #     # finger-painting-43786073?l=fr
            #     self.finger_id.add(event.finger_id)
            # elif event.type == pygame.FINGERMOTION:
            #     if len(self.finger_id) == 1:
            #         self.finger_x_array.append(event.x)
            #         self.finger_y_array.append(event.y)
            #     if len(self.finger_id) == 4:
            #         print(1111)
            # elif event.type == pygame.FINGERUP:
            #     if len(self.finger_id) == 1:
            #         drawing_candidate = \
            #             DollarRecognizer(self.finger_x_array,
            #                              self.finger_y_array) \
            #                 .get_template_answer()
            #         if drawing_candidate == "O":
            #             self.spaceship.add_shield()
            #     self.finger_x_array.clear()
            #     self.finger_y_array.clear()
            #     self.finger_id.clear()
        return run


def main():
    Main()


if __name__ == "__main__":
    main()
