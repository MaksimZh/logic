from random import randint
from multiprocessing import Pool

SIZE = 1000000
CHUNK = 100000
THREADS = 4

if __name__ == "__main__":
    numbers = [randint(0, 100) for _ in range(SIZE)]

    n_full_chunks = SIZE // CHUNK
    tail_size = SIZE % CHUNK
    chunks = \
        [numbers[i * CHUNK: (i + 1) * CHUNK] for i in range(n_full_chunks)] + \
        ([numbers[-tail_size:]] if tail_size else [])

    with Pool(processes=THREADS) as pool:
        total = sum(pool.map_async(sum, chunks).get())
    print("Sum of all elements:", total)
