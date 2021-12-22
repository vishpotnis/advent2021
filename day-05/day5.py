from typing import Union
from enum import Enum
import numpy as np


class LineType(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Point:    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Line:

    maxX = 0
    maxY = 0

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:

        self.start  = Point(x1, y1)
        self.end    = Point(x2, y2)

        Line.maxX = max(Line.maxX, x1)
        Line.maxX = max(Line.maxX, x2)
        Line.maxY = max(Line.maxY, y1)
        Line.maxY = max(Line.maxY, y2)

        self.linetype = self.get_line_type()

    def __str__(self) -> str:
        return f"{str(self.start)} -> {str(self.end)} {str(self.linetype)}"

    def get_slope(self) -> Union[int, None]:
        y_diff = self.end.y - self.start.y
        x_diff = self.end.x - self.start.x

        if x_diff == 0:
            return None
        return int(y_diff/x_diff)

    def get_yint(self) -> int:
        return self.start.y - self.slope * self.start.x

    def get_line_type(self) -> LineType:
        self.slope = self.get_slope()
        if self.slope is None:
            return LineType.VERTICAL

        self.yint = self.get_yint()
        if self.slope == 0:
            return LineType.HORIZONTAL
        return LineType.DIAGONAL

    def get_points(self) -> list[Point]:

        if self.linetype == LineType.VERTICAL:
            return self._get_vertical_points()
        return self._get_line_points()

    def _get_vertical_points(self) -> list[Point]:
        y_start = min(self.start.y, self.end.y)
        y_end = max(self.start.y, self.end.y)
        x_fixed = self.start.x

        points = []
        for y in range(y_start, y_end + 1):
            point = Point(x_fixed, y)
            points.append(point)
        return points

    def _get_line_points(self) -> list[Point]:
        x_start = min(self.start.x, self.end.x)
        x_end = max(self.start.x, self.end.x)

        points = []
        for x in range(x_start, x_end + 1):
            y = self.slope * x + self.yint
            point = Point(x, y)
            points.append(point)
        return points

class Grid:
    def __init__(self, size_x: int, size_y: int) -> None:
        self.grid = np.zeros(shape=(size_y + 1, size_x + 1), dtype=np.int32)

    def __str__(self) -> str:
        return f"{str(self.grid)}"

    def mark_line(self, line: Line) -> None:
        points = line.get_points()

        if points:
            for point in points:
                self.grid[point.y, point.x] += 1

    def calculate_total_dangerous_areas(self) -> int:
        return len(self.grid[self.grid >= 2])


def parse_input(fname) -> list[Line]:

    lines = []
    with open(fname) as file:
        for line in file.readlines():
            tmp = line.strip().split('->')
            x1, y1 = tmp[0].strip().split(',')
            x2, y2 = tmp[1].strip().split(',')

            line = Line(int(x1), int(y1), int(x2), int(y2))
            lines.append(line)
    return lines


def main():
    fname = "day5_input2.txt"
    include_diagonal = True

    lines = parse_input(fname)
    grid = Grid(Line.maxX, Line.maxY)

    for line in lines:
        if not include_diagonal and line.linetype is LineType.DIAGONAL:
            continue
        grid.mark_line(line)

    print(grid)
    print(f"Number of dangerous areas: {grid.calculate_total_dangerous_areas()}")

if __name__ == "__main__":
    main()
