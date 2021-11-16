import pygame
from Utilities import EyeGazeInstance
import math

from ConstantVars import Constants, GenFunctions
from ship import ship_blueprint


class EvilShip(ship_blueprint.Ship):
    def __init__(self):
        # ship characteristics
        SPACESHIP_MAX_HEALTH = 100
        SPACESHIP_HEIGHT = 50
        SPACESHIP_ICON = r'ship\\evil_ship\\evil_ship_icon.png'
        top_left_init = GenFunctions.rand_coord_padded()
        super().__init__(SPACESHIP_MAX_HEALTH, top_left_init, SPACESHIP_HEIGHT,
                         SPACESHIP_ICON)
        self.rotated_image = self.scaled_ship_image
        self.SPEED = 8
        self.BULLET_SPEED = 10
        self.out_of_range = False
        self.health = SPACESHIP_MAX_HEALTH

    def update_ship(self, screen, mouse_instance: EyeGazeInstance, main):
        if not self.ship_paused:
            self.update_coords(mouse_instance)
            self.update_rotation()
        health_bar_pos = [
            int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                / 2),
            self.edges["top_left"][1]
        ]
        self.update_health_bar(screen, health_bar_pos)

        bullet_velocity = self.generate_bullet_velocity()
        self.fire_bullets(screen, Constants.BULLET_DAMAGE, bullet_velocity[0],
                          bullet_velocity[1], main)
        screen.blit(self.rotated_image, self.edges["top_left"])

    def generate_bullet_velocity(self) -> list:
        bullet_velocity = [0, 0]
        ship_quadrant = GenFunctions \
            .get_quadrant(0, 0, angle_from_center=self.angle_from_center)
        sine_angle_abs = math.fabs(math.sin(math.radians(
            self.angle_from_center)))
        cosine_angle_abs = math.fabs(math.cos(math.radians(
            self.angle_from_center)))

        if ship_quadrant == 1:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs * -1
        elif ship_quadrant == 2:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs * -1
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs * -1
        elif ship_quadrant == 3:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs * -1
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs
        else:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs

        return bullet_velocity

    def update_rotation(self):
        ship_center = self.get_center()
        y_delta_from_center = ship_center[1] - Constants.CENTER[1]
        x_delta_from_center = ship_center[0] - Constants.CENTER[0]
        try:
            base_angle_from_center = math.degrees(
                math.atan(abs(y_delta_from_center) / abs(x_delta_from_center)))
        except ZeroDivisionError:
            return
        quadrant = GenFunctions.get_quadrant(ship_center[0], ship_center[1])
        if quadrant == 1:
            self.angle_from_center = 90 + base_angle_from_center
        elif quadrant == 2:
            self.angle_from_center = 270 - base_angle_from_center
        elif quadrant == 3:
            self.angle_from_center = 270 + base_angle_from_center
        elif quadrant == 4:
            self.angle_from_center = 90 - base_angle_from_center
        self.rotated_image = pygame.transform. \
            rotate(self.scaled_ship_image, self.angle_from_center)

    def update_coords(self, mouse_instance: EyeGazeInstance):
        self.edges["top_left"][0] = self.edges["top_left"][0] \
                                    - mouse_instance.unit_x_displacement \
                                    * self.SPEED
        self.edges["top_left"][1] = self.edges["top_left"][1] \
                                    - mouse_instance.unit_y_displacement \
                                    * self.SPEED
        self.update_edges(self.edges["top_left"])

        if GenFunctions.out_of_range(self.edges["top_left"][0],
                                     self.edges["top_left"][1]):
            self.out_of_range = True
