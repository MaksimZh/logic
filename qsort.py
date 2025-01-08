from typing import Callable, Optional
from operator import le

# Это максимально абстрактная сортировка.
# Всё, что мы знаем про order:
#     order(a, a) = True
#     not order(a, b) => order(b, a)
#     order(a, b) and order(b, c) => order(a, c)

def quickSort[T](
        data: list[T], order: Callable[[T, T], bool],
        start: int = 0, end: Optional[int] = None):
    if end == None:
        end = len(data) - 1
    # {
    assert 0 <= start and start <= end and end < len(data)
    # }
    # Массив длины меньше 2 уже упорядочен
    if end - start < 1:
        return
        # {sorted(data[start : end + 1])}
    mid = data[(start + end) // 2]
    a = start
    b = end
    # I: {
    #     order(data[start : a], mid)
    #     and order(mid, data[b + 1 : end + 1])
    # }
    while a < b:
        while not order(mid, data[a]):
            # {
            #     order(data[start : a], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and not order(mid, data[a])
            # }
            a += 1
            # {
            #     order(data[start : a - 1], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and not order(mid, data[a - 1])
            # }
            # =>
            # {
            #     order(data[start : a], mid) // из свойств order
            #     and order(mid, data[b + 1 : end + 1])
            # }
        # {
        #     order(data[start : a], mid)
        #     and order(mid, data[b + 1 : end + 1])
        #     and order(mid, data[a]) // завершение цикла
        # }
        while not order(data[b], mid):
            # {
            #     order(data[start : a], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and order(mid, data[a]) 
            #     and not order(data[b], mid)
            # }
            b -= 1
            # {
            #     order(data[start : a], mid)
            #     and order(mid, data[b + 2 : end + 1])
            #     and order(mid, data[a])
            #     and not order(data[b + 1], mid)
            # }
            # =>
            # {
            #     order(data[start : a], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and order(mid, data[a])
            # }
        # {
        #     order(data[start : a], mid)
        #     and order(mid, data[b + 1 : end + 1])
        #     and order(mid, data[a]) 
        #     and order(data[b], mid) // завершение цикла
        # }
        if a == b:
            # {
            #     order(data[start : a], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and order(mid, data[a]) 
            #     and order(data[b], mid)
            #     and a == b
            # }
            # =>
            # {
            #     order(data[start : b + 1], mid)
            #     and order(mid, data[b + 1 : end + 1])
            #     and a == b
            # }
            # инвариант цикла выполняется, т.к. это условие сильнее
            break
        # {
        #     order(data[start : a], mid)
        #     and order(mid, data[b + 1 : end + 1])
        #     and order(mid, data[a]) 
        #     and order(data[b], mid)
        # }
        data[a], data[b] = data[b], data[a]
        # {
        #     order(data[start : a], mid)
        #     and order(mid, data[b + 1 : end + 1])
        #     and order(mid, data[b]) 
        #     and order(data[a], mid)
        # }
        # =>
        # {
        #     order(data[start : a + 1], mid)
        #     and order(mid, data[b : end + 1])
        # }
        a += 1
        b -= 1
        # {
        #     order(data[start : a], mid)
        #     and order(mid, data[b + 1: end + 1])
        # }
        # инвариант цикла выполняется
    # {
    #     (
    #         order(data[start : b + 1], mid)
    #         and order(mid, data[b + 1 : end + 1])
    #         and a == b
    #     )
    #     or (
    #         order(data[start : a], mid)
    #         and order(mid, data[b + 1: end + 1])
    #         and a > b
    #    )
    # }
    # =>
    # {
    #     order(data[start : b + 1], mid)
    #     and order(mid, data[b + 1: end + 1])
    # }
    # =>
    # {order(data[i], data[j]), start <= i <= b, b < j <= end}
    quickSort(data, order, start, b)
    quickSort(data, order, b + 1, end)
    # {
    #     (order(data[i], data[j]), start <= i <= b, b < j <= end)
    #     and sorted(data[start : b + 1])
    #     and sorted(data[b + 1 : end + 1])
    # }
    # => sorted(data[start : end + 1])


a = [1, 8, 4, 9, 8, 5, 6, 4, 3, 9, 5]
print(a)
quickSort(a, le)
print(a)
