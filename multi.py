from typing import Any, Optional
from multiprocessing import Process, Array, Barrier, Value, Semaphore, Event, \
    Pool
from concurrent.futures import ProcessPoolExecutor, as_completed
from time import sleep


def barrier_f(a: Any, i: int, bar: Optional[Any]):
    for _ in range(100):
        a[i] += 1
    if bar:
        # Sum after all increments
        bar.wait()
    x = sum(a)
    if bar:
        # Assign after all sums
        bar.wait()
    # All array elements are equal if no racing happens
    a[i] = x

def barrier(n: int, race: bool = False):
    print(f"barrier: race={race}")
    a = Array("i", [0] * n)
    bar = None if race else Barrier(n)
    pool = [Process(target=barrier_f, args=(a, i, bar)) for i in range(n)]
    for p in pool:
        p.start()
    for p in pool:
        p.join()
    print(a[:])


def semaphore_f(v: Any, m: Any, sem: Optional[Any]):
    if sem:
        # Limit number of working processes
        sem.acquire()
    for _ in range(100):
        with v.get_lock():
            v.value += 1
        sleep(1e-4)
    # Store maximal value
    # It will be less or equal than 100 * number of working processes
    with v.get_lock():
        with m.get_lock():
            if v.value > m.value:
                m.value = v.value
    # Undo increment
    with v.get_lock():
        v.value -= 100
    if sem:
        sem.release()


def semaphore(n: int, race: bool = False):
    print(f"semaphore: race={race}")
    v = Value("i", 0, lock=True)
    m = Value("i", 0, lock=True)
    sem = None if race else Semaphore(2)
    pool = [Process(target=semaphore_f, args=(v, m, sem)) for _ in range(n)]
    for p in pool:
        p.start()
    for p in pool:
        p.join()
    print(m.value)


def event_inc(v: Any, m: Any, ev: Optional[Any]):
    for _ in range(100):
        with v.get_lock():
            v.value += 1
        sleep(1e-4)
    # Store final value
    # It is 100 if no decrement happens
    m.value = v.value
    if ev:
        # Release decrement
        ev.set()

def event_dec(v: Any, m: Any, ev: Optional[Any]):
    if ev:
        # Wait for increment finish
        ev.wait()
    for _ in range(100):
        with v.get_lock():
            v.value -= 1
        sleep(1e-4)


def event(race: bool = False):
    print(f"event: race={race}")
    v = Value("i", 0, lock=True)
    m = Value("i", 0, lock=True)
    ev = None if race else Event()
    pool = [
        Process(target=event_inc, args=(v, m, ev)),
        Process(target=event_dec, args=(v, m, ev)),
    ]
    for p in pool:
        p.start()
    for p in pool:
        p.join()
    print(m.value)


race_value = Value("i", 0)


def race_inc():
    # Initiate race on shared value increment
    # to ensure that futures are calculated concurrently
    for _ in range(100):
        race_value.value += 1
        sleep(1e-4)
    return race_value.value


def futures(n: int):
    print("futures:")
    race_value.value = 0
    with ProcessPoolExecutor() as executor:
        pool = [executor.submit(race_inc) for _ in range(n)]
        print([v.result() for v in as_completed(pool)])


def tasks(n: int):
    print(f"tasks: n={n}")
    race_value.value = 0
    with Pool(processes=n) as pool:
        # Increments race in parallel or performed subsequently
        # depending on the maximal number of processes
        # the results in theese cases are different
        tasks = [pool.apply_async(race_inc) for _ in range(10)]
        print([t.get() for t in tasks])


if __name__ == "__main__":
    print()
    barrier(10)
    barrier(10, race=True)

    print()
    semaphore(10)
    semaphore(10, race=True)

    print()
    event()
    event(race=True)

    print()
    futures(10)

    print()
    tasks(1)
    tasks(10)
