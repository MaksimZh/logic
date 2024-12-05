from typing import Any
from multiprocessing import Process, Value

def task(counter: Any):
    for _ in range(1000):
        with counter.get_lock():
            counter.value += 1


counter = Value("i", 0, lock=True)

if __name__ == "__main__":
    p1 = Process(target=task, args=(counter,))
    p2 = Process(target=task, args=(counter,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(counter.value)
