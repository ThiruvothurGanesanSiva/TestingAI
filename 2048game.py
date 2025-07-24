import random
import os
import sys
import msvcrt

# Constants
GRID_SIZE = 4

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def init_game():
    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def print_grid(grid):
    clear_console()
    print("2048 Game\nUse arrow keys to move. Press 'q' to quit.\n")
    for row in grid:
        print("+------"*GRID_SIZE + "+")
        print("".join(f"|{str(num).center(6) if num != 0 else ' '*6}" for num in row) + "|")
    print("+------"*GRID_SIZE + "+")

def compress(row):
    """Slide all non-zero elements to the left."""
    new_row = [num for num in row if num != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def merge(row):
    """Merge the row to the left."""
    for i in range(GRID_SIZE-1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    return row

def move_left(grid):
    moved = False
    new_grid = []
    for row in grid:
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        if final != row:
            moved = True
        new_grid.append(final)
    return new_grid, moved

def move_right(grid):
    reversed_grid = [row[::-1] for row in grid]
    moved_grid, moved = move_left(reversed_grid)
    return [row[::-1] for row in moved_grid], moved

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_up(grid):
    transposed = transpose(grid)
    moved_grid, moved = move_left(transposed)
    return transpose(moved_grid), moved

def move_down(grid):
    transposed = transpose(grid)
    moved_grid, moved = move_right(transposed)
    return transpose(moved_grid), moved

def is_game_over(grid):
    for move_func in [move_left, move_right, move_up, move_down]:
        _, moved = move_func([row[:] for row in grid])
        if moved:
            return False
    return True

def get_key():
    """Read arrow key input on Windows."""
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # Special key prefix
            key = msvcrt.getch()
            if key == b'H': return 'UP'
            elif key == b'P': return 'DOWN'
            elif key == b'K': return 'LEFT'
            elif key == b'M': return 'RIGHT'
        elif key == b'q':
            return 'QUIT'

def main():
    grid = init_game()
    while True:
        print_grid(grid)
        if is_game_over(grid):
            print("Game Over!")
            break

        key = get_key()
        if key == 'QUIT':
            print("Goodbye!")
            break

        moved = False
        if key == 'LEFT':
            grid, moved = move_left(grid)
        elif key == 'RIGHT':
            grid, moved = move_right(grid)
        elif key == 'UP':
            grid, moved = move_up(grid)
        elif key == 'DOWN':
            grid, moved = move_down(grid)

        if moved:
            add_random_tile(grid)

if __name__ == "__main__":
    main()
