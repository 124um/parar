import pygame
import random  # Import random module to enable random selection of dungeon maps
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 640, 480  # Game window size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mother all game")

# Define colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (139, 69, 19)
red = (255, 0, 0)
orange = (255, 165, 0)  # Orange for Dungeon entrance ('D')
map_name = ''

# Define tile size
tile_width, tile_height = 40, 40  # Size of each map tile

# Load the coin image
coin_image = pygame.image.load('./resource/cristal_nb.png')
coin_image = pygame.transform.scale(coin_image, (tile_width, tile_height))  # Scale image to fit the tile size

gate_entrance_image = pygame.image.load('./resource/wind_poodl.png')
gate_entrance_image = pygame.transform.scale(gate_entrance_image, (tile_width, tile_height))  # Scale image to fit the tile size

gate_exit_image = pygame.image.load('./resource/gw1.png')
gate_exit_image = pygame.transform.scale(gate_exit_image, (tile_width, tile_height))  # Scale image to fit the tile size

# Function to read the map from a file
def read_map(filename):
    with open(filename, 'r') as f:
        map_data = [list(line.strip()) for line in f.readlines()]
    name = os.path.splitext(os.path.basename(filename))[0]
    return map_data, name

# Load the first map (main map)
current_map_file = './resource/map1.txt'
map_data, map_name = read_map(current_map_file)
map_width = len(map_data[0])
map_height = len(map_data)

# Player starting position (in tile coordinates)
player_x, player_y = 8, 8  # Start in the middle (adjust as needed)
player_color = (255, 0, 0)  # Red
coin_count = 0  # Initialize coin counter

player_image = pygame.image.load('./resource/bred_true2.png')
player_image = pygame.transform.scale(player_image, (tile_width, tile_height))  # Scale image to fit the tile size

# Font setup for displaying coin count
font = pygame.font.Font(None, 36)

# Camera offset to keep the player centered
camera_x, camera_y = 0, 0

# Function to get a color based on the tile value
def get_color(tile):
    if tile == '0':
        return green  # Grass
    elif tile == '1':
        return blue  # Water
    elif tile == '2':
        return brown  # Wall
    elif tile == 'A':
        return red  # Example for card 'A'
    elif tile == 'D':
        return orange  # Dungeon entrance ('D')
    elif tile == 'E':
        return white  # Dungeon exit ('E') (you can use another color if you like)
    else:
        return white  # Default color for unknown tiles

# Function to check if the next position is blocked
def is_blocked(x, y):
    if 0 <= x < map_width and 0 <= y < map_height:  # Ensure the coordinates are within the map
        tile = map_data[y][x]
        if tile == '1' or tile == '2':  # Block player if the tile is water ('1') or wall ('2')
            return True
    return False

# Function to check if the player is on a coin (yellow tile 'B')
def check_coin(x, y):
    global coin_count
    if map_data[y][x] == 'B':  # Check if the player is on a yellow tile ('B')
        coin_count += 1  # Add 1 to the coin count
        map_data[y][x] = '0'  # Change the tile to grass ('0') after collecting the coin

# Function to switch to a different map (e.g., dungeon map)
def switch_to_map(map_file, new_player_x, new_player_y):
    global map_name, map_data, map_width, map_height, player_x, player_y
    map_data, map_name = read_map(map_file)
    map_width = len(map_data[0])
    map_height = len(map_data)
    player_x, player_y = new_player_x, new_player_y  # Update player's starting position in the new map

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses and move the player once per press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0 and not is_blocked(player_x - 1, player_y):
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < map_width - 1 and not is_blocked(player_x + 1, player_y):
                player_x += 1
            if event.key == pygame.K_UP and player_y > 0 and not is_blocked(player_x, player_y - 1):
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < map_height - 1 and not is_blocked(player_x, player_y + 1):
                player_y += 1

        # Check if the player collects a coin (yellow tile 'B')
        check_coin(player_x, player_y)

        # Check if the player enters a dungeon (tile 'D')
        if map_data[player_y][player_x] == 'D':
            # Randomly choose between 'dange1.txt' and 'dange2.txt'
            dungeon_map = random.choice(['./resource/dange1.txt', './resource/dange2.txt'])
            # Switch to randomly selected dungeon map and set the player's new position
            switch_to_map(dungeon_map, 5, 5)  # For example, player starts at (5, 5) in the dungeon

        # Check if the player exits the dungeon (tile 'E')
        if map_data[player_y][player_x] == 'E':
            # Switch back to the main map (e.g., map1.txt) and set the player's new position
            switch_to_map('./resource/map1.txt', 8, 8)  # Return to the main map, starting at (8, 8)

    # Calculate camera offset to keep player centered, except when near the edges
    if player_x * tile_width < screen_width // 2:  # Player near the left edge
        camera_x = 0
    elif player_x * tile_width > (map_width * tile_width - screen_width // 2):  # Player near the right edge
        camera_x = map_width * tile_width - screen_width
    else:
        camera_x = player_x * tile_width - screen_width // 2 + tile_width // 2

    if player_y * tile_height < screen_height // 2:  # Player near the top edge
        camera_y = 0
    elif player_y * tile_height > (map_height * tile_height - screen_height // 2):  # Player near the bottom edge
        camera_y = map_height * tile_height - screen_height
    else:
        camera_y = player_y * tile_height - screen_height // 2 + tile_height // 2

    # Fill the screen with white
    screen.fill(white)

    # Draw the visible portion of the map
    for row in range(map_height):
        for col in range(map_width):
            tile = map_data[row][col]
            tile_screen_x = col * tile_width - camera_x
            tile_screen_y = row * tile_height - camera_y

            # Draw the gate entrance image for dungeon ('D') and exit image for ('E')
            if tile == 'D':
                screen.blit(gate_entrance_image, (tile_screen_x, tile_screen_y))
            elif tile == 'E':
                screen.blit(gate_exit_image, (tile_screen_x, tile_screen_y))
            elif tile == 'B':  # If tile is 'B', draw the green background and then the coin image
                pygame.draw.rect(screen, green, (tile_screen_x, tile_screen_y, tile_width, tile_height))
                screen.blit(coin_image, (tile_screen_x, tile_screen_y))
            else:
                color = get_color(tile)
                # Only draw tiles that are visible on the screen
                if 0 <= tile_screen_x < screen_width and 0 <= tile_screen_y < screen_height:
                    pygame.draw.rect(screen, color, (tile_screen_x, tile_screen_y, tile_width, tile_height))

    # Draw the player (the player stays centered unless near the map edge)
    player_screen_x = screen_width // 2 - tile_width // 2
    player_screen_y = screen_height // 2 - tile_height // 2

    # When near edges, the player moves toward the edge, not the center
    if player_x * tile_width < screen_width // 2:
        player_screen_x = player_x * tile_width
    elif player_x * tile_width > (map_width * tile_width - screen_width // 2):
        player_screen_x = player_x * tile_width - (map_width * tile_width - screen_width)

    if player_y * tile_height < screen_height // 2:
        player_screen_y = player_y * tile_height
    elif player_y * tile_height > (map_height * tile_height - screen_height // 2):
        player_screen_y = player_y * tile_height - (map_height * tile_height - screen_height)

    # Draw the player image at the computed position
    screen.blit(player_image, (player_screen_x, player_screen_y))

    # Draw the coin count at the top of the screen
    coin_text = font.render(f"Coins: {coin_count} - map - {map_name}", True, (0, 0, 0))
    screen.blit(coin_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
