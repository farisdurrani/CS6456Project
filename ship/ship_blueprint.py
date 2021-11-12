import random

import pygame
import MouseInstance

from ConstantVars import Constants, Colors


class Ship:
    def __init__(self, max_health: int, top_left: list, height: int, icon: str):
        # ship characteristics
        self.id = random.randint(0, 10_000)
        self.angle_from_center = 0  # counterclockwise, in deg
        self.MAX_HEALTH = max_health
        self.health = self.MAX_HEALTH
        self.bullets = []
        self.has_shield = False
        self.shield_start_time = 0

        # loading ship image
        raw_spaceship_image = pygame.image.load(icon)
        SPACESHIP_HEIGHT = height
        self.scaled_ship_image = pygame.transform.scale(raw_spaceship_image,
                                                        (SPACESHIP_HEIGHT,
                                                         SPACESHIP_HEIGHT))
        self.ship_image_width = self.scaled_ship_image.get_width()
        self.ship_image_height = self.scaled_ship_image.get_height()
        self.edges = dict()
        self.update_edges(top_left)

        # loading variables for health bar

    def update_ship(self, screen, mouse_instance: MouseInstance, main):
        pass

    def update_edges(self, top_left):
        bottom_right = [
            top_left[0] + self.ship_image_width,
            top_left[1] + self.ship_image_height]
        self.edges = {
            "top_left": top_left,
            "bottom_right": bottom_right
        }

    def update_health_bar(self, screen, health_bar_pos: list):
        pygame.draw.rect(screen, Colors.WHITE, (health_bar_pos[0],
                                                health_bar_pos[1],
                                                Constants.HEALTH_BAR_LEN,
                                                Constants.HEALTH_BAR_HEIGHT))
        current_bar_len = self.health / self.MAX_HEALTH \
                          * Constants.HEALTH_BAR_LEN
        pygame.draw.rect(screen, Colors.RED, (health_bar_pos[0],
                                              health_bar_pos[1],
                                              current_bar_len,
                                              Constants.HEALTH_BAR_HEIGHT))

    def fire_bullets(self, screen, damage, x_velocity, y_velocity, main):
        ship_center = self.get_center()
        new_bullet = ShipBullet(ship_center, damage, x_velocity, y_velocity)
        self.bullets.append(new_bullet)

        bullets_to_remove = set()
        for bullet_i, bullet in enumerate(self.bullets):
            bullet.update_screen_pos(screen)
            if bullet.out_of_range:
                bullets_to_remove.add(bullet_i)

        for other_ship in main.all_ships:
            if other_ship.id != self.id:
                for bullet_i, bullet in enumerate(self.bullets):
                    if other_ship.analyze_hit(bullet.get_coord(),
                                              bullet.get_damage()):
                        bullets_to_remove.add(bullet_i)

        for bullet_to_remove in bullets_to_remove:
            try:
                self.bullets.pop(bullet_to_remove)
            except IndexError:
                self.bullets.pop()

        bullets_to_remove.clear()

    def analyze_hit(self, bullet_coord: list, damage: int) -> bool:
        if self.has_shield or not self.is_alive():
            return False
        if self.edges["top_left"][0] <= bullet_coord[0] <= \
                self.edges["bottom_right"][0] \
                and self.edges["top_left"][1] <= bullet_coord[1] <= \
                self.edges["bottom_right"][1]:
            self.health -= damage
            return True
        return False

    def is_alive(self) -> bool:
        return self.health > 0

    def get_center(self) -> list:
        return [
            int((self.edges["top_left"][0]
                 + self.edges["bottom_right"][0]) / 2),
            int((self.edges["top_left"][1]
                 + self.edges["bottom_right"][1]) / 2),
        ]


class ShipBullet:
    def __init__(self, ship_center: list, damage: int, x_velocity, y_velocity,
                 color=Colors.RED, height: int = 3):
        self.coord = [ship_center[0], ship_center[1]]
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.out_of_range = False
        self.damage = damage
        self.color = color
        self.height = height

    def update_screen_pos(self, screen):
        self.coord = [
            self.coord[0] + self.x_velocity,
            self.coord[1] + self.y_velocity
        ]
        if self.coord[0] > Constants.WINDOW_WIDTH \
                or self.coord[1] > Constants.WINDOW_HEIGHT:
            self.out_of_range = True
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.coord[0], self.coord[1],
                                     self.height, self.height))

    def get_damage(self) -> int:
        return self.damage

    def get_coord(self) -> list:
        return self.coord
