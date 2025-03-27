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


def valid_board_string(board: str) -> bool:
    split_board = board.strip().split("\n")
    assert len(split_board) == 13
    assert split_board[0] == "╔═════╦═════╦═════╗"
    assert split_board[4] == "╠═════╬═════╬═════╣"
    assert split_board[8] == "╠═════╬═════╬═════╣"
    assert split_board[12] == "╚═════╩═════╩═════╝"

    for i in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
        assert len(split_board[i]) == 19
        for j in range(19):
            if j % 2 == 1:
                assert split_board[i][j] in "·123456789"
            elif j % 6 == 0:
                assert split_board[i][j] == "║"
            else:
                assert split_board[i][j] == " "
    return True


class Board:
    @staticmethod
    def from_string(board: str) -> "Board":
        if not valid_board_string(board):
            raise ValueError("Invalid board string")
        split_board = board.strip().split("\n")

        arr_board: list[list[int]] = []
        for i in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
            row_board = []
            for j in range(19):
                if j % 2 == 1:
                    if split_board[i][j] == "·":
                        row_board.append(0)
                    else:
                        row_board.append(int(split_board[i][j]))
            arr_board.append(row_board)
        return Board(arr_board)

    def __init__(self, board: list[list[int]]) -> None:
        assert len(board) == 9
        for row in board:
            assert len(row) == 9
            for cell in row:
                assert cell in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.board = board

    def __str__(self) -> str:
        split_board = BLANK.strip().split("\n")
        for arr_i, string_i in enumerate([1, 2, 3, 5, 6, 7, 9, 10, 11]):
            string_row = list(split_board[string_i])
            for j in range(9):
                if self.board[arr_i][j] == 0:
                    string_row[j * 2 + 1] = "·"
                else:
                    string_row[j * 2 + 1] = str(self.board[arr_i][j])
            split_board[string_i] = "".join(string_row)

        return "\n".join(split_board)
