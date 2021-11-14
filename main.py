import time

import pygame
import random
from ship.spaceship import Spaceship
from ship.evil_ship import EvilShip
from ship.friend_ship import friend_ship
from ConstantVars import Colors, Constants
import MouseInstance
from nine_sq_recognizer import NineSquareRecognizer
from AltScreens.request_support import RequestSupport
import cv2
from Utilities.gaze_tracking import GazeTracking


class Main:
    def __init__(self):
        self.run = True

        self.spaceship = None
        self.all_ships = []
        self.bullets = []
        self.finger_x_array = []
        self.finger_y_array = []
        self.finger_id = set()
        self.game_is_paused = False
        self.req_support = None
        self.MINIMUM_SHIPS = 5

        self.webcam = None
        self.gaze = None
        self.scaled_pupil_right_coords = [0, 0]  # based on min and max recorded
        self.min_pupil_right_coords = [10000, 10000]
        self.max_pupil_right_coords = [0, 0]
        # when min and max pupil coords are no longer equal
        self.able_to_scale = False

        screen = self.initiate_game()
        self.run_game(screen)

    def initiate_game(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        pygame.init()
        Constants.initiate_constants(pygame)

        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                          Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")

        # make ships
        self.spaceship = Spaceship.Spaceship()
        self.all_ships.append(self.spaceship)
        for _ in range(random.randint(3, 10)):
            evil_ship = EvilShip.EvilShip()
            self.all_ships.append(evil_ship)

        return screen

    def run_game(self, screen):
        clock = pygame.time.Clock()
        self.run = True

        while self.run:
            pygame.time.delay(100)

            self.collect_eye_data()
            self.update_components(screen)

            pygame.display.update()
            clock.tick(Constants.FPS)

        self.exit_game()

    def collect_eye_data(self):
        _, frame = self.webcam.read()
        self.gaze.refresh(frame)

        new_frame = self.gaze.annotated_frame()
        text = ""

        if self.gaze.is_right():
            text = "Looking right"
        elif self.gaze.is_left():
            text = "Looking left"
        elif self.gaze.is_center():
            text = "Looking center"

        # calculating eye position scaled
        # as we have more data, the scale gets better
        coord = self.gaze.pupil_right_coords()
        if coord is not None:
            self.min_pupil_right_coords = [
                min(self.min_pupil_right_coords[0], coord[0]),
                min(self.min_pupil_right_coords[1], coord[1])
            ]
            self.max_pupil_right_coords = [
                max(self.max_pupil_right_coords[0], coord[0]),
                max(self.max_pupil_right_coords[1], coord[1])
            ]
            if not self.able_to_scale:
                if self.min_pupil_right_coords[0] \
                        != self.max_pupil_right_coords[0] \
                        and self.min_pupil_right_coords[1] \
                        != self.max_pupil_right_coords[1]:
                    self.able_to_scale = True
            else:
                x_scaled = (coord[0] - self.min_pupil_right_coords[0]) / \
                           (self.max_pupil_right_coords[0]
                            - self.min_pupil_right_coords[0]) \
                           * Constants.WINDOW_WIDTH
                y_scaled = (coord[1] - self.min_pupil_right_coords[1]) / \
                           (self.max_pupil_right_coords[1]
                            - self.min_pupil_right_coords[1]) \
                           * Constants.WINDOW_HEIGHT
                self.scaled_pupil_right_coords = [x_scaled, y_scaled]

        if self.gaze.is_blinking():
            print(f'True {time.time()}')

        cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2,
                    (255, 0, 0), 2)
        cv2.imshow("Eye Tracker", new_frame)

        # if Esc or 'X' close key clicked
        if cv2.waitKey(1) == 27 \
                or cv2.getWindowProperty("Eye Tracker",
                                         cv2.WND_PROP_VISIBLE) == 0:
            self.run = False

    def update_components(self, screen):
        for event in pygame.event.get():
            # reset screen
            screen.fill(Colors.BLACK)

            # update ships and bullets
            self.update_ships_and_bullets(screen)

            # check for any inputs
            if event.type == pygame.QUIT:
                self.run = False
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
                            self.request_support()
                        elif drawing_candidate == "O":
                            self.spaceship.add_shield()
                    self.finger_x_array.clear()
                    self.finger_y_array.clear()
                    self.finger_id.clear()

            # update request support screen
            if self.game_is_paused:
                friends_requested = self.req_support.update_gui(screen, event)
                if friends_requested is not None:
                    self.add_allies(friends_requested)
                    self.resume_game()

        screen.fill(Colors.BLACK)
        self.update_ships_and_bullets(screen)
        if self.game_is_paused and self.req_support is not None:
            self.req_support.update_gui(screen, None)

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

    def add_allies(self, friends_requested):
        for friend in friends_requested:
            self.all_ships.append(friend_ship.FriendShip(friend))

    def request_support(self):
        self.req_support = RequestSupport()
        self.pause_game()

    def update_ships_and_bullets(self, screen):
        mouse_instance = MouseInstance.MouseInstance(
            self.scaled_pupil_right_coords)
        ships_to_remove = set()
        for ship_i, ship in enumerate(self.all_ships):
            ship.update_ship(screen, mouse_instance, self)
            if ship.out_of_range:
                ships_to_remove.add(ship_i)

        # remove ships out of range
        for ship_to_remove in ships_to_remove:
            try:
                self.all_ships.pop(ship_to_remove)
            except IndexError:
                print(ship_to_remove)
        ships_to_remove.clear()

        if len(self.all_ships) < self.MINIMUM_SHIPS:
            self.all_ships.append(EvilShip.EvilShip())

    def exit_game(self):
        print("EXITING...")
        pygame.quit()
        self.webcam.release()
        cv2.destroyAllWindows()


def main():
    Main()


if __name__ == "__main__":
    main()
