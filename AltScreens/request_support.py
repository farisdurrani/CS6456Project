import random
from ConstantVars import Constants, Colors
import pygame.draw


class RequestSupport:
    def __init__(self):
        self.available_friends = []
        self.generate_friends()

        self.friends_requested = []

    def update_gui(self, screen):
        # citation for translucent: https://stackoverflow.com/questions/
        # 6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
        translucent_surface = pygame.Surface((Constants.WINDOW_WIDTH,
                                              Constants.WINDOW_HEIGHT))
        translucent_surface.set_alpha(128)  # alpha level
        translucent_surface.fill(Colors.WHITE)  # this fills the entire surface
        screen.blit(translucent_surface, (0, 0))

        background = pygame.Surface((Constants.WINDOW_WIDTH / 2,
                                     Constants.WINDOW_HEIGHT))
        background.fill(Colors.WHITE)  # this fills the entire surface
        screen.blit(background, (int(Constants.WINDOW_WIDTH / 2), 0))

        FRIEND_PIC_HEIGHT = 50
        GENERAL_MARGIN = 10
        LEFT_MARGIN = 20

        for friend_i, friend in enumerate(self.available_friends):
            friend_pic_pos = [
                Constants.WINDOW_WIDTH // 2 + LEFT_MARGIN,
                GENERAL_MARGIN
            ]
            pygame.draw.rect(screen, Colors.BLACK,
                             (friend_pic_pos[0], friend_pic_pos[1],
                              FRIEND_PIC_HEIGHT, FRIEND_PIC_HEIGHT))
            request_button_pos = [
                Constants.WINDOW_WIDTH // 2 + LEFT_MARGIN + FRIEND_PIC_HEIGHT
                + GENERAL_MARGIN,
                GENERAL_MARGIN
            ]
            request_button_width = Constants.WINDOW_WIDTH // 2 - \
                                   LEFT_MARGIN * 2 + GENERAL_MARGIN
            pygame.draw.rect(screen, Colors.SILVER,
                             (request_button_pos[0], request_button_pos[1],
                              request_button_width, FRIEND_PIC_HEIGHT))

            # render text
            req_support_label = Constants.HEADING_1_FONT.render(
                "Request Support", False, Colors.BLACK)
            req_support_label_pos = [
                request_button_pos[0] // 2 - req_support_label.get_width() // 2,
                request_button_pos[1] // 2 - req_support_label.get_height() // 2
            ]
            screen.blit(req_support_label, tuple(req_support_label_pos))

    def generate_friends(self):
        FRIEND_NAMES = ["Aman", "Bo", "Charlie",
                        "AJ", "Jackson", "Sam",
                        "Jonathan", "Patrick", "John",
                        "Subbarao"]
        friend_limit = random.randint(1, 10)
        self.available_friends = FRIEND_NAMES[:friend_limit]
