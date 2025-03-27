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

        self.row_left = [set(range(1, 10)) for _ in range(9)]
        self.col_left = [set(range(1, 10)) for _ in range(9)]
        self.box_left = [[set(range(1, 10)) for _ in range(3)] for _ in range(3)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        assert len(board) == 9
        for i, row in enumerate(board):
            assert len(row) == 9
            for j, cell in enumerate(row):
                assert cell in list(range(10))
                if cell != 0:
                    self[i, j] = cell

    def __str__(self) -> str:
        split_board = list(BLANK)
        split_board_i = 0
        for row in self.board:
            for cell in row:
                while split_board[split_board_i] != EMPTY:
                    split_board_i += 1
                split_board[split_board_i] = str(cell) if cell != 0 else EMPTY
                split_board_i += 1
        return "".join(split_board).strip()

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.board[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        old_value = self.board[key[0]][key[1]]
        if old_value == value:
            return
        if (
            value not in self.row_left[key[0]]
            or value not in self.col_left[key[1]]
            or value not in self.box_left[key[0] // 3][key[1] // 3]
        ):
            if value != 0:
                raise ValueError(f"Invalid value {value} at {key}")
        if old_value != 0:
            self.row_left[key[0]].add(old_value)
            self.col_left[key[1]].add(old_value)
            self.box_left[key[0] // 3][key[1] // 3].add(old_value)

        if value != 0:
            self.row_left[key[0]].remove(value)
            self.col_left[key[1]].remove(value)
            self.box_left[key[0] // 3][key[1] // 3].remove(value)

        self.board[key[0]][key[1]] = value
