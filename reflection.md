# 1. Отделение интерфейса от реализации
В моём решении соединение с БД устанавливается (и удаляется)
самим классом `DatabaseStorage` при каждом действии.
В примере это делает клиентский код.
С точки зрения интерфейса `Storage` это не важно,
потому что реализация методов чтения и записи инкапсулируется.

Исправление неоптимальной работы с соединением
потребует изменений клиентского кода
в относительно небольшом количестве мест -
там где есть завязка на конкретный класс `DatabaseStorage`.


# 2. Почему давно работающий код всё ещё содержит баги
Решение и у меня и в примере выглядит просто и наглядно,
но не учитывает случаи недопустимых (отрицательных) значений.
Если с отрицательными входными данными ещё можно как-то побороться
через систему типов (добавив класс `NonNegativeAmount`, например),
то проверка на достаточность средств всё равно необходима.
Её, впрочем, тоже можно сделать через систему типов.

## Дополнительное задание
Сделал исправление, используя старые наработки,
оставшиеся после изучения ООП.
В примере простой вывод в консоль, а в моём решении -
статусы, привязанные к методам.

Выглядит громоздко, но 3/4 проверок можно убрать,
используя `NonNegativeAmount`.
Пока не стал выходить на уровень системы типов
(вдруг потом будет такое задание),
но взял на заметку, что уже думаю такими категориями.


# 2. Неполное покрытие кода тестами
В Python нужно проверять аргумент не только на `None`, но и на всё остальное.
И вообще, там вместо списка целых может быть смесь
словарей, вложенных списков, объектов каких-то других типов и т.п.
Вместо того, чтобы разбираться с этими проблемами
я использовал аннотации типов,
так что даже возможная (!) передача None будет отслеживаться линтером
на стадии написания кода.
Это отличная иллюстрация преимуществ явной типизации.

В качестве потенциальной проблемы я выделил ещё возможность того,
что код будет искать целое среднее.
Это может показаться совсем детской ошибкой,
но при использовании дженериков такой исход вполне вероятен.
Логично предположить, что тип результата будет совпадать с типом аргументов,
и это работает для типов с плавающей точкой
(включая комплексные числа, векторы, матрицы и т.д.).
Вот только при использовании такого дженерика для целых чисел нас ждёт фиаско:
здесь тип среднего отличается от типа аргументов.


# 2. Тестирование граничных условий
Я не добавил в тесты граничные случаи из одной оценки,
а также из двух оценок (максимальной и минимальной).
И вообще, я не использовал `AverageCalculator`,
а реализовал совсем другую логику:
средняя оценка - тоже оценка,
то есть, целое число в заданном диапазоне (от 2 до 5).

Поэтому у меня возникли краевые случаи, связанные с округлением:

  - делится нацело;
  - округление к большему;
  - округление к меньшему;
  - ровно посередине - округление к большему.

Случай с `Null`/`None` опять не рассматривался,
так как использовалась аннотация типов,
которая не допускает `None` во входных данных.


# 3. Асинхронное программирование и многопоточность
И моё решение и образец в примере с состоянием гонки
превращают операцию инкремента в атомарную.
В Python мне в учебных целях сначала пришлось
искусственно сделать её неатомарной с помощью `sleep`.
В противном случае потоки выполнялись бы последовательно из-за
[Global interpreted lock](https://docs.python.org/3/glossary.html#term-global-interpreter-lock).

В примере с deadlock в обоих случаях используется
единый порядок блокировки и разблокировки замков.
Если это то, с чем приходится иметь дело при многопоточной разработке,
то лучше бы свести к минимуму разделяемое изменяемое состояние
(как и изменяемое состояние вообще).
В более сложных проектах так легко запутаться!


# Работа с датой и временем
Сразу бросилось в глаза то, что исходная программа может работать
только с одним единственным форматом даты и времени.
Для того, чтобы решить эту проблему
я использовал функцию из стандартной библиотеки,
которая автоматически подбирает подходящий формат.
Идея использовать системные настройки ("локали") мне так и не пришла.


# Сумма массива случайных чисел
Хотя аналог `ForkJoinPool` в Python я не нашёл,
направление мысли было правильным:
переложить задачу управления потоками на автоматический планировщик.
В результате самой сложной частью было разбиение массива на кусочки,
которые нужно было скормить планировщику.
Хорошо было бы и это тоже автоматизировать, как в учебном примере.


# Функциональный подход
Сортировка быстрым слиянием в школе была для меня самым сложным алгоритмом.
Уже не помню почему.
При функциональном подходе всё становится куда проще,
особенно если ввести типы, которые гарантируют
выполнение определённых инвариантов.
В данном случае это сортированный список,
все операции с которым дают новый отсортированный список.
Хорошо бы, если бы компилятор догадался
хранить всё это в паре массивов.