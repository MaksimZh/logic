from typing import final, cast
from itertools import batched

# Сортировка быстрым слиянием в объектно-императивном стиле

class MergeSorter:
    __data: list[int]

    def __init__(self, data: list[int]) -> None:
        self.__data = data.copy()

    @property
    def data(self) -> list[int]:
        return self.__data

    @property
    def size(self) -> int:
        return len(self.__data)

    def __merge(self, s: int, m: int, f: int) -> None:
        assert 0 <= s and s < m and m < f and f <= self.size
        tmp = list[int]()
        i = s
        j = m
        while i < m and j < f:
            if self.__data[i] < self.__data[j]:
                tmp.append(self.__data[i])
                i += 1
                continue
            tmp.append(self.__data[j])
            j += 1
        tmp += self.__data[i:m] + self.__data[j:f]
        assert len(tmp) == f - s
        self.__data[s:f] = tmp

    
    def merge_chunks(self, l: int) -> None:
        assert 0 < l
        s = 0
        while s <= self.size - 2 * l:
            m = s + l
            f = m + l
            self.__merge(s, m, f)
            s = f
        if s < self.size - l:
            self.__merge(s, s + l, self.size)


def merge_sort(a: list[int]) -> list[int]:
    ms = MergeSorter(a)
    l = 1
    while l < ms.size:
        ms.merge_chunks(l)
        l *= 2
    return ms.data


# Сортировка быстрым слиянием в функциональном стиле

# Сортированный список
@final
class Sorted:
    __data: list[int]

    def __repr__(self) -> str:
        return str(self.__data)

    # Клиентский код может создавать только сортированные списки размера 1
    def __init__(self, data: int) -> None:
        self.__data = [data]

    @property
    def data(self) -> list[int]:
        return self.__data

    @property
    def size(self) -> int:
        return len(self.__data)

    # Секретный конструктор для сортированного списка любого размера
    @classmethod
    def __init(cls, data: list[int]) -> "Sorted":
        instance = cls.__new__(cls)
        instance.__data = data
        return instance    
    
    # Слияние создаёт новый сортированный список,
    def merge(self, other: "Sorted") -> "Sorted":
        # Немного императивного кода внутри, хотя можно и рекурсией
        dest = list[int]()
        a = self.data
        b = other.data
        while a and b:
            if a[0] < b[0]:
                dest.append(a[0])
                a = a[1:]
                continue
            dest.append(b[0])
            b = b[1:]
            continue
        # Используем секретный конструктор
        return self.__init(dest + a + b)


def fun_sort(a: list[int]) -> list[int]:
    s = list(map(Sorted, a))
    while len(s) > 1:
        # Это не совсем stateful-код
        # Мы не меняем значение списка, а выбрасываем старый, заменяя его новым
        s = [
            p[0].merge(p[1]) if len(p) > 1  # слияние пары
            else cast(tuple[Sorted], p)[0]  # простой хвост
            for p in batched(s, 2)]
    # На каждом шаге мы имеем список сортированных списков
    # Должен остаться только один!
    return s[0].data


a = [7, 8, 3, 2, 7, 4, 7, 6, 5, 1, 7, 9, 5, 0, 1, 2, 3, 9, 8]
print(a)
print(merge_sort(a))
print(fun_sort(a))
