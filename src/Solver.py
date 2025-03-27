from src.Board import Board
from copy import deepcopy


class Solver:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.solutions: list[Board] = []

    def _solve(self, row: int, col: int, max_solutions) -> None:
        if col == 9:
            if len(self.solutions) < max_solutions:
                self.solutions.append(deepcopy(self.board))
            return
        if row == 9:
            return self._solve(0, col + 1, max_solutions)

        if self.board[row, col] != 0:
            return self._solve(row + 1, col, max_solutions)

        for num in range(1, 10):
            if len(self.solutions) >= max_solutions:
                break
            self.board[row, col] = num
            if self.board.is_valid():
                self._solve(row + 1, col, max_solutions)

        self.board[row, col] = 0

    def solution(self, max_solutions=1) -> list[Board]:

        self._solve(0, 0, max_solutions)

        if len(self.solutions) == 0:
            print("No solution found")
        elif len(self.solutions) < max_solutions:
            print("All solutions found")
        else:
            print(
                f"Hit max solutions limit of {max_solutions}. There can be more solutions"
            )

        return self.solutions
