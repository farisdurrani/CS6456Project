import math
import pygame
import time

from ConstantVars import Colors, Constants
from MouseInstance import MouseInstance
from ship import ship_blueprint


class Spaceship(ship_blueprint.Ship):
    def __init__(self):
        # ship characteristics
        SPACESHIP_MAX_HEALTH = 1000
        SPACESHIP_HEIGHT = 80
        SPACESHIP_ICON = r'ship\\spaceship\\spaceship_icon.png'
        TOP_LEFT = [
            int(Constants.CENTER[0] - SPACESHIP_HEIGHT / 2),
            int(Constants.CENTER[1] - SPACESHIP_HEIGHT / 2)
        ]
        super().__init__(SPACESHIP_MAX_HEALTH, TOP_LEFT, SPACESHIP_HEIGHT,
                         SPACESHIP_ICON)

        self.BULLET_SPEED = 10
        self.SHIELD_THICKNESS = 10
        self.SHIELD_LIFE = 4  # in seconds

        self.shield_start_time = 0
        self.time_begin_paused = 0
        self.duration_paused = 0
        self.rotated_image = None

        self.SHIELD_RADIUS = math.sqrt(
            (Constants.CENTER[0] - self.edges["top_left"][0]) ** 2 +
            (Constants.CENTER[1] - self.edges["top_left"][1]) ** 2
        )

        self.health_bar_pos = [
            int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                / 2),
            self.edges["top_left"][1]
        ]

    def update_ship(self, screen, mouse_instance: MouseInstance, main):
        if self.has_shield:
            pygame.draw.circle(screen, Colors.WHITE, tuple(Constants.CENTER),
                               self.SHIELD_RADIUS)
            pygame.draw.circle(screen, Colors.BLACK, tuple(Constants.CENTER),
                               self.SHIELD_RADIUS - self.SHIELD_THICKNESS)
            if time.time() - self.shield_start_time - self.duration_paused \
                    > self.SHIELD_LIFE:
                self.remove_shield()
        self.update_health_bar(screen, self.health_bar_pos)
        self.update_spaceship_rotation(mouse_instance)
        screen.blit(self.rotated_image, self.edges["top_left"])

        bullet_x_velocity = self.BULLET_SPEED \
                            * mouse_instance.unit_x_displacement
        bullet_y_velocity = self.BULLET_SPEED \
                            * mouse_instance.unit_y_displacement
        self.fire_bullets(screen, 5, bullet_x_velocity, bullet_y_velocity, main)

    def update_spaceship_rotation(self, mouse_instance):
        if not self.ship_paused:
            self.angle_from_center = mouse_instance.angle_from_center
            self.rotated_image = pygame.transform.rotate(self.scaled_ship_image,
                                                         self.angle_from_center)

    def add_shield(self):
        self.has_shield = True
        self.shield_start_time = time.time()

    def remove_shield(self):
        self.has_shield = False
        self.time_begin_paused = 0
        self.duration_paused = 0

    def pause_ship(self):
        self.ship_paused = True
        print("paused")
        if self.has_shield:
            self.time_begin_paused = time.time()

    def resume_ship(self):
        self.ship_paused = False
        if self.has_shield:
            self.duration_paused = time.time() - self.time_begin_paused
