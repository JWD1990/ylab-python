def bananas(s: str, idx_in_teststr: int = 0) -> set:
    teststr: str = 'banana'
    # 0 - значит последний символ
    count_next_chs: int = len(teststr) - 1 - idx_in_teststr
    result = set()

    for offset, ch in enumerate(s):
        next_idx: int = offset + 1
        count_last_pos: int = len(s) - next_idx

        # есть ли позиции для размещения оставшихся символов
        if count_next_chs > count_last_pos:
            break

        if ch != teststr[idx_in_teststr]:
            continue

        tmp_s: str = ('-' * offset) + ch

        if not count_next_chs:  # последний символ teststr?
            tmp_s += '-' * (count_last_pos)
            result.add(tmp_s)
        else:
            res_set = bananas(s[next_idx:], idx_in_teststr + 1)

            for part_s in res_set:  # пустота не будет итерироваться
                result.add(tmp_s + part_s)

    return result
