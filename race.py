from threading import Thread, Lock
from time import sleep


def race() -> int:
    counter = 0
    lock = Lock()  # +++
    num_of_threads = 10

    def inc():
        nonlocal counter
        for _ in range(1000):
            lock.acquire()  # +++
            tmp = counter
            sleep(1e-6)
            counter = tmp + 1
            lock.release()  # +++
    
    threads = tuple(
        Thread(target = inc)
        for _ in range(num_of_threads))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return counter


def deadlock():

    lock1 = Lock()
    lock2 = Lock()

    def a():
        lock1.acquire()
        lock2.acquire()  # +++
        print("a: 1")
        sleep(1e-2)
        #lock2.acquire()  # ---
        print("a: 2")
        lock2.release()
        lock1.release()

    def b():
        lock1.acquire()  # +++
        lock2.acquire()
        print("b: 2")
        sleep(1e-2)
        #lock1.acquire()  # ---
        print("b: 1")
        lock2.release()  # +++
        lock1.release()
        #lock2.release()  # ---

    thread1 = Thread(target=a)
    thread1.start()
    thread2 = Thread(target=b)
    thread2.start()

    thread1.join()
    thread2.join()

print(race())
deadlock()
