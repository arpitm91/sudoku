import cv2
from src.Board import Board
from src.Constants import (
    FONT,
    FONT_SCALE,
    FONT_THICKNESS,
    FONT_COLOR,
    FONT_LINE_TYPE,
    TEMPORARY_FONT_COLOR,
)
import numpy as np


def display_puzzle_result(
    puzzle_image: np.ndarray, solution: Board, temporary: bool = False
) -> None:
    h, w = puzzle_image.shape[:2]
    assert h == w, "Puzzle image must be square"
    assert h % 9 == 0, "Puzzle image must be divisible by 9"
    digit_size = h // 9
    result_image = puzzle_image.copy()
    for i in range(9):
        for j in range(9):
            if solution.is_original(i, j):
                continue
            if solution[i, j] != 0:
                text = str(solution[i, j])
                textsize = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
                textX = j * digit_size + ((digit_size - textsize[0]) // 2)
                textY = i * digit_size + ((digit_size + textsize[1]) // 2)
                cv2.putText(
                    result_image,
                    text,
                    (textX, textY),
                    FONT,
                    FONT_SCALE,
                    TEMPORARY_FONT_COLOR if temporary else FONT_COLOR,
                    FONT_THICKNESS,
                    FONT_LINE_TYPE,
                )

    cv2.imshow("result", result_image)
    wait_time = 10 if temporary else 0
    cv2.waitKey(wait_time)
