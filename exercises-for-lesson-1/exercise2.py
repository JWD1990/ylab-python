def int32_to_ip(int32: int) -> str:
    if type(int32) != int:
        raise TypeError('Тип аргумента не int')

    if int32 >= 2**32:
        raise ValueError('Число не является 32 битным целым')

    ip: list[int] = [0, 0, 0, 0]
    idx: int = 1
    res: int = int32

    while int32 >= 256:
        int32 //= 256
        ip[-idx] = (res := res - int32 * 256)
        res = int32
        idx += 1

    ip[-idx] = res

    return '.'.join(map(str, ip))
