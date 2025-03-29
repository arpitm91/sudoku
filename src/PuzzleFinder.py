import cv2
import numpy as np
from src.Constants import DIGIT_SIZE, SEE_COUNTOURS, SEE_COUNTOURS_TIME


def find_puzzle(image: np.ndarray) -> np.ndarray:
    preprocessed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    preprocessed_image = cv2.GaussianBlur(preprocessed_image, (7, 7), 3)
    preprocessed_image = cv2.adaptiveThreshold(
        preprocessed_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
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
        cv2.waitKey(SEE_COUNTOURS_TIME)

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
        cv2.waitKey(SEE_COUNTOURS_TIME)

    puzzle_size = 9 * DIGIT_SIZE
    src_pts = puzzle_vertices.reshape(4, 2).astype("float32")
    dst_pts = np.array(
        [[puzzle_size, 0], [0, 0], [0, puzzle_size], [puzzle_size, puzzle_size]],
        dtype="float32",
    )

    perspective = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warp = cv2.warpPerspective(image.copy(), perspective, (puzzle_size, puzzle_size))

    return warp
