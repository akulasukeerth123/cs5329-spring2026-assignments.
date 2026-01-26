import time
import bisect

def linear_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

def binary_search(arr, x):
    pos = bisect.bisect_left(arr, x)
    if pos != len(arr) and arr[pos] == x:
        return pos
    return -1

def run_test():
    sizes = [10_000, 50_000, 100_000, 200_000]
    runs = 1000

    for n in sizes:
        arr = list(range(n))
        target = n - 1  # worst case

        start = time.perf_counter()
        for _ in range(runs):
            linear_search(arr, target)
        linear_total = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(runs):
            binary_search(arr, target)
        binary_total = time.perf_counter() - start

        print(f"\nArray Size: {n}")
        print(f"Linear Search Avg Time : {linear_total / runs:.8f} seconds")
        print(f"Binary Search Avg Time : {binary_total / runs:.8f} seconds")

if __name__ == "__main__":
    run_test()
