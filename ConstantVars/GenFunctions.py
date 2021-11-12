import pygame.draw
from ConstantVars import Constants, Colors
import random


def out_of_range(x: int, y: int) -> bool:
    return (x < 0 or x > Constants.WINDOW_WIDTH
            or y < 0 or y > Constants.WINDOW_HEIGHT)


def rand_coord() -> tuple:
    x = random.randint(0, Constants.WINDOW_WIDTH)
    y = random.randint(0, Constants.WINDOW_HEIGHT)
    return x, y


def get_quadrant(x_pos: int, y_pos: int,
                 angle_from_center: float = None) -> int:
    if angle_from_center is not None:
        if angle_from_center <= 90:
            return 2
        elif angle_from_center <= 180:
            return 3
        elif angle_from_center <= 270:
            return 4
        else:
            return 1

    # with respect to center of screen
    x_center = Constants.CENTER[0]
    y_center = Constants.CENTER[1]
    if x_pos >= x_center and y_pos < y_center:
        return 1
    elif x_pos < x_center and y_pos < y_center:
        return 2
    elif x_pos < x_center and y_pos >= y_center:
        return 3
    elif x_pos >= x_center and y_pos >= y_center:
        return 4


def draw_point(screen, coords: list):
    pygame.draw.rect(screen, Colors.GREEN, (coords[0], coords[1], 3, 3))
