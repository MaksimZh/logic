# {len(arr) > 0}
def findMax(arr: list[int]) -> int:
    m = arr[0]
    # {m = arr[0]}
    # I: {0 <= i < len(arr) and m = max(arr[0 : i+1])}
    # перед началом цикла (i = 0) инвариант выполняется:
    #     i = 0 and m = max(arr[0:1])
    for i in range(1, len(arr)):
        # {m = max(arr[0:i])}
        if arr[i] > m:
            # {m = max(arr[0:i]) and arr[i] > m}
            # равносильно
            # {arr[i] = max(arr[0 : i + 1])}
            m = arr[i]
            # {m = max(arr[0 : i + 1])}
            # инвариант выполняется, т.к. по условию цикла:
            #     1 <= i < len(arr)
    return m
# {return = max(arr)}
