import time
from src.Board import Board
import numpy as np
from src.DisplayPuzzleResult import display_puzzle_result


class Logger:
    def __init__(
        self, log_frequency: int = 1, puzzle_image: None | np.ndarray = None
    ) -> None:
        self.log_frequency = log_frequency
        self.start_time = round(time.time())
        self.last_print_time = self.start_time
        self.puzzle_image = puzzle_image

    def report(self, board: Board, solutions: list[Board]) -> None:
        current_time = time.time()
        if current_time - self.last_print_time > self.log_frequency:
            print(
                f"Found {len(solutions)} solutions in {current_time - self.start_time:.2f} seconds\n{board}"
            )
            if self.puzzle_image is not None:
                display_puzzle_result(self.puzzle_image, board, True)
            self.last_print_time = round(current_time)
