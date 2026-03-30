import time
import tracemalloc

def measure_performance(func, data, k):
    """
    Measures runtime and memory usage
    """
    tracemalloc.start()

    start_time = time.perf_counter()
    result = func(data, k)
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "result": result,
        "time": end_time - start_time,
        "memory": peak / (1024 * 1024)  # MB
    }


def check_correctness(result1, result2):
    """
    Checks if both approaches return same Top-K IDs
    """
    ids1 = [item['id'] for item in result1]
    ids2 = [item['id'] for item in result2]

    return set(ids1) == set(ids2)