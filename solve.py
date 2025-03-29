import cv2
from src.Board import Board
from src.Solver import solve

USE_HARDCODED_BOARD = True
board = Board.from_string(
    """
╔═════╦ARPIT╦═════╗
║· 7 ·║· · 1║4 · ·║
║8 · ·║6 · ·║· · ·║
║· 4 ·║8 · 7║· · ·║
╠═════╬═════╬═════╣
║· · ·║· 9 6║2 · 8║
║3 · ·║2 · 8║5 · 7║
║· · ·║7 · 3║· 9 ·║
╠═════╬═════╬═════╣
║· · 3║· · ·║· · ·║
║· · 5║· · 2║8 7 3║
║· 2 8║· · ·║1 · 5║
╚═════╩═════╩═════╝
"""
)

if not USE_HARDCODED_BOARD:
    from src.PuzzleFinder import find_puzzle
    from src.PuzzleToBoard import puzzle_to_board

    image = cv2.imread("./puzzle_images/b.webp")
    puzzle_image = find_puzzle(image)
    board = puzzle_to_board(puzzle_image)


solutions = solve(board, 2)

for i, solution in enumerate(solutions):
    print(f"{i+1})\n{solution}")

if not USE_HARDCODED_BOARD:
    from src.DisplayPuzzleResult import display_puzzle_result

    for i in range(min(len(solutions), 3)):
        display_puzzle_result(puzzle_image, solutions[i])
