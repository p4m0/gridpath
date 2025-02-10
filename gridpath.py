import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 700  # Width and height of the window
GRID_SIZE = 5  # Number of rows and columns in the grid
SQUARE_SIZE = WINDOW_SIZE // (GRID_SIZE + 1)  # Size of each square
MARGIN = SQUARE_SIZE // 5  # Margin between squares
TEXT_SPACE = 50  # Extra space for the text

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Setup the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + TEXT_SPACE))
pygame.display.set_caption("Grid with Paths for Each Start Tile")

# Font for the counter
font = pygame.font.Font(None, 36)  # Default font, size 36

def draw_grid():
    """Draws a 5x5 grid of white squares."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Calculate top-left corner of the square
            x = col * (SQUARE_SIZE + MARGIN) + MARGIN
            y = row * (SQUARE_SIZE + MARGIN) + MARGIN + TEXT_SPACE
            # Draw the square
            pygame.draw.rect(screen, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            # Draw the border around the square
            pygame.draw.rect(screen, GRAY, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)

def get_square_center(row, col):
    """Returns the center coordinates of a square in the grid."""
    x = col * (SQUARE_SIZE + MARGIN) + MARGIN + SQUARE_SIZE // 2
    y = row * (SQUARE_SIZE + MARGIN) + MARGIN + SQUARE_SIZE // 2 + TEXT_SPACE
    return x, y

def generate_paths_from(row, col=0):
    """Generates all valid paths starting from a specific tile."""
    paths = []

    def dfs(r, c, path):
        # If we reach the last column, add the path
        if c == GRID_SIZE - 1:
            paths.append(path)
            return

        # Move right
        if c + 1 < GRID_SIZE:
            dfs(r, c + 1, path + [(r, c + 1)])

        # Move right and up
        if r - 1 >= 0 and c + 1 < GRID_SIZE:
            dfs(r - 1, c + 1, path + [(r - 1, c + 1)])

        # Move right and down
        if r + 1 < GRID_SIZE and c + 1 < GRID_SIZE:
            dfs(r + 1, c + 1, path + [(r + 1, c + 1)])

    # Start DFS from the given tile
    dfs(row, col, [(row, col)])
    return paths

def draw_path(path):
    """Draws a single path on the grid."""
    for i in range(len(path) - 1):
        start = get_square_center(*path[i])
        end = get_square_center(*path[i + 1])
        # Draw the line for this segment
        pygame.draw.line(screen, RED, start, end, 3)
        
def highlight_square(row, col):
    """Highlights a square in red."""
    # Calculate the top-left corner of the square
    x = col * (SQUARE_SIZE + MARGIN) + MARGIN
    y = row * (SQUARE_SIZE + MARGIN) + MARGIN + TEXT_SPACE
    # Draw the square filled with red color
    pygame.draw.rect(screen, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_counter(counter, total_paths, start_tile, total_paths_all_tiles):
    """Draws a counter on the screen."""
    text = f"Tile: {start_tile} | Path: {counter + 1}/{total_paths} | Total Paths: {total_paths_all_tiles}"
    rendered_text = font.render(text, True, YELLOW)
    # Position the text at the top-center of the screen
    text_rect = rendered_text.get_rect(center=(WINDOW_SIZE // 2, TEXT_SPACE // 2))
    screen.blit(rendered_text, text_rect)

def main():
    """Main loop of the program."""
    clock = pygame.time.Clock()

    # Generate paths for each starting tile in the first column
    paths_by_start_tile = {
        row: generate_paths_from(row) for row in range(GRID_SIZE)
    }

    # Total number of paths across all tiles
    total_paths_all_tiles = sum(len(paths) for paths in paths_by_start_tile.values())

    # Current start tile and path index
    current_start_tile = 0
    current_path_index = 0

    # Track whether all paths have been shown
    all_paths_shown = False 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # If all paths have been shown, pause indefinitely
        if all_paths_shown:
            # Clear the screen
            screen.fill(BLACK)
            draw_grid()

            # Display a message indicating completion
            text = "All paths have been displayed. Press Esc to exit."
            rendered_text = font.render(text, True, YELLOW)
            text_rect = rendered_text.get_rect(center=(WINDOW_SIZE // 2, TEXT_SPACE // 2))
            screen.blit(rendered_text, text_rect)
            pygame.display.flip()

            # Check for exit key
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            clock.tick(60)
            continue

        # Get the paths for the current start tile
        current_paths = paths_by_start_tile[current_start_tile]

        # Clear the screen and redraw the grid
        screen.fill(BLACK)
        draw_grid()

        # Highlight the current square in the path
        for (r, c) in current_paths[current_path_index]:
            highlight_square(r, c)
        #draw line according to path
        draw_path(current_paths[current_path_index])
        
            

        # Draw the counter
        draw_counter(
            current_path_index,
            len(current_paths),
            f"({current_start_tile}, 0)",
            total_paths_all_tiles,
        )

        # Update the display
        pygame.display.flip()

        # Wait for a short time and move to the next path
        pygame.time.wait(100)
        current_path_index += 1

        # If we've shown all paths for this tile, move to the next tile
        if current_path_index >= len(current_paths):
            current_path_index = 0
            current_start_tile += 1

            # If we've shown all tiles, mark completion
            if current_start_tile >= GRID_SIZE:
                all_paths_shown = True

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
