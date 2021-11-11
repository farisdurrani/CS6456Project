import pygame
import MouseInstance
from Constants import Constants, Colors, GeneralFunctions
import math


class EvilShip:
    def __init__(self):
        self.velocity = Constants.EVIL_SHIPS_VELOCITY
        self.health = 100
        self.top_left = [Constants.CENTER_X, Constants.CENTER_Y]
        raw_spaceship_image = pygame.image.load(
            r'EvilSpaceshipDir\\evil_ship_icon.png')
        self.EVIL_SHIP_HEIGHT = 50
        self.EVIL_SHIP_WIDTH = 50
        self.scaled_spaceship_image = pygame.transform.scale(raw_spaceship_image,
                                                      (self.EVIL_SHIP_WIDTH,
                                                       self.EVIL_SHIP_HEIGHT))
        self.rotated_image = self.scaled_spaceship_image
        self.out_of_range = False

    def update_evil_ship(self, screen, mouse_instance: MouseInstance):
        self.update_rotation()
        self.update_coords(mouse_instance)
        screen.blit(self.rotated_image, self.top_left)
        return self.get_center()

    def update_rotation(self):
        center = self.get_center()
        y_delta_from_center = center[1] - Constants.CENTER_Y
        x_delta_from_center = center[0] - Constants.CENTER_X
        # print(center)
        try:
            base_angle_from_center = math.degrees(
                math.atan(abs(y_delta_from_center) / abs(x_delta_from_center)))
        except ZeroDivisionError:
            return
        quadrant = self.get_quadrant(x_delta_from_center, y_delta_from_center)
        angle_rotation = 0
        if quadrant == 1:
            angle_rotation = 90 + base_angle_from_center
        elif quadrant == 2:
            angle_rotation = 270 - base_angle_from_center
        elif quadrant == 3:
            angle_rotation = 270 + base_angle_from_center
        elif quadrant == 4:
            angle_rotation = 90 - base_angle_from_center
        self.rotated_image = pygame.transform. \
            rotate(self.scaled_spaceship_image, angle_rotation)

    def update_coords(self, mouse_instance: MouseInstance):
        if mouse_instance.quadrant == 1:
            self.top_left[0] = self.top_left[0] \
                               - mouse_instance.unit_x_velocity * self.velocity
            self.top_left[1] = self.top_left[1] \
                               + mouse_instance.unit_y_velocity * self.velocity
        elif mouse_instance.quadrant == 2:
            self.top_left[0] = self.top_left[0] \
                               + mouse_instance.unit_x_velocity * self.velocity
            self.top_left[1] = self.top_left[1] \
                               + mouse_instance.unit_y_velocity * self.velocity
        elif mouse_instance.quadrant == 3:
            self.top_left[0] = self.top_left[0] \
                               + mouse_instance.unit_x_velocity * self.velocity
            self.top_left[1] = self.top_left[1] \
                               - mouse_instance.unit_y_velocity * self.velocity
        elif mouse_instance.quadrant == 4:
            self.top_left[0] = self.top_left[0] \
                               - mouse_instance.unit_x_velocity * self.velocity
            self.top_left[1] = self.top_left[1] \
                               - mouse_instance.unit_y_velocity * self.velocity

        if GeneralFunctions.out_of_range(self.top_left[0], self.top_left[1]):
            self.out_of_range = True

    def fire_bullets(self):
        pass

    def get_quadrant(self, x_delta, y_delta):
        # print(x_delta)
        # print(y_delta)
        if x_delta >= 0 and y_delta < 0:
            return 1
        elif x_delta < 0 and y_delta < 0:
            return 2
        elif x_delta < 0 and y_delta >= 0:
            return 3
        elif x_delta >= 0 and y_delta >= 0:
            return 4
        else:
            return None

    def get_center(self) -> list:
        return [
            int(self.top_left[0] + self.EVIL_SHIP_WIDTH / 2),
            int(self.top_left[1] + self.EVIL_SHIP_HEIGHT / 2)
        ]


class EvilSpaceshipBullet:
    def __init__(self, mouse_instance: MouseInstance,
                 ship_center: tuple = (Constants.CENTER_X, Constants.CENTER_Y)):
        self.velocity = 10
        self.coord = [ship_center[0], ship_center[1]]
        self.mouse_instance = mouse_instance
        self.x_velocity = int(self.velocity
                              * self.mouse_instance.unit_x_velocity)
        self.y_velocity = int(self.velocity
                              * self.mouse_instance.unit_y_velocity)
        self.out_of_range = False

    def update_screen_pos(self, screen):
        self.update_coord()
        pygame.draw.rect(screen, Colors.RED,
                         pygame.Rect(self.coord[0], self.coord[1],
                                     Constants.BULLET_WIDTH,
                                     Constants.BULLET_WIDTH))

    def update_coord(self):
        if self.mouse_instance.quadrant == 1:
            self.coord[0] = self.coord[0] + self.x_velocity
            self.coord[1] = self.coord[1] - self.y_velocity
        elif self.mouse_instance.quadrant == 2:
            self.coord[0] = self.coord[0] - self.x_velocity
            self.coord[1] = self.coord[1] - self.y_velocity
        elif self.mouse_instance.quadrant == 3:
            self.coord[0] = self.coord[0] - self.x_velocity
            self.coord[1] = self.coord[1] + self.y_velocity
        elif self.mouse_instance.quadrant == 4:
            self.coord[0] = self.coord[0] + self.x_velocity
            self.coord[1] = self.coord[1] + self.y_velocity

        if GeneralFunctions.out_of_range(self.coord[0], self.coord[1]):
            self.out_of_range = True


