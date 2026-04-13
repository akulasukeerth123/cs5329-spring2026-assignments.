import json
import os
import random
import time
import subprocess
import sys


TEST_CASES_DIR = "test_cases"
RESULTS_DIR = "results"


def ensure_dirs():
    os.makedirs(TEST_CASES_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def make_task(task_id, start, end, weight, resource, category):
    return {
        "id": task_id,
        "start": start,
        "end": end,
        "weight": round(weight, 2),
        "resource": resource,
        "category": category
    }


def sparse_scenario(n=10):
    tasks = []
    current = 0
    cats = ["compute", "io", "network"]
    for i in range(n):
        duration = random.randint(1, 3)
        gap = random.randint(1, 2)
        start = current
        end = start + duration
        current = end + gap
        tasks.append(make_task(
            i, start, end,
            random.uniform(8, 30),
            random.randint(1, 3),
            random.choice(cats)
        ))
    return {
        "resource_capacity": 10,
        "category_limit": 3,
        "tasks": tasks
    }


def dense_scenario(n=10):
    tasks = []
    cats = ["compute", "io", "network"]
    for i in range(n):
        start = random.randint(0, 10)
        end = random.randint(start + 1, min(15, start + 6))
        tasks.append(make_task(
            i, start, end,
            random.uniform(10, 80),
            random.randint(2, 6),
            random.choice(cats)
        ))
    return {
        "resource_capacity": 7,
        "category_limit": 2,
        "tasks": tasks
    }


def category_heavy_scenario(n=10):
    tasks = []
    for i in range(n):
        category = "compute" if i < int(0.8 * n) else random.choice(["io", "network"])
        start = random.randint(0, 12)
        end = random.randint(start + 1, min(16, start + 5))
        tasks.append(make_task(
            i, start, end,
            random.uniform(8, 70),
            random.randint(1, 4),
            category
        ))
    return {
        "resource_capacity": 9,
        "category_limit": 1,
        "tasks": tasks
    }


def adversarial_scenario():
    tasks = [
        make_task(0, 0, 10, 95, 5, "compute"),
        make_task(1, 0, 3, 25, 2, "io"),
        make_task(2, 3, 6, 25, 2, "io"),
        make_task(3, 6, 10, 25, 2, "io"),
        make_task(4, 0, 5, 30, 3, "network"),
        make_task(5, 5, 10, 30, 3, "network"),
        make_task(6, 1, 4, 18, 1, "compute"),
        make_task(7, 4, 8, 18, 1, "compute"),
        make_task(8, 8, 10, 10, 1, "compute"),
        make_task(9, 2, 9, 60, 4, "io")
    ]
    return {
        "resource_capacity": 5,
        "category_limit": 2,
        "tasks": tasks
    }


def benchmark_case(n):
    tasks = []
    cats = ["compute", "io", "network"]
    for i in range(n):
        start = random.randint(0, 100)
        end = random.randint(start + 1, min(120, start + 12))
        tasks.append(make_task(
            i, start, end,
            random.uniform(5, 100),
            random.randint(1, 5),
            random.choice(cats)
        ))
    return {
        "resource_capacity": 10,
        "category_limit": 2,
        "tasks": tasks
    }


def run_scheduler(input_path, strategy, output_path):
    cmd = [
        sys.executable,
        "scheduler.py",
        "--input", input_path,
        "--strategy", strategy,
        "--output", output_path
    ]
    start = time.perf_counter()
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    end = time.perf_counter()
    return round(end - start, 6)


def read_total_weight(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["total_weight"]


def generate_quality_table(small_cases):
    rows = []
    for case_name in small_cases:
        input_path = os.path.join(TEST_CASES_DIR, case_name)

        bf_output = os.path.join(RESULTS_DIR, f"{case_name[:-5]}_bruteforce.json")
        g1_output = os.path.join(RESULTS_DIR, f"{case_name[:-5]}_g1.json")
        g2_output = os.path.join(RESULTS_DIR, f"{case_name[:-5]}_g2.json")

        run_scheduler(input_path, "bruteforce", bf_output)
        run_scheduler(input_path, "earliest_finish_resource_aware", g1_output)
        run_scheduler(input_path, "weight_to_resource_ratio", g2_output)

        optimal = read_total_weight(bf_output)
        g1 = read_total_weight(g1_output)
        g2 = read_total_weight(g2_output)

        g1_pct = 0.0 if optimal == 0 else round((g1 / optimal) * 100, 2)
        g2_pct = 0.0 if optimal == 0 else round((g2 / optimal) * 100, 2)

        rows.append({
            "case": case_name,
            "optimal_weight": optimal,
            "g1_weight": g1,
            "g1_percent_of_optimal": g1_pct,
            "g2_weight": g2,
            "g2_percent_of_optimal": g2_pct
        })
    return rows


def generate_timing_table(sizes):
    rows = []
    for n in sizes:
        case_name = f"benchmark_{n}.json"
        input_path = os.path.join(TEST_CASES_DIR, case_name)

        g1_output = os.path.join(RESULTS_DIR, f"benchmark_{n}_g1.json")
        g2_output = os.path.join(RESULTS_DIR, f"benchmark_{n}_g2.json")

        g1_time = run_scheduler(input_path, "earliest_finish_resource_aware", g1_output)
        g2_time = run_scheduler(input_path, "weight_to_resource_ratio", g2_output)

        row = {
            "input_size": n,
            "earliest_finish_resource_aware_seconds": g1_time,
            "weight_to_resource_ratio_seconds": g2_time
        }

        if n <= 10:
            bf_output = os.path.join(RESULTS_DIR, f"benchmark_{n}_bruteforce.json")
            bf_time = run_scheduler(input_path, "bruteforce", bf_output)
            row["bruteforce_seconds"] = bf_time
        else:
            row["bruteforce_seconds"] = "N/A (n > 15)"

        rows.append(row)
    return rows


def generate_ascii_chart(timing_rows):
    lines = []
    lines.append("Timing Chart (smaller bar = faster)")
    lines.append("")

    for row in timing_rows:
        n = row["input_size"]
        g1 = row["earliest_finish_resource_aware_seconds"]
        g2 = row["weight_to_resource_ratio_seconds"]

        g1_bar = "#" * max(1, int(g1 * 100))
        g2_bar = "#" * max(1, int(g2 * 100))

        lines.append(f"n={n}")
        lines.append(f"  G1 {g1:>8} sec | {g1_bar}")
        lines.append(f"  G2 {g2:>8} sec | {g2_bar}")
        lines.append("")

    return "\n".join(lines)


def main():
    random.seed(42)
    ensure_dirs()

    scenario_files = {
        "sparse_10.json": sparse_scenario(10),
        "dense_10.json": dense_scenario(10),
        "category_heavy_10.json": category_heavy_scenario(10),
        "adversarial_10.json": adversarial_scenario(),
        "benchmark_10.json": benchmark_case(10),
        "benchmark_50.json": benchmark_case(50),
        "benchmark_100.json": benchmark_case(100),
        "benchmark_500.json": benchmark_case(500),
        "benchmark_1000.json": benchmark_case(1000)
    }

    for filename, data in scenario_files.items():
        save_json(os.path.join(TEST_CASES_DIR, filename), data)

    small_cases = [
        "sparse_10.json",
        "dense_10.json",
        "category_heavy_10.json",
        "adversarial_10.json",
        "benchmark_10.json"
    ]

    quality_rows = generate_quality_table(small_cases)
    timing_rows = generate_timing_table([10, 50, 100, 500, 1000])

    save_json(os.path.join(RESULTS_DIR, "quality_comparison.json"), quality_rows)
    save_json(os.path.join(RESULTS_DIR, "timing_comparison.json"), timing_rows)

    chart_text = generate_ascii_chart(timing_rows)
    with open(os.path.join(RESULTS_DIR, "timing_chart.txt"), "w", encoding="utf-8") as f:
        f.write(chart_text)

    print("All test cases and benchmark results generated successfully.")


if __name__ == "__main__":
    main()