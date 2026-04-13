import csv
import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.baseline_sorting import get_top_k_baseline
from src.heap_leaderboard import get_top_k_heap
from src.evaluation import measure_performance, check_correctness


def load_data(csv_file):
    data = []
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            try:
                views = int(row.get('views', 0))
                likes = int(row.get('likes', 0))
                comments = int(row.get('comment_count', 0))
            except:
                views, likes, comments = 0, 0, 0

            score = views + 2 * likes + 3 * comments

            data.append({
                "id": i,
                "title": row.get('title', ''),
                "score": score
            })

    return data


def run_benchmark(csv_file, k):
    print("Loading dataset...")
    data = load_data(csv_file)

    print(f"\nRunning Top-{k} comparison...\n")

    baseline = measure_performance(get_top_k_baseline, data, k)
    heap = measure_performance(get_top_k_heap, data, k)

    correct = check_correctness(baseline["result"], heap["result"])

    print("=== RESULTS ===")
    print(f"Baseline Time: {baseline['time']:.6f} sec")
    print(f"Heap Time: {heap['time']:.6f} sec")
    print(f"Baseline Memory: {baseline['memory']:.4f} MB")
    print(f"Heap Memory: {heap['memory']:.4f} MB")
    print(f"Correctness Match: {correct}")

    if heap['time'] > 0:
        print(f"Speedup: {baseline['time'] / heap['time']:.2f}x")

    print("\nTop Results:")
    for item in heap["result"][:5]:
        print(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--k", type=int, default=10)

    args = parser.parse_args()

    run_benchmark(args.csv, args.k)