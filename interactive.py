import random
import pygame

# GAME OF LIFE
# createa grid of variable size. It will be a 2D array of cells
# each cell will be a square
# each cell will have a state: alive or dead

# the game will accept a 2d numpy array as input and will display it

def create_grid(size):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(random.randint(0, 1))
        grid.append(row)
    return grid

def display_grid(grid, screen):
    size = len(grid)
    cell_size = 10
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (i*cell_size, j*cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (i*cell_size, j*cell_size, cell_size, cell_size))
    pygame.display.flip()


def create():
    size = 100
    grid = create_grid(size)
    pygame.init()
    screen = pygame.display.set_mode((size*10, size*10))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_grid(grid, screen)
    pygame.quit()

if __name__ == "__main__":
    main()