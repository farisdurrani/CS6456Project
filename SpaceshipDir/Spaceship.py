import pygame

from ConstantVars import Colors, Constants
from MouseInstance import MouseInstance
import math


class Spaceship:
    def __init__(self, screen):
        # ship characteristics
        self.angle_from_center = 0  # counterclockwise, in deg
        self.MAX_HEALTH = 100
        self.health = self.MAX_HEALTH
        self.bullets = []

        # loading ship image
        raw_spaceship_image = pygame.image.load(
            r'SpaceshipDir\\spaceship_icon.png')
        SPACESHIP_HEIGHT = 80
        self.spaceship_image = pygame.transform.scale(raw_spaceship_image,
                                                      (SPACESHIP_HEIGHT,
                                                       SPACESHIP_HEIGHT))
        spaceship_image_width = self.spaceship_image.get_width()
        spaceship_image_height = self.spaceship_image.get_height()
        self.top_left = tuple()
        self.edges = self.define_edges(
            spaceship_image_width, spaceship_image_height)

        # loading variables for health bar
        self.health_bar_pos = [
            int(Constants.CENTER_X - Constants.HEALTH_BAR_LEN / 2),
            self.edges["top_right"][1]
        ]

    def define_edges(self, spaceship_image_width, spaceship_image_height) \
            -> dict:
        self.top_left = (
            Constants.CENTER_X - spaceship_image_width / 2,
            Constants.CENTER_Y - spaceship_image_height / 2)
        top_right = (
            Constants.CENTER_X + spaceship_image_width / 2,
            Constants.CENTER_Y - spaceship_image_height / 2)
        bottom_left = (
            Constants.CENTER_X - spaceship_image_width / 2,
            Constants.CENTER_Y + spaceship_image_height / 2)
        bottom_right = (
            Constants.CENTER_X + spaceship_image_width / 2,
            Constants.CENTER_Y + spaceship_image_height / 2)
        return {
            "top_left": self.top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right
        }

    def update_health_bar(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, (self.health_bar_pos[0],
                                                self.health_bar_pos[1],
                                                Constants.HEALTH_BAR_LEN,
                                                Constants.HEALTH_BAR_HEIGHT))
        current_bar_len = self.health / self.MAX_HEALTH \
                          * Constants.HEALTH_BAR_LEN
        pygame.draw.rect(screen, Colors.RED, (self.health_bar_pos[0],
                                                self.health_bar_pos[1],
                                                current_bar_len,
                                                Constants.HEALTH_BAR_HEIGHT))

    def update_spaceship(self, screen, mouse_instance: MouseInstance):
        self.update_health_bar(screen)
        self.update_spaceship_rotation(screen, mouse_instance)
        self.fire_bullets(screen, mouse_instance)

    def update_spaceship_rotation(self, screen, mouse_instance):
        self.angle_from_center = mouse_instance.angle_from_center
        rotated_image = pygame.transform.rotate(self.spaceship_image,
                                                self.angle_from_center)
        screen.blit(rotated_image, self.top_left)

    def fire_bullets(self, screen, mouse_instance):
        new_bullet = SpaceshipBullet(mouse_instance)
        self.bullets.append(new_bullet)
        bullets_to_remove = []
        for bullet_i, bullet in enumerate(self.bullets):
            bullet.update_screen_pos(screen)
            if bullet.out_of_range:
                bullets_to_remove.append(bullet_i)
        for bullet_to_remove in bullets_to_remove:
            self.bullets.pop(bullet_to_remove)

    def analyze_hit(self, bullet_coord: list, damage: int):
        if self.edges["top_left"][0] <= bullet_coord[0] <= \
                self.edges["bottom_right"][0] \
                and self.edges["top_left"][1] <= bullet_coord[1] <= \
                self.edges["bottom_right"][1]:
            self.health -= damage

    def is_alive(self) -> bool:
        return self.health > 0


class SpaceshipBullet:
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
        self.damage = 5

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

        if self.coord[0] > Constants.WINDOW_WIDTH \
                or self.coord[1] > Constants.WINDOW_HEIGHT:
            self.out_of_range = True

    def get_damage(self) -> int:
        return self.damage
