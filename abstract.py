from typing import Mapping, Any, Callable, TextIO

# Набор параметров - это иммутабельный словарь,
# с особым поведением при добавлении новых данных
class ParamSet:
    __data: Mapping[str, Any]

    def __init__(self, src: Mapping[str, Any]) -> None:
        self.__data = src

    @property
    def data(self) -> Mapping[str, Any]:
        return self.__data

    def update(self, src: Mapping[str, Any]) -> "ParamSet":
        return ParamSet(dict(self.__data) | dict(src))

    def append(self, src: Mapping[str, Any]) -> "ParamSet":
        duplicates = self.__data.keys() & src.keys()
        assert not duplicates, duplicates
        return self.update(src)


# Вместо абстрактных классов с 1 методом
# лучше уж использовать функции
type ParamReader = Callable[[], ParamSet]
type ParamWriter = Callable[[ParamSet], None]


def text_param_reader(src: TextIO) -> ParamReader:
    def reader() -> ParamSet:
        ...
    return reader

def text_param_writer(dest: TextIO) -> ParamWriter:
    def writer(params: ParamSet) -> None:
        ...
    return writer
