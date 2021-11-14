WINDOW_WIDTH = 1244
WINDOW_HEIGHT = 700
CENTER = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]  # [622, 350]
FPS = 10
HEALTH_BAR_LEN = 20
HEALTH_BAR_HEIGHT = 2
FONTS = dict()
BULLET_DAMAGE = 5


def initiate_constants(pygame):
    generate_fonts(pygame)


def generate_fonts(pygame):
    FONTS["HEADING_1_FONT"] = pygame.font.SysFont("arial", 18)
    FONTS["HEADING_2_FONT"] = pygame.font.SysFont("arial", 15)
    FONTS["TEXT_FONT"] = pygame.font.SysFont("arial", 11)
