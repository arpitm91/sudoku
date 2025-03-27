from src.Board import Board
from src.Solver import Solver

board = Board.from_string(
    """
╔═════╦═════╦═════╗
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

solver = Solver(board)
[print(solution) for solution in solver.solution(2)]
