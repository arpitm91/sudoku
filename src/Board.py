from enum import Enum

EMPTY = "·"
BLANK = """
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

assert BLANK.count(EMPTY) == 9 * 9
VALID_NUMBERS = set(list(range(10)))
VALID_STRING = f"{EMPTY}123456789"


class BoardState(str, Enum):
    SOLVED = "SOLVED"
    INVALID = "INVALID"
    INCOMPLETE = "INCOMPLETE"


class Board:
    @staticmethod
    def from_string(board: str) -> "Board":
        blank_board, user_board = BLANK.strip(), board.strip()
        assert len(blank_board) == len(user_board)

        arr_board: list[list[int]] = []
        row = []
        for base, user in zip(blank_board, user_board):
            if base == EMPTY:
                assert user in VALID_STRING
                row.append(0 if user == EMPTY else int(user))
            else:
                assert base == user
                if base == "\n":
                    if len(row) == 9:
                        arr_board.append(row)
                        row = []
        return Board(arr_board)

    def __init__(self, board: list[list[int]]) -> None:
        assert len(board) == 9
        for row in board:
            assert len(row) == 9
            for cell in row:
                assert cell in list(range(10))
        self.board = board

    def __str__(self) -> str:
        split_board = list(BLANK)
        split_board_i = 0
        for row in self.board:
            for cell in row:
                while split_board[split_board_i] != EMPTY:
                    split_board_i += 1
                split_board[split_board_i] = str(cell) if cell != 0 else EMPTY
                split_board_i += 1
        return "".join(split_board)

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.board[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.board[key[0]][key[1]] = value

    def compute_state(self) -> BoardState:
        row_left = [set(range(1, 10)) for _ in range(9)]
        col_left = [set(range(1, 10)) for _ in range(9)]
        box_left = [set(range(1, 10)) for _ in range(9)]

        result = BoardState.SOLVED
        try:
            for i in range(10):
                for j in range(10):
                    if self[i, j] == 0:
                        result = BoardState.INCOMPLETE
                    else:
                        row_left[i].remove(self[i, j])
                        col_left[j].remove(self[i, j])
                        box_left[(i // 3) * 3 + j // 3].remove(self[i, j])
        except KeyError:
            return BoardState.INVALID

        return result
