import sys
import platform

def fib_number(n):
    # Iterative Fibonacci (faster + looks different from recursive)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def show_env_details():
    print("Hello, Algorithms!")
    print("Python Version:", sys.version)
    print(f"Operating System: {platform.system()} {platform.release()}")


if __name__ == "__main__":
    show_env_details()

    position = 10
    result = fib_number(position)
    print(f"The {position}th Fibonacci number is: {result}")
