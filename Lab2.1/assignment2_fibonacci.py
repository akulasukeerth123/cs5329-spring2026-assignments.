import time

def fib_recursive(n):
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

fib_memo = {0: 0, 1: 1}

def fib_dp(n):
    if n in fib_memo:
        return fib_memo[n]
    fib_memo[n] = fib_dp(n - 1) + fib_dp(n - 2)
    return fib_memo[n]

if __name__ == "__main__":
    test_values = [10, 20, 30, 35]

    for n in test_values:
        start = time.time()
        res1 = fib_recursive(n)
        t1 = time.time() - start

        start = time.time()
        res2 = fib_dp(n)
        t2 = time.time() - start

        print(
            f"n={n}: fib_recursive -> {res1} (time {t1:.4f}s), "
            f"fib_dp -> {res2} (time {t2:.4f}s)"
        )
