from src.Board import Board
from src.Solver import solve

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

solutions = solve(board, 2000000)

for i, solution in enumerate(solutions):
    print(f"{i+1})\n{solution}")
