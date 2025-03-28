from src.Board import Board
from src.Logger import Logger
from copy import deepcopy


def _solve(
    board: Board,
    row: int,
    col: int,
    solutions: list[Board],
    max_solutions: int,
    logger: Logger,
) -> None:
    logger.report(board, solutions)
    if col == 9:
        if len(solutions) < max_solutions:
            solutions.append(deepcopy(board))
        return
    if row == 9:
        return _solve(board, 0, col + 1, solutions, max_solutions, logger)

    if board[row, col] != 0:
        return _solve(board, row + 1, col, solutions, max_solutions, logger)

    for num in range(1, 10):
        if len(solutions) >= max_solutions:
            break
        try:
            board[row, col] = num
            _solve(board, row + 1, col, solutions, max_solutions, logger)
        except ValueError:
            continue

    board[row, col] = 0


def solve(board: Board, max_solutions: int = 1) -> list[Board]:
    logger = Logger()
    solutions: list[Board] = []
    _solve(board, 0, 0, solutions, max_solutions, logger)

    if len(solutions) == 0:
        print("No solution found")
    elif len(solutions) < max_solutions:
        print(f"All {len(solutions)} solutions found")
    else:
        print(
            f"Hit max solutions limit of {max_solutions}. There can be more solutions"
        )

    return solutions
