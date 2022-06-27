from itertools import combinations_with_replacement
from math import prod


def count_find_num(cor_divs: list[int], limit: int) -> list[int]:
    if type(limit) != int or type(cor_divs) != list:
        raise TypeError('Один или оба аргумента не корректны')

    numbs: int = 1
    first_numb: int = prod(cor_divs)
    max: int = first_numb

    if max > limit:
        return []

    is_end: bool = False
    ext_pos: int = 0  # у нас len(cor_divs) позиций уже есть (первое число)

    # делаем перестановки и просто смотрим по произведению, что число < limit
    while not is_end:
        combo_list = [
            *combinations_with_replacement(
                cor_divs,
                (ext_pos := ext_pos + 1)
            )
        ]

        second_in_combo: int = 0

        for combo in combo_list:
            numb = prod([*combo] + [first_numb])

            # при том выкидываем превышающие, а если это ещё и
            # первое число из списка комбинаций, то мы пришли к краю,
            # т.к. первая перестановка min по произведению
            if numb > limit:
                if not second_in_combo:
                    is_end = True
                    break

                continue

            numbs += 1

            if max < numb:
                max = numb

            second_in_combo = 1

    return [numbs, max]
