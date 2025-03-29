import cv2
import numpy as np

from skimage.segmentation import clear_border
from recognize_digit import Recognizer

SEE_COUNTOURS = True
DIGIT_SIZE = 60
time = 1

image = cv2.imread("./b.webp")

preprocessed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
preprocessed_image = cv2.GaussianBlur(preprocessed_image, (7, 7), 3)
preprocessed_image = cv2.adaptiveThreshold(
    preprocessed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)
preprocessed_image = cv2.bitwise_not(preprocessed_image)
contours = cv2.findContours(
    preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)


puzzle_vertices: cv2.typing.MatLike | None = None
max_area = 0.0

if SEE_COUNTOURS:
    countoured_image = image.copy()
    cv2.drawContours(countoured_image, contours[0], -1, (0, 255, 0), 2)
    cv2.imshow("See Countours", countoured_image)
    cv2.waitKey(time)

for c in contours[0]:
    perimeter = cv2.arcLength(c, True)
    approx_points = cv2.approxPolyDP(c, 0.02 * perimeter, True)

    if len(approx_points) == 4:
        area = cv2.contourArea(c)
        if area > max_area:
            max_area = area
            puzzle_vertices = approx_points

assert puzzle_vertices is not None, "Could not find puzzle contour"

if SEE_COUNTOURS:
    countoured_image = image.copy()
    cv2.drawContours(countoured_image, [puzzle_vertices], -1, (0, 255, 0), 2)
    cv2.imshow("See Countours", countoured_image)
    cv2.waitKey(time)


puzzle_size = 9 * DIGIT_SIZE
src_pts = puzzle_vertices.reshape(4, 2).astype("float32")
dst_pts = np.array(
    [[puzzle_size, 0], [0, 0], [0, puzzle_size], [puzzle_size, puzzle_size]],
    dtype="float32",
)

perspective = cv2.getPerspectiveTransform(src_pts, dst_pts)
warp = cv2.warpPerspective(image.copy(), perspective, (puzzle_size, puzzle_size))
cv2.imshow("warp", warp)
cv2.waitKey(time)


board = []

recognizer = Recognizer()

font = cv2.FONT_HERSHEY_SIMPLEX

for i in range(9):
    row = []
    for j in range(9):
        x = j * DIGIT_SIZE
        y = i * DIGIT_SIZE
        digit = warp[y : y + DIGIT_SIZE, x : x + DIGIT_SIZE]
        digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
        digit = cv2.GaussianBlur(digit, (7, 7), 3)
        digit = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        digit = clear_border(digit)

        (h, w) = digit.shape
        percentageFilled = cv2.countNonZero(digit) / float(w * h)
        if percentageFilled < 0.03:
            result = 0
        else:
            digit_r = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)
            result = recognizer.predict(digit_r)
        cv2.imshow("digit", digit)
        cv2.waitKey(time)
        text_image = np.ones((DIGIT_SIZE, DIGIT_SIZE), dtype=np.uint8) * 255
        text = str(result)
        textsize = cv2.getTextSize(text, font, 1, 2)[0]
        textX = (DIGIT_SIZE - textsize[0]) // 2
        textY = (DIGIT_SIZE + textsize[1]) // 2
        cv2.putText(
            text_image,
            text,
            (textX, textY),
            font,
            1,
            (0, 0, 0),
            2,
        )
        digit = np.concatenate((digit, text_image), axis=1)
        cv2.imshow("digit", digit)
        cv2.waitKey(time)
        row.append(result)
    board.append(row)


board[3][1] = 6
board[4][4] = 6
board[6][6] = 6
from src.Board import Board
from src.Solver import solve

board = Board(board)

solutions = solve(board, 2)

for i, solution in enumerate(solutions):
    print(f"{i+1})\n{solution}")


if len(solutions) > 0:
    result_image = warp.copy()
    final_result = solutions[0]
    for i in range(9):
        for j in range(9):
            if final_result.is_original(i, j):
                continue
            if final_result[i, j] != 0:
                text = str(final_result[i, j])
                textsize = cv2.getTextSize(text, font, 1, 2)[0]
                textX = j * DIGIT_SIZE + ((DIGIT_SIZE - textsize[0]) // 2)
                textY = i * DIGIT_SIZE + ((DIGIT_SIZE + textsize[1]) // 2)
                cv2.putText(
                    result_image,
                    text,
                    (textX, textY),
                    font,
                    1,
                    (0, 0, 0),
                    2,
                )

    cv2.imshow("result", result_image)
    cv2.waitKey(0)
