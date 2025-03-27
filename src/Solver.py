from src.Board import Board
from copy import deepcopy
import time


class Solver:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.solutions: list[Board] = []
        self.start_time = time.time()
        self.last_print_time = self.start_time

    def report(self, row: int, col: int):
        current_time = time.time()
        if current_time - self.last_print_time > 1:
            print(
                f"Found {len(self.solutions)} solutions in {current_time - self.start_time:.2f} seconds, currently at row {row}, col {col}"
            )
            print(self.board)
            self.last_print_time = current_time

    def _solve(self, row: int, col: int, max_solutions: int) -> None:
        self.report(row, col)
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
            try:
                self.board[row, col] = num
                self._solve(row + 1, col, max_solutions)
            except ValueError:
                continue

        self.board[row, col] = 0

    def solution(self, max_solutions: int = 1) -> list[Board]:

        self._solve(0, 0, max_solutions)

        if len(self.solutions) == 0:
            print("No solution found")
        elif len(self.solutions) < max_solutions:
            print(f"All {len(self.solutions)} solutions found")
        else:
            print(
                f"Hit max solutions limit of {max_solutions}. There can be more solutions"
            )

        return self.solutions
