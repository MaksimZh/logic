def max(a: int, b: int) -> int:
    if a >= b:
        return a
    # {(a >= b and return = a) or a < b}
    # это что-то типа монады: продолжаем выполнение, пока return не определён
    return b
    # {(a >= b and return = a) or (a < b and return = b)}
    # следовательно
    # {(return = a and return >= b) or (return = b and return >= a)}
    # следовательно
    # {return >= a and return >= b and return in {a, b}}
    # по определению максимума
# {return = max(a, b)}


def abs(x: int) -> int:
    if x >= 0:
        return x
    # {(x >= 0 and return = x) or x < 0}
    return -x
    # {(x >= 0 and return = x) or (x < 0 and return = -x)}
    # по определению модуля
# {return = |x|}


def maxabs(a: int, b: int) -> int:
    a1 = abs(a)
    # {a1 = |a|}
    b1 = abs(b)
    # {a1 = |a| and b1 = |b|}
    return max(a1, b1)
    # {a1 = |a| and b1 = |b| and return = max(a1, b1)}
    # следовательно
# {return = max(|a|, |b|)}
