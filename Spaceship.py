import pygame

import Colors
import Constants
import math


class Spaceship:
    def __init__(self):
        self.angle_from_center = 0  # counterclockwise, in deg
        self.spaceship_image = pygame.image.load(r'spaceship_icon.png')
        SPACESHIP_HEIGHT = 80
        self.spaceship_image = pygame.transform.scale(self.spaceship_image,
                                                      (SPACESHIP_HEIGHT,
                                                       SPACESHIP_HEIGHT))
        spaceship_image_width = self.spaceship_image.get_width()
        spaceship_image_height = self.spaceship_image.get_height()
        self.top_left = (
            Constants.CENTER_X - spaceship_image_width / 2,
            Constants.CENTER_Y - spaceship_image_height / 2)
        self.bullets = []

    def update_spaceship(self, screen):
        mouse_instance = MouseInstance()
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


class MouseInstance:
    def __init__(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        x_delta = self.mouse_x - Constants.CENTER_X
        y_delta = self.mouse_y - Constants.CENTER_Y
        self.quadrant = self.get_quadrant(x_delta, y_delta)

        self.base_mouse_angle = 0  # in deg, from x-axis
        self.angle_from_center = 0  # counterclockwise, in deg
        try:
            self.base_mouse_angle = math.degrees(
                math.atan(abs(y_delta) / abs(x_delta)))
        except ZeroDivisionError:
            pass
        if self.quadrant == 1:
            self.angle_from_center = 270 + self.base_mouse_angle
        elif self.quadrant == 2:
            self.angle_from_center = 90 - self.base_mouse_angle
        elif self.quadrant == 3:
            self.angle_from_center = 90 + self.base_mouse_angle
        elif self.quadrant == 4:
            self.angle_from_center = 270 - self.base_mouse_angle

    def get_quadrant(self, x_delta, y_delta):
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


class SpaceshipBullet:
    def __init__(self, mouse_instance: MouseInstance,
                 ship_center: tuple = (Constants.CENTER_X, Constants.CENTER_Y)):
        self.tangential_velocity = 10
        self.coord = [ship_center[0], ship_center[1]]
        self.mouse_instance = mouse_instance
        base_angle = self.mouse_instance.base_mouse_angle
        self.x_velocity = int(self.tangential_velocity
                              * math.cos(math.radians(base_angle)))
        self.y_velocity = int(self.tangential_velocity
                              * math.sin(math.radians(base_angle)))
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

        if self.coord[0] > Constants.WINDOW_WIDTH \
                or self.coord[1] > Constants.WINDOW_HEIGHT:
            self.out_of_range = True
