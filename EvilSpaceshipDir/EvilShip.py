import pygame
import MouseInstance
from ConstantVars import Constants, Colors, GenFunctions
import math


class EvilShip:
    def __init__(self):
        self.velocity = Constants.EVIL_SHIPS_VELOCITY
        self.health = 100
        self.top_left = list(GenFunctions.rand_coord())
        raw_spaceship_image = pygame.image.load(
            r'EvilSpaceshipDir\\evil_ship_icon.png')
        self.EVIL_SHIP_HEIGHT = 50
        self.EVIL_SHIP_WIDTH = 50
        self.scaled_spaceship_image = pygame.transform \
            .scale(raw_spaceship_image, (self.EVIL_SHIP_WIDTH,
                                         self.EVIL_SHIP_HEIGHT))
        self.rotated_image = self.scaled_spaceship_image
        self.angle_rotation = 0  # in deg, from center
        self.out_of_range = False
        self.bullets = []

    def update_evil_ship(self, screen, mouse_instance: MouseInstance):
        center = self.get_center()
        self.update_rotation(center)
        self.update_coords(mouse_instance)
        self.fire_bullets(screen, center)
        screen.blit(self.rotated_image, self.top_left)
        return self.get_center()

    def update_rotation(self, center: list):
        y_delta_from_center = center[1] - Constants.CENTER_Y
        x_delta_from_center = center[0] - Constants.CENTER_X
        try:
            base_angle_from_center = math.degrees(
                math.atan(abs(y_delta_from_center) / abs(x_delta_from_center)))
        except ZeroDivisionError:
            return
        quadrant = GenFunctions.get_quadrant(center[0], center[1])
        if quadrant == 1:
            self.angle_rotation = 90 + base_angle_from_center
        elif quadrant == 2:
            self.angle_rotation = 270 - base_angle_from_center
        elif quadrant == 3:
            self.angle_rotation = 270 + base_angle_from_center
        elif quadrant == 4:
            self.angle_rotation = 90 - base_angle_from_center
        self.rotated_image = pygame.transform. \
            rotate(self.scaled_spaceship_image, self.angle_rotation)

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

        if GenFunctions.out_of_range(self.top_left[0], self.top_left[1]):
            self.out_of_range = True

    def fire_bullets(self, screen, ship_center: list):
        new_bullet = EvilSpaceshipBullet(self.angle_rotation, ship_center)
        self.bullets.append(new_bullet)
        bullets_to_remove = []
        for bullet_i, bullet in enumerate(self.bullets):
            bullet.update_screen_pos(screen)
            if bullet.out_of_range:
                bullets_to_remove.append(bullet_i)
        for bullet_to_remove in bullets_to_remove:
            try:
                self.bullets.pop(bullet_to_remove)
            except IndexError:
                self.bullets.pop()

    def get_center(self) -> list:
        return [
            int(self.top_left[0] + self.EVIL_SHIP_WIDTH / 2),
            int(self.top_left[1] + self.EVIL_SHIP_HEIGHT / 2)
        ]


class EvilSpaceshipBullet:
    def __init__(self, angle_rotation: int, ship_center: list):
        self.SPEED = 10
        self.x_velocity = 0
        self.y_velocity = 0
        self.coord = [ship_center[0], ship_center[1]]
        self.define_x_y_velocity(angle_rotation)
        # print(self.x_velocity, self.y_velocity)
        self.out_of_range = False

    def update_screen_pos(self, screen):
        self.update_coord()
        pygame.draw.rect(screen, Colors.RED,
                         pygame.Rect(self.coord[0], self.coord[1],
                                     Constants.BULLET_WIDTH,
                                     Constants.BULLET_WIDTH))

    def define_x_y_velocity(self, angle_rotation: int):
        angle_rotation_rad = math.radians(angle_rotation)
        self.x_velocity = int(self.SPEED
                              * abs(math.cos(angle_rotation_rad)))
        self.y_velocity = int(self.SPEED
                              * abs(math.sin(angle_rotation_rad)))
        quadrant = GenFunctions.get_quadrant(self.coord[0], self.coord[1])
        if quadrant == 1:
            self.x_velocity = -self.y_velocity
        elif quadrant == 2:
            pass
        elif quadrant == 3:
            self.y_velocity = -self.y_velocity
        elif quadrant == 4:
            self.x_velocity = -self.x_velocity
            self.y_velocity = -self.y_velocity

    def update_coord(self):
        self.coord[0] = self.coord[0] + self.x_velocity
        self.coord[1] = self.coord[1] + self.y_velocity
        if GenFunctions.out_of_range(self.coord[0], self.coord[1]):
            self.out_of_range = True
