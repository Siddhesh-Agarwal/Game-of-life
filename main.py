import time

import numpy as np
import pygame

BG_COLOR = (5, 5, 5)
GRID_COLOR = (42, 42, 42)
DIE_NEXT_COLOR = (127, 127, 127)
ALIVE_NEXT_COLOR = (255, 255, 255)
SIZE = 10
SLEEP = 0.001


def update(screen, cells, size: int, with_progress: bool = False):
    # updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1 : row + 2, col - 1 : col + 2]) - cells[row, col]
        color = BG_COLOR if cells[row, col] == 0 else ALIVE_NEXT_COLOR

        if cells[row, col] == 1:
            if 2 <= alive <= 3:
                cells[row, col] = 1
                if with_progress:
                    color = ALIVE_NEXT_COLOR
            elif alive > 0:
                cells[row, col] = 0
                if with_progress:
                    color = DIE_NEXT_COLOR
        else:
            if alive == 3:
                cells[row, col] = 1
                if with_progress:
                    color = ALIVE_NEXT_COLOR

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((80 * SIZE, 60 * SIZE))
    cells = np.zeros((60, 80))
    screen.fill(BG_COLOR)
    update(screen, cells, SIZE)

    pygame.display.flip()
    pygame.display.update()
    pygame.display.set_caption("Game of Life")

    running = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                cells[y // SIZE, x // SIZE] = 1
                update(screen, cells, SIZE)
                pygame.display.update()

        screen.fill(GRID_COLOR)

        if running:
            cells = update(screen, cells, SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(SLEEP)


if __name__ == "__main__":
    main()
