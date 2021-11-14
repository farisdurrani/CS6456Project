from ConstantVars import Colors
import pygame


class Button:
    def __init__(self, message: str, font: pygame.font, dimension: list,
                 top_left: list, btn_type: str = "Generic"):
        self.message = message
        self.font = font
        self.width = dimension[0]
        self.height = dimension[1]
        self.btn_type = btn_type

        self.top_left = top_left
        self.bg_color_options = {
            "disabled": Colors.LIGHT_GRAY,
            "enabled": Colors.SILVER,
            "hovered": Colors.WHITE
        }
        self.bg_color = self.bg_color_options["disabled"]

        self.text_color_options = {
            "disabled": Colors.BLACK,
            "enabled": Colors.BLUE
        }
        self.text_color = self.text_color_options["disabled"]
        self.enabled = False

    def update_button(self, screen, event: pygame.event = None):
        # draw button box
        button_rect = pygame.Rect((self.top_left[0], self.top_left[1],
                                   self.width, self.height))
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            self.hover_button()
        else:
            self.dishover_button()
        # if click on button, change color and status
        if event is not None \
                and event.type == pygame.MOUSEBUTTONUP \
                and button_rect.collidepoint(mouse_pos):
            self.click_button()

        pygame.draw.rect(screen, self.bg_color, button_rect)

        # draw label
        label = self.font.render(self.message, True, self.text_color)
        label_pos = [
            self.top_left[0] + self.width / 2 - label.get_width() / 2,
            self.top_left[1] + self.height / 2 - label.get_height() / 2,
        ]

        screen.blit(label, tuple(label_pos))

    def click_button(self):
        if self.enabled:
            self.disable_button()
        else:
            self.enable_button()

    def hover_button(self):
        self.bg_color = self.bg_color_options["hovered"]

    def dishover_button(self):
        if self.enabled:
            self.bg_color = self.bg_color_options["disabled"]
        else:
            self.bg_color = self.bg_color_options["enabled"]

    def enable_button(self):
        self.enabled = True
        self.bg_color = self.bg_color_options["enabled"]
        self.text_color = self.text_color_options["enabled"]

    def disable_button(self):
        self.enabled = False
        self.bg_color = self.bg_color_options["disabled"]
        self.text_color = self.text_color_options["disabled"]

    def update_position(self, top_left):
        self.top_left = top_left

    def is_enabled(self):
        return self.enabled
