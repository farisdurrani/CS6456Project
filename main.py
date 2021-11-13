import pygame
import random
from ship.SpaceshipDir import Spaceship
from ship.EvilSpaceshipDir import EvilShip
from ConstantVars import Colors, Constants, GenFunctions
import MouseInstance
from nine_sq_recognizer import NineSquareRecognizer


class Main:
    def __init__(self):
        self.spaceship = None
        self.all_ships = []
        self.bullets = []
        self.finger_x_array = []
        self.finger_y_array = []
        self.finger_id = set()
        self.game_is_paused = False

        screen = self.initiate_game()
        self.run_game(screen)

    def initiate_game(self):
        pygame.init()
        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                          Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")

        self.spaceship = Spaceship.Spaceship()
        self.all_ships.append(self.spaceship)

        for _ in range(random.randint(1, 10)):
            evil_ship = EvilShip.EvilShip()
            self.all_ships.append(evil_ship)
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

        ships_to_remove = set()
        for ship_i, ship in enumerate(self.all_ships):
            ship.update_ship(screen, mouse_instance, self)
            if ship.out_of_range:
                ships_to_remove.add(ship_i)
        for ship_to_remove in ships_to_remove:
            self.all_ships.pop(ship_to_remove)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.FINGERDOWN:
                # Citation: https://www.patreon.com/posts/
                # finger-painting-43786073?l=fr
                self.finger_id.add(event.finger_id)
            elif event.type == pygame.FINGERMOTION:
                if len(self.finger_id) == 1:
                    self.finger_x_array.append(event.x)
                    self.finger_y_array.append(event.y)
                if len(self.finger_id) == 4:
                    print(1111)
            elif event.type == pygame.FINGERUP:
                if len(self.finger_id) == 1:
                    drawing_candidate = \
                        NineSquareRecognizer(self.finger_x_array,
                                             self.finger_y_array) \
                            .get_template_answer()
                    print(drawing_candidate)
                    if drawing_candidate == ">":
                        self.pause_game()
                    elif drawing_candidate == "O":
                        self.spaceship.add_shield()
                self.finger_x_array.clear()
                self.finger_y_array.clear()
                self.finger_id.clear()
        return run

    def pause_game(self):
        print("GAME IS PAUSED")
        self.game_is_paused = True
        for ship in self.all_ships:
            ship.pause_ship()

    def resume_game(self):
        self.game_is_paused = False
        for ship in self.all_ships:
            ship.resume_ship()


def main():
    Main()


if __name__ == "__main__":
    main()
