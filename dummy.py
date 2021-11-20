from ConstantVars import Constants, Colors
# Simple pygame program

# Import and initialize the pygame library
import pygame


def main():
    run()

def run():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([Constants.WINDOW_WIDTH,
                                     Constants.WINDOW_HEIGHT])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill(Colors.BLACK)

        # Draw a solid blue circle in the center
        btm_mid = [Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT]
        sides = [
            [btm_mid[0] - 300, btm_mid[1]],
            [btm_mid[0] + 300, btm_mid[1]],
            [btm_mid[0], btm_mid[1] - 150],
        ]
        pygame.draw.polygon(screen, Colors.WHITE, sides)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
