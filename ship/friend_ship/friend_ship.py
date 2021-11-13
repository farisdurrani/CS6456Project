import math

from ship import ship_blueprint
from ConstantVars import GenFunctions, Constants, Colors
import MouseInstance
import random
import pygame


class FriendShip(ship_blueprint.Ship):
    def __init__(self, friend_name):
        FRIEND_MAX_HEALTH = 100
        TOP_LEFT_INITIAL = GenFunctions.rand_coord()
        FRIEND_HEIGHT = 50
        FRIEND_SHIP_ICON = r'ship\\friend_ship\\friend_ship_icon.png'

        super().__init__(FRIEND_MAX_HEALTH, TOP_LEFT_INITIAL, FRIEND_HEIGHT,
                         FRIEND_SHIP_ICON)
        self.SPEED = 8
        self.friend_name = friend_name

    def update_ship(self, screen, mouse_instance: MouseInstance, main):
        health_bar_pos = [
            int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                / 2),
            self.edges["top_left"][1]
        ]
        self.update_health_bar(screen, health_bar_pos)

        # fire bullets
        x_unit_velocity = random.random() * 2 - 1  # [-1, 1]
        y_unit_velocity = random.random() * 2 - 1  # [-1, 1]
        bullet_velocity = [
            self.BULLET_SPEED * x_unit_velocity,
            self.BULLET_SPEED * y_unit_velocity
        ]
        self.fire_bullets(screen, Constants.BULLET_DAMAGE, bullet_velocity[0],
                          bullet_velocity[1], main)

        # rotate and move ship
        if not self.ship_paused:
            self.angle_from_center = random.randint(0, 359)
            self.edges["top_left"] = [
                self.edges["top_left"][0] + self.SPEED * x_unit_velocity,
                self.edges["top_left"][1] + self.SPEED * y_unit_velocity
            ]
            self.update_edges(self.edges["top_left"])
        rotated_image = pygame.transform. \
            rotate(self.scaled_ship_image, self.angle_from_center)
        screen.blit(rotated_image, self.edges["top_left"])

        # put name of friend
        name_label = Constants.FONTS["TEXT_FONT"].render(
            self.friend_name, True, Colors.WHITE)
        name_pos = [
            self.edges["top_left"][0] + self.scaled_ship_image.get_width() // 2
            - name_label.get_width() // 2,
            self.edges["top_left"][1] + self.scaled_ship_image.get_height()
            * 3 // 4
        ]
        screen.blit(name_label, tuple(name_pos))
