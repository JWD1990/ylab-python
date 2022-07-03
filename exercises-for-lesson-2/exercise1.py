from itertools import permutations
from typing import Optional


Point_coords = tuple[int, ...]
Points_coords = list[Point_coords]
Point_numbers = dict[str, Point_coords]
Path = Optional[list[tuple[Point_coords, float]]]
Last_point_coords = Point_coords


def get_distance_between_points(
    start: Point_coords,
    end: Point_coords
) -> float:
    return (
        (end[0] - start[0]) ** 2 +
        (end[1] - start[1]) ** 2
    ) ** 0.5


def show_paths(points_coords: Points_coords) -> None:
    point_numbers: Point_numbers = {
        str(i): coord for i, coord in enumerate(points_coords)
    }
    point_numbers_without_start_point: list[str] = \
        list(point_numbers.keys())[1:]
    distances: dict[str, float] = {}
    path: Path = None

    point_numbers_permutations: list[tuple[str, ...]] = permutations(
        point_numbers_without_start_point,
        len(point_numbers) - 1
    )

    # считаем длину каждого пути
    start_coords: Point_coords = point_numbers['0']

    for permutation in point_numbers_permutations:
        last_point_number: str = '0'
        total_distance: float = 0.0
        last_coords: Last_point_coords = start_coords
        cur_path: Path = [(start_coords, 0)]  # старт с почты
        permutation += ('0',)  # на почту вернуться в конце надо

        for number in permutation:
            cur_coords: Point_coords = point_numbers[number]
            distance_key: tuple[str, ...] = (
                last_point_number + number,
                number + last_point_number
            )

            if any([
                distance_key[0] in distances,
                distance_key[1] in distances
            ]):  # возьмём дистанцию, eсли она посчитана
                total_distance += distances[
                    distance_key[0] if distance_key[0] in distances
                    else distance_key[1]
                ]
            else:  # или считаем и запоминаем, направление не важно
                new_distance: float = get_distance_between_points(
                    last_coords, cur_coords
                )
                total_distance += new_distance
                distances[last_point_number + number] = new_distance

            cur_path.append((cur_coords, total_distance))
            last_point_number = number
            last_coords = cur_coords

        if not path or (path and path[-1][1] > total_distance):
            path = cur_path

    # выводим путь
    path_str: str = ''
    len_path: int = len(path) - 1
    for i, point in enumerate(path):
        coords: Point_coords = point[0]
        path_str += f'({coords[0]}, {coords[1]})'

        if point[1]:
            path_str += f'[{point[1]}]'

        if len_path != i:
            path_str += ' -> '
        else:
            path_str += f' = {point[1]}'
    print(path_str)


points_coords: Points_coords = [
    (0, 2), (2, 5), (5, 2), (6, 6), (8, 3)
]
show_paths(points_coords)
