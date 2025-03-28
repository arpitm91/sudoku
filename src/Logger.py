import time
from src.Board import Board


class Logger:
    def __init__(self, log_frequency: int = 1) -> None:
        self.log_frequency = log_frequency
        self.start_time = round(time.time())
        self.last_print_time = self.start_time

    def report(self, board: Board, solutions: list[Board]) -> None:
        current_time = time.time()
        if current_time - self.last_print_time > self.log_frequency:
            print(
                f"Found {len(solutions)} solutions in {current_time - self.start_time:.2f} seconds\n{board}"
            )
            self.last_print_time = round(current_time)
