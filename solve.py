from src.Board import Board
from src.Solver import Solver

board = Board.from_string(
    """
╔═════╦═════╦═════╗
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
╠═════╬═════╬═════╣
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
╠═════╬═════╬═════╣
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
║· · ·║· · ·║· · ·║
╚═════╩═════╩═════╝
"""
)

solver = Solver(board)
print(solver.solution())
