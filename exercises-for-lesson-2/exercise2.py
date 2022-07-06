from typing import Optional
from random import randint
from os import system, name
import re


Area_data = list[list[str]]
Free_cells_Area = dict[int, list[int]]
Coords = tuple[int, ...]  # row, col
Cell_data = Optional[Coords]
Selected_cell = Cell_data
Actions_on_coords = Coords


def show_rules():
    print("""
    "Обратные крестики-нолики"

    Игра происходит по правилам "Пять в ряд", но проигрывает тот, у кого
    получился вертикальный, горизонтальный или диагональный ряд из пяти
    своих фигур (крестиков/ноликов).

    Чтобы поставить свою фигуру, необходимо просто указать номер строки и,
    через пробел, номер столбца, затем нажать Enter (Ввод) для завершения
    своего хода. Если эта клетка уже занята, нужно будет ввести другую)
    """)


def generate_new_area(rows: int, cols: int) -> Area_data:
    return [[' ' for __ in range(cols)] for _ in range(rows)]


def area_render(data_area: Area_data, rows: int, cols: int) -> None:
    col_width: int = 3
    indent: str = ' ' * col_width
    numb_decor_elms: int = cols * (col_width + 1) + 1
    decor_str: str = f'{indent}{"-" * numb_decor_elms}'
    head_area: list[str] = [
        (
            f'{idx:^{col_width}}'
            if len(str(idx)) < 2 else
            f'{idx:>{col_width}}'
        ) + ' '
        for idx in range(1, cols + 1)
    ]
    area_str: str = f'{indent} {"".join(head_area)}\n{decor_str}\n'

    for row_idx, row in enumerate(data_area, start=1):
        area_str += f'{row_idx:<{col_width}}|'

        for col in row:
            area_str += f'{col:^{col_width}}|'

        area_str += '\n' + (decor_str + '\n' if row_idx != rows else '')

    area_str += decor_str
    print(area_str, end='\n\n')


def is_free_cell(area: Area_data, cell_data: Cell_data) -> bool:
    return area[cell_data[0]][cell_data[1]] == ' '


def del_free_cell(cell_data: Cell_data, area: Free_cells_Area) -> None:
    row: Optional[list[int]] = area.get(cell_data[0], None)

    # AI почистил)
    if not row:
        return None

    if len(row) == 1:
        del area[cell_data[0]]
        return None

    if cell_data[1] in row:
        row.remove(cell_data[1])


def mark_cell(area: Area_data, cell_data: Cell_data, mark: str) -> None:
    area[cell_data[0]][cell_data[1]] = mark


def check_lose(
    area: Area_data, rows: int, cols: int,
    center: Cell_data, check_mark: str
) -> bool:
    '''
    Смотрим квадратик 9 на 9 с центром в нашей текущей ячейке,
    и проверяем в нём главную, доп диагонали и центральные линии

    count_line_elms_for_lose - глобалка
    '''

    have_full_line: bool = False
    side_elms: int = int(count_line_elms_for_lose / 2)
    max_side_elms: int = side_elms * 2
    check_positions: int = max_side_elms * 2 + 1
    start_coords: list[Coords] = [
        (center[0] - max_side_elms, center[1] - max_side_elms),  # left
        (center[0] - max_side_elms, center[1]),                  # vertical
        (center[0] - max_side_elms, center[1] + max_side_elms),  # right
        (center[0], center[1] - max_side_elms),                  # horizontal
    ]
    # каким образом мы будем проходить каждую линию
    actions_on_coords: list[Actions_on_coords] = [
        (1, 1), (1, 0), (1, -1), (0, 1)
    ]

    # перебираем линии
    for idx in range(4):
        if have_full_line:
            break

        cur_coords: Coords = start_coords[idx]
        cur_actions: Actions_on_coords = actions_on_coords[idx]
        count_elms: int = 0

        for offset in range(check_positions):
            d_row_coord: int = cur_coords[0] + cur_actions[0] * offset
            d_col_coord: int = cur_coords[1] + cur_actions[1] * offset

            if not (
                0 <= d_row_coord <= rows - 1 and 0 <= d_col_coord <= cols - 1
            ):
                continue

            value: str = area[d_row_coord][d_col_coord]
            count_elms = count_elms + 1 if value == check_mark else 0

            if count_elms == count_line_elms_for_lose:
                have_full_line = True
                break

    return have_full_line


def get_user_input(rows: int, cols: int) -> Optional[Cell_data]:
    data: list[str] = re.findall('\w+', input('Ваш ход: ').strip())

    if 2 < len(data) or len(data) <= 1 or \
       not data[0].isdigit() or not data[1].isdigit() or \
       int(data[0]) > rows or int(data[1]) > cols:
        return None

    return int(data[0]) - 1, int(data[1]) - 1


def get_user_move(area: Area_data, rows: int, cols: int) -> Cell_data:
    while True:
        selected_cell: Optional[Cell_data] = get_user_input(rows, cols)

        if not selected_cell:
            print('Не корректный ввод, повторите попытку, пожалуйста.')
            continue

        if not is_free_cell(area, selected_cell):
            print('Выберите не занятую ячейку')
            continue

        return selected_cell


def get_free_any_cell(area: Area_data) -> Cell_data:
    for idx_row, row in enumerate(area):
        if ' ' in row:
            return idx_row, row.index(' ')


def get_ai_move(
    free_cells: Free_cells_Area, mark: str, area: Area_data,
    rows: int, cols: int
) -> Cell_data:
    selected_cell: Optional[Cell_data] = None

    while len(free_cells):
        cell: list[int] = []  # [row, col]
        good_rows_idx: list[int] = list(free_cells.keys())
        cell.append(good_rows_idx[randint(0, len(good_rows_idx) - 1)])
        row: list[int] = free_cells[cell[0]]
        cell.append(row[randint(0, len(row) - 1)])
        mark_cell(area, cell, mark)

        if check_lose(area, rows, cols, cell, mark):
            mark_cell(area, cell, ' ')
            del_free_cell(cell, free_cells)
            continue

        selected_cell = tuple(cell)
        break

    return get_free_any_cell(area) if not selected_cell else selected_cell


rows: int = 10
cols: int = 10
count_line_elms_for_lose: int = 5
free_cells: Free_cells_Area = {
    row_idx: [col_idx for col_idx in range(cols)] for row_idx in range(rows)
}
moves: int = rows * cols
have_winner: bool = False
player_lose: bool = False
selected_cell: Cell_data = None
marks: list[str] = ['O', 'X']

area: Area_data = generate_new_area(rows, cols)
show_rules()
area_render(area, rows, cols)

# игровой процесс
while moves > 0:
    is_player_move: bool = moves % 2 == 0
    cur_mark: str = marks[is_player_move]

    if is_player_move:
        selected_cell = get_user_move(area, rows, cols)
    else:
        selected_cell = get_ai_move(free_cells, cur_mark, area, rows, cols)

    moves -= 1
    del_free_cell(selected_cell, free_cells)
    system('CLS' if name == 'nt' else 'clear')
    mark_cell(area, selected_cell, cur_mark)
    area_render(area, rows, cols)

    if check_lose(area, rows, cols, selected_cell, cur_mark):
        player_lose = is_player_move
        have_winner = True
        break

if have_winner:
    print(f'И победителем становится - {("Вы! =)", "Комп o_O")[player_lose]}')
else:
    print('Ничья =)')
