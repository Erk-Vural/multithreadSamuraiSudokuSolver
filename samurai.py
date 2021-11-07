import numpy as np

from file_functions import read_sudoku, check_solution_files_exist
from sudoku import possible
from timer import Timer

# Samurai
sudoku_type = 2
is_solved = False

t = Timer()

# samurai_grid is the version read from file
# puzzle[0] is top_left
# puzzle[1] is top_right
# puzzle[2] is middle
# puzzle[3] is bottom_left
# puzzle[4] is bottom_right
samurai_grid = []
puzzles = [[], [], [], [], []]
solved_puzzles = [[], [], [], [], []]


def list_to_matrix(puzzle_list):
    puzzle_matrix = []
    matrix_line = []

    for x in range(81):
        matrix_line.append(puzzle_list[x])

        if x % 9 == 8 and x > 8 or x == 8:
            puzzle_matrix.append(matrix_line)
            matrix_line = []
    return puzzle_matrix


def convert_to_pieces():
    global puzzles

    # temp puzzle lists
    temp_puzzles = [[], [], [], [], []]

    y_range = len(samurai_grid)
    for y in range(y_range):
        x_range = len(samurai_grid[y])
        for x in range(x_range):
            if y < 6:
                if x < 9:
                    temp_puzzles[0].append(samurai_grid[y][x])
                if x >= 9:
                    temp_puzzles[1].append(samurai_grid[y][x])

            if 6 <= y < 9:
                if x < 9:
                    temp_puzzles[0].append(samurai_grid[y][x])
                if 6 <= x < 15:
                    temp_puzzles[2].append(samurai_grid[y][x])
                if x >= 12:
                    temp_puzzles[1].append(samurai_grid[y][x])

            if 9 <= y < 12:
                temp_puzzles[2].append(samurai_grid[y][x])

            if 12 <= y < 15:
                if x < 9:
                    temp_puzzles[3].append(samurai_grid[y][x])
                if 6 <= x < 15:
                    temp_puzzles[2].append(samurai_grid[y][x])
                if x >= 12:
                    temp_puzzles[4].append(samurai_grid[y][x])

            if y >= 15:
                if x < 9:
                    temp_puzzles[3].append(samurai_grid[y][x])
                if x >= 9:
                    temp_puzzles[4].append(samurai_grid[y][x])

    for i in range(5):
        puzzles[i] = list_to_matrix(temp_puzzles[i])
        print(np.matrix(puzzles[i]))
        print("\n")


def solve(piece_id):
    global is_solved
    global t
    global solved_puzzles

    grid = puzzles[piece_id]

    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, grid) and not is_solved:
                        grid[y][x] = n

                        solve(piece_id)

                        grid[y][x] = 0

                return

    for y in range(9):
        matrix_line = []
        for x in range(9):
            matrix_line.append(grid[y][x])
        solved_puzzles[piece_id].append(matrix_line)
        matrix_line = []

    print("Final version of: " + str(piece_id))
    print(np.matrix(solved_puzzles[piece_id]))
    print("\n")

    is_solved = True


# Solve samurai without threads
def solve_samurai():
    global is_solved

    for i in range(5):
        if i == 2:
            continue

        solve(i)
        is_solved = False

    update_middle()
    solve(2)


def update_middle():
    global puzzles

    for i in range(5):
        if i == 0:
            for y in range(6, 9):
                for x in range(6, 9):
                    puzzles[2][y - 6][x - 6] = solved_puzzles[i][y][x]
        if i == 1:
            for y in range(6, 9):
                for x in range(3):
                    puzzles[2][y - 6][x + 6] = solved_puzzles[i][y][x]
        if i == 3:
            for y in range(3):
                for x in range(6, 9):
                    puzzles[2][y + 6][x - 6] = solved_puzzles[i][y][x]
        if i == 4:
            for y in range(3):
                for x in range(3):
                    puzzles[2][y + 6][x + 6] = solved_puzzles[i][y][x]

    print("Updated version of: " + str(2))
    print(np.matrix(puzzles[2]))
    print("\n")


def main():
    global samurai_grid

    samurai_grid = read_sudoku(sudoku_type)
    print("Read Version: ")
    print(samurai_grid)
    print("\n")

    check_solution_files_exist(sudoku_type)

    convert_to_pieces()

    solve_samurai()


if __name__ == "__main__":
    main()
