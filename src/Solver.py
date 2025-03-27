from src.Board import Board, BoardState


class Solver:
    def __init__(self, board: Board) -> None:
        self.board = board

    def _solve(self, row: int, col: int) -> bool:
        if col == 9:
            return True
        if row == 9:
            return self._solve(0, col + 1)

        if self.board[row, col] != 0:
            return self._solve(row + 1, col)

        for num in range(1, 10):
            self.board[row, col] = num
            state = self.board.compute_state()
            if state == BoardState.SOLVED:
                return True
            elif state == BoardState.INVALID:
                continue
            elif self._solve(row + 1, col):
                return True

        self.board[row, col] = 0
        return False

    def solution(self) -> Board:

        self._solve(0, 0)

        if self.board.compute_state() == BoardState.SOLVED:
            print("Solved")
        else:
            print("Unsolvable")

        return self.board
