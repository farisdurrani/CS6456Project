from ConstantVars import Constants
import random


def out_of_range(x: int, y: int) -> bool:
    return (x < 0 or x > Constants.WINDOW_WIDTH
            or y < 0 or y > Constants.WINDOW_HEIGHT)


def rand_coord() -> tuple:
    x = random.randint(0, Constants.WINDOW_WIDTH)
    y = random.randint(0, Constants.WINDOW_HEIGHT)
    return x, y


def get_quadrant(x_delta: int, y_delta: int) -> int:
    # with respect to center of screen
    x_center = Constants.CENTER_X
    y_center = Constants.CENTER_Y
    if x_delta >= x_center and y_delta < y_center:
        return 1
    elif x_delta < x_center and y_delta < y_center:
        return 2
    elif x_delta < x_center and y_delta >= y_center:
        return 3
    elif x_delta >= x_center and y_delta >= y_center:
        return 4
