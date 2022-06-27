def zeros(n):
    count_zero = 0
    # находим числа (множители), содержащие 5 в своё составе делителей
    res = n // 5
    while res != 0:
        count_zero += res
        res //= 5
    return count_zero
