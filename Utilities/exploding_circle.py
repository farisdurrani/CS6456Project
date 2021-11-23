from typing import List
from ConstantVars import Colors
import pygame
import time


class ExplodingCircle:
    """
    Draws a shrinking circle at the position where enemy ship or asteroid dies.
    Once the circle shrinks to zero, it ceases to exist and will not be
    rendered.

    The current implementation of this program does not implement this class.
    """
    def __init__(self, center: List[int]):
        self.INITIAL_RADIUS = 25
        self.TIME_LIMIT = 2  # in secs

        self.CENTER = center
        self.current_rad = self.INITIAL_RADIUS
        self.time_started = time.time()
        self.ceased_to_exist = False

    def update_explosion(self, screen):
        time_since_start = time.time() - self.time_started
        self.current_rad = (self.TIME_LIMIT - time_since_start) / \
                           self.TIME_LIMIT * self.INITIAL_RADIUS
        pygame.draw.circle(screen, Colors.WHITE, tuple(self.CENTER),
                           self.current_rad)
        if self.current_rad <= 0:
            self.ceased_to_exist = True
