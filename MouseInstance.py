import math
from Constants import Constants
import pygame


class MouseInstance:
    def __init__(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        x_delta = self.mouse_x - Constants.CENTER_X
        y_delta = self.mouse_y - Constants.CENTER_Y
        self.quadrant = self.get_quadrant(x_delta, y_delta)

        self.base_mouse_angle = 0  # in radians, from x-axis
        self.angle_from_center = 0  # counterclockwise, in deg
        self.unit_x_velocity = 0  # from center
        self.unit_y_velocity = 0  # from center
        try:
            self.base_mouse_angle = math.atan(abs(y_delta) / abs(x_delta))
            self.unit_x_velocity = math.cos(self.base_mouse_angle)
            self.unit_y_velocity = math.sin(self.base_mouse_angle)
        except ZeroDivisionError:
            pass
        if self.quadrant == 1:
            self.angle_from_center = 270 + math.degrees(self.base_mouse_angle)
        elif self.quadrant == 2:
            self.angle_from_center = 90 - math.degrees(self.base_mouse_angle)
        elif self.quadrant == 3:
            self.angle_from_center = 90 + math.degrees(self.base_mouse_angle)
        elif self.quadrant == 4:
            self.angle_from_center = 270 - math.degrees(self.base_mouse_angle)

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
