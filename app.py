import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arrow Key Reaction Game")

# Define colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Initial position of a rectangle
rect_x, rect_y = screen_width // 2, screen_height // 2
rect_width, rect_height = 50, 50
rect_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()

    # React to arrow key presses
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed  # Move left
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed  # Move right
    if keys[pygame.K_UP]:
        rect_y -= rect_speed  # Move up
    if keys[pygame.K_DOWN]:
        rect_y += rect_speed  # Move down

    # Fill the screen with white
    screen.fill(white)

    # Draw the rectangle
    pygame.draw.rect(screen, blue, (rect_x, rect_y, rect_width, rect_height))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
