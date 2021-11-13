import pygame
import random
from ship.spaceship import Spaceship
from ship.evil_ship import EvilShip
from ship.friend_ship import friend_ship
from ConstantVars import Colors, Constants
import MouseInstance
from nine_sq_recognizer import NineSquareRecognizer
from AltScreens.request_support import RequestSupport


class Main:
    def __init__(self):
        self.spaceship = None
        self.all_ships = []
        self.bullets = []
        self.finger_x_array = []
        self.finger_y_array = []
        self.finger_id = set()
        self.game_is_paused = False
        self.req_support = None

        screen = self.initiate_game()
        self.run_game(screen)

    def initiate_game(self):
        pygame.init()
        Constants.initiate_constants(pygame)

        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                          Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")

        # make ships
        self.spaceship = Spaceship.Spaceship()
        self.all_ships.append(self.spaceship)
        for _ in range(random.randint(1, 10)):
            evil_ship = EvilShip.EvilShip()
            ally_ship = friend_ship.FriendShip("Bob")
            self.all_ships.append(evil_ship)
            self.all_ships.append(ally_ship)

        # make request support screen
        self.req_support = RequestSupport()
        return screen

    def run_game(self, screen):
        clock = pygame.time.Clock()
        run = True

        while run:
            pygame.time.delay(100)

            run = self.update_components(screen)

            pygame.display.update()
            clock.tick(Constants.FPS)

        pygame.quit()

    def update_components(self, screen):
        run = True

        for event in pygame.event.get():
            # reset screen
            screen.fill(Colors.BLACK)

            # update ships and bullets
            self.update_ships_and_bullets(screen)

            # check for any inputs
            if event.type == pygame.QUIT:
                run = False
                return run
            elif event.type == pygame.FINGERDOWN:
                # Citation: https://www.patreon.com/posts/
                # finger-painting-43786073?l=fr
                if not self.game_is_paused:
                    self.finger_id.add(event.finger_id)
            elif event.type == pygame.FINGERMOTION:
                if not self.game_is_paused:
                    if len(self.finger_id) == 1:
                        self.finger_x_array.append(event.x)
                        self.finger_y_array.append(event.y)
                    if len(self.finger_id) == 4:
                        print(1111)
            elif event.type == pygame.FINGERUP:
                if not self.game_is_paused:
                    if len(self.finger_id) == 1:
                        drawing_candidate = \
                            NineSquareRecognizer(self.finger_x_array,
                                                 self.finger_y_array) \
                                .get_template_answer()
                        print(f"drawing_candidate = {drawing_candidate}")
                        if drawing_candidate == ">":
                            self.pause_game()
                            self.req_support.reset_friends()
                        elif drawing_candidate == "O":
                            self.spaceship.add_shield()
                    self.finger_x_array.clear()
                    self.finger_y_array.clear()
                    self.finger_id.clear()

            # update request support screen
            if self.game_is_paused:
                self.req_support.update_gui(screen, event)

        screen.fill(Colors.BLACK)
        self.update_ships_and_bullets(screen)
        if self.game_is_paused:
            self.req_support.update_gui(screen, None)

        return run

    def pause_game(self):
        print("GAME IS PAUSED")
        self.game_is_paused = True
        for ship in self.all_ships:
            ship.pause_ship()

    def resume_game(self):
        print("GAME IS RESUMED")
        self.game_is_paused = False
        for ship in self.all_ships:
            ship.resume_ship()

    def update_ships_and_bullets(self, screen):
        mouse_instance = MouseInstance.MouseInstance()
        ships_to_remove = set()
        for ship_i, ship in enumerate(self.all_ships):
            ship.update_ship(screen, mouse_instance, self)
            if ship.out_of_range:
                ships_to_remove.add(ship_i)
        # remove ships out of range
        for ship_to_remove in ships_to_remove:
            self.all_ships.pop(ship_to_remove)


def main():
    Main()


if __name__ == "__main__":
    main()
