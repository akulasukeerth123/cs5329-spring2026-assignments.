import json
import time
import argparse
import itertools
from collections import defaultdict
from typing import List, Dict, Any


def load_json(path: str) -> Dict[str, Any]:
    # read input file
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Dict[str, Any]) -> None:
    # save output file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def check_task(task: Dict[str, Any]) -> None:
    required = ["id", "start", "end", "weight", "resource", "category"]
    for key in required:
        if key not in task:
            raise ValueError(f"Missing task field: {key}")

    if not isinstance(task["start"], int) or not isinstance(task["end"], int):
        raise ValueError("start and end must be integers")
    if task["start"] < 0 or task["start"] >= task["end"]:
        raise ValueError("Task must satisfy 0 <= start < end")
    if not (0.0 < float(task["weight"]) <= 100.0):
        raise ValueError("weight must satisfy 0.0 < weight <= 100.0")
    if int(task["resource"]) < 1:
        raise ValueError("resource must be at least 1")
    if not isinstance(task["category"], str):
        raise ValueError("category must be a string")


def check_input(data: Dict[str, Any]) -> None:
    if "resource_capacity" not in data or "category_limit" not in data or "tasks" not in data:
        raise ValueError("Input JSON must contain resource_capacity, category_limit, and tasks")

    if not isinstance(data["resource_capacity"], int) or data["resource_capacity"] < 1:
        raise ValueError("resource_capacity must be an integer >= 1")

    if not isinstance(data["category_limit"], int) or data["category_limit"] < 1:
        raise ValueError("category_limit must be an integer >= 1")

    if not isinstance(data["tasks"], list):
        raise ValueError("tasks must be a list")

    seen_ids = set()
    for task in data["tasks"]:
        check_task(task)
        if task["id"] in seen_ids:
            raise ValueError(f"Duplicate task id found: {task['id']}")
        seen_ids.add(task["id"])


def is_active(task: Dict[str, Any], t: int) -> bool:
    return task["start"] <= t < task["end"]


def get_time_points(tasks: List[Dict[str, Any]]) -> List[int]:
    time_points = set()
    for task in tasks:
        time_points.add(task["start"])
        time_points.add(task["end"])
    return sorted(time_points)


def make_timeline(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    timeline = {}
    if not tasks:
        return timeline

    time_points = get_time_points(tasks)
    for i in range(len(time_points) - 1):
        seg_start = time_points[i]
        seg_end = time_points[i + 1]
        active_tasks = [task for task in tasks if is_active(task, seg_start)]

        if active_tasks:
            category_counts = defaultdict(int)
            resource_used = 0

            for task in active_tasks:
                resource_used += task["resource"]
                category_counts[task["category"]] += 1

            timeline[f"{seg_start}-{seg_end}"] = {
                "resource_used": resource_used,
                "categories": dict(category_counts)
            }

    return timeline


def is_valid_schedule(tasks: List[Dict[str, Any]], resource_capacity: int, category_limit: int) -> bool:
    if not tasks:
        return True

    time_points = get_time_points(tasks)
    if len(time_points) <= 1:
        return True

    for i in range(len(time_points) - 1):
        seg_start = time_points[i]
        active_tasks = [task for task in tasks if is_active(task, seg_start)]

        total_resource = sum(task["resource"] for task in active_tasks)
        if total_resource > resource_capacity:
            return False

        category_counts = defaultdict(int)
        for task in active_tasks:
            category_counts[task["category"]] += 1

        for count in category_counts.values():
            if count > category_limit:
                return False

    return True


def can_add(chosen: List[Dict[str, Any]], task: Dict[str, Any], resource_capacity: int, category_limit: int) -> bool:
    return is_valid_schedule(chosen + [task], resource_capacity, category_limit)


def get_total_weight(tasks: List[Dict[str, Any]]) -> float:
    return round(sum(float(task["weight"]) for task in tasks), 4)


def greedy_earliest_finish_resource_aware(
    tasks: List[Dict[str, Any]],
    resource_capacity: int,
    category_limit: int
) -> List[Dict[str, Any]]:
    sorted_tasks = sorted(
        tasks,
        key=lambda x: (x["end"], x["start"], x["resource"], -x["weight"], x["id"])
    )

    chosen = []
    for task in sorted_tasks:
        if can_add(chosen, task, resource_capacity, category_limit):
            chosen.append(task)

    return chosen


def greedy_weight_to_resource(
    tasks: List[Dict[str, Any]],
    resource_capacity: int,
    category_limit: int
) -> List[Dict[str, Any]]:
    sorted_tasks = sorted(
        tasks,
        key=lambda x: (
            -(x["weight"] / x["resource"]),
            -x["weight"],
            x["end"],
            x["start"],
            x["id"]
        )
    )

    chosen = []
    for task in sorted_tasks:
        if can_add(chosen, task, resource_capacity, category_limit):
            chosen.append(task)

    return chosen


def brute_force_solver(
    tasks: List[Dict[str, Any]],
    resource_capacity: int,
    category_limit: int
) -> List[Dict[str, Any]]:
    # try all subsets for small cases
    n = len(tasks)
    if n > 15:
        raise ValueError("Brute-force solver only supports n <= 15")

    best_subset = []
    best_weight = -1.0

    for r in range(n + 1):
        for subset in itertools.combinations(tasks, r):
            subset = list(subset)
            if is_valid_schedule(subset, resource_capacity, category_limit):
                weight = get_total_weight(subset)
                if weight > best_weight:
                    best_weight = weight
                    best_subset = subset

    return best_subset


def run_strategy(data: Dict[str, Any], strategy_name: str) -> Dict[str, Any]:
    check_input(data)

    resource_capacity = data["resource_capacity"]
    category_limit = data["category_limit"]
    tasks = data["tasks"]

    start_time = time.perf_counter()

    if strategy_name == "earliest_finish_resource_aware":
        chosen = greedy_earliest_finish_resource_aware(tasks, resource_capacity, category_limit)
    elif strategy_name == "weight_to_resource_ratio":
        chosen = greedy_weight_to_resource(tasks, resource_capacity, category_limit)
    elif strategy_name == "bruteforce":
        chosen = brute_force_solver(tasks, resource_capacity, category_limit)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    end_time = time.perf_counter()

    result = {
        "strategy_name": strategy_name,
        "selected_tasks": [task["id"] for task in chosen],
        "total_weight": get_total_weight(chosen),
        "execution_time_seconds": round(end_time - start_time, 6),
        "utilization_timeline": make_timeline(chosen),
        "schedule_valid": is_valid_schedule(chosen, resource_capacity, category_limit)
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-constraint greedy scheduler")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument(
        "--strategy",
        required=True,
        choices=[
            "earliest_finish_resource_aware",
            "weight_to_resource_ratio",
            "bruteforce"
        ],
        help="Strategy name"
    )
    parser.add_argument("--output", required=True, help="Path to save output JSON")

    args = parser.parse_args()

    data = load_json(args.input)
    result = run_strategy(data, args.strategy)

    print(json.dumps(result, indent=2))
    save_json(args.output, result)


if __name__ == "__main__":
    main()