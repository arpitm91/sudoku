import cv2
import numpy as np

from skimage.segmentation import clear_border
from src.DigitRecognizer import Recognizer
from src.Board import Board
from src.Constants import (
    FONT,
    FONT_SCALE,
    FONT_THICKNESS,
    FONT_COLOR,
    SEE_DIGIT,
    SEE_DIGIT_TIME,
    FONT_LINE_TYPE,
)

wait_time = 1

recognizer = Recognizer()


def puzzle_to_board(puzzle_image: np.ndarray) -> list:
    h, w = puzzle_image.shape[:2]
    assert h == w, "Puzzle image must be square"
    assert h % 9 == 0, "Puzzle image must be divisible by 9"
    digit_size = h // 9
    board = []
    display_image = puzzle_image.copy()
    for i in range(9):
        row = []
        for j in range(9):
            x = j * digit_size
            y = i * digit_size
            digit = puzzle_image[y : y + digit_size, x : x + digit_size]
            digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
            digit = cv2.GaussianBlur(digit, (7, 7), 3)
            digit = cv2.threshold(
                digit, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
            )[1]
            digit = clear_border(digit)

            (h, w) = digit.shape
            percentageFilled = cv2.countNonZero(digit) / float(w * h)
            if percentageFilled < 0.03:
                result = 0
            else:
                digit_r = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)
                result = recognizer.predict(digit_r)
            if SEE_DIGIT:
                display_image[y : y + digit_size, x : x + digit_size] = cv2.cvtColor(
                    digit, cv2.COLOR_GRAY2BGR
                )
                cv2.imshow("digit", display_image)
                cv2.waitKey(SEE_DIGIT_TIME)
            text_image = puzzle_image[y : y + digit_size, x : x + digit_size].copy()
            if result != 0:
                text = str(result)
                textsize = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
                textX = (digit_size - textsize[0]) // 2
                textY = (digit_size + textsize[1]) // 2
                cv2.putText(
                    text_image,
                    text,
                    (textX, textY),
                    FONT,
                    FONT_SCALE,
                    FONT_COLOR,
                    FONT_THICKNESS,
                    FONT_LINE_TYPE,
                )
            # digit = np.concatenate((digit, text_image), axis=1)
            if SEE_DIGIT:
                display_image[y : y + digit_size, x : x + digit_size] = text_image
                cv2.imshow("digit", display_image)
                cv2.waitKey(SEE_DIGIT_TIME)
            row.append(result)
        board.append(row)
    cv2.destroyAllWindows()
    return Board(board)
