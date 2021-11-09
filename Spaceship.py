import pygame
import Constants
import math


def update_spaceship(screen):
    SPACESHIP_HEIGHT = 80
    spaceship_image = pygame.image.load(r'spaceship_icon.png')
    spaceship_image = pygame.transform.scale(spaceship_image,
                                             (SPACESHIP_HEIGHT,
                                              SPACESHIP_HEIGHT))
    angle_rotation = mouse_angle_from_center()
    rotated_image = pygame.transform.rotate(spaceship_image, angle_rotation)

    spaceship_image_width = spaceship_image.get_width()
    spaceship_image_height = spaceship_image.get_height()

    spaceship_image_topleft = (Constants.CENTER_X - spaceship_image_width / 2,
                               Constants.CENTER_Y - spaceship_image_height / 2)

    screen.blit(rotated_image, spaceship_image_topleft)



def mouse_angle_from_center():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    y_delta = mouse_y - Constants.CENTER_Y
    x_delta = mouse_x - Constants.CENTER_X
    mouse_quadrant = get_mouse_quadrant(x_delta, y_delta)
    base_mouse_angle = math.degrees(math.atan(abs(y_delta) / abs(x_delta)))
    if mouse_quadrant == 1:
        return 270 + base_mouse_angle
    elif mouse_quadrant == 2:
        return 90 - base_mouse_angle
    elif mouse_quadrant == 3:
        return 90 + base_mouse_angle
    elif mouse_quadrant == 4:
        return 270 - base_mouse_angle


def get_mouse_quadrant(x_delta, y_delta):
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
