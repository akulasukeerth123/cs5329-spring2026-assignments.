# Analysis and Reflection

## Part 1: Greedy Strategy Justifications

### Strategy 1: Earliest Finish Time with Resource-Aware Filtering

My first greedy strategy sorts tasks by earliest finish time and then adds a task only if doing so keeps the schedule valid. The main greedy idea behind this strategy is that tasks that finish earlier usually leave more room for future tasks. This is based on the same intuition as the classic interval scheduling problem, where choosing an early-finishing activity can preserve future scheduling options.

In this project, I could not use earliest finish time alone because the problem has extra constraints. Even if two tasks do not cause a direct time conflict, they may still violate the total resource capacity or the category overlap limit. Because of that, I added a validation step before accepting any task. A task is selected only if it keeps the schedule valid in terms of time overlap, resource usage, and category count.

This strategy works well when tasks are more spread out and when preserving flexibility is more important than choosing the heaviest task immediately. It performed very well in my experiments and matched the brute-force optimal result in the sparse case, the dense case, and the adversarial case.

However, this strategy is not always optimal. It can fail when a task that finishes early has lower value than a task or combination of tasks that finish later. It also may miss the best result when the category constraint changes which later tasks remain possible. In my results, this strategy missed the optimum in the category-heavy case and in the identical-edge case.

### Strategy 2: Highest Weight-to-Resource Ratio with Compatibility Checking

My second greedy strategy sorts tasks by weight-to-resource ratio. The goal is to prioritize tasks that give the most value for each unit of resource consumed. Since the assignment includes a strict resource-capacity constraint, this is a reasonable greedy rule because it tries to use the available capacity efficiently.

Like the first strategy, this method also requires a schedule validity check before adding a task. A task may look attractive based on its ratio, but it still cannot be selected if it causes the total overlapping resource usage to go above the capacity or if it causes too many overlapping tasks from the same category. Because of that, the strategy combines a greedy ordering rule with full constraint checking.

This strategy works well when resource competition is the main challenge and when selecting more efficient tasks leads to a stronger overall schedule. In my validation tests, it performed well in the sparse case and matched the optimal result in the category-heavy case. It also came very close to the optimum in the dense case.

Its weakness is that it focuses on local efficiency and does not fully account for how a selected task may block better combinations later. It also does not directly consider how long the task occupies the timeline. This was clear in my adversarial case, where the strategy achieved only 30.00% of the optimal result. That shows it can make a locally attractive decision that is globally poor.

## Part 2: Brute-Force Baseline

I implemented a brute-force baseline for small inputs where `n <= 15`. This solver checks every possible subset of tasks and then tests whether that subset is valid. A subset is valid only if it satisfies all assignment constraints:

1. The total resource usage at every overlapping time segment must not exceed the resource capacity.
2. The number of overlapping tasks from the same category must not exceed the category limit.
3. Tasks are fully selected or not selected at all, which matches the no-preemption requirement.

After checking all possible subsets, the brute-force solver returns the valid subset with the highest total weight. Since it explores every possible combination, it gives the true optimal solution for small cases. This makes it a good baseline for measuring how well the greedy strategies perform.

I used this brute-force solver to validate both greedy strategies on five small test cases. These cases were chosen to represent different scheduling conditions: sparse, dense, category-heavy, adversarial, and an identical-parameter edge case.

## Part 2: Validation Results

| Case | Brute Force | Greedy 1 | Greedy 2 | G1 % of Optimal | G2 % of Optimal |
|------|-------------|----------|----------|-----------------|-----------------|
| case1_sparse | 57.0 | 57.0 | 57.0 | 100.00% | 100.00% |
| case2_dense | 82.0 | 82.0 | 81.0 | 100.00% | 98.78% |
| case3_category_heavy | 56.0 | 54.0 | 56.0 | 96.43% | 100.00% |
| case4_adversarial | 60.0 | 60.0 | 18.0 | 100.00% | 30.00% |
| case5_identical_edge | 38.0 | 34.0 | 34.0 | 89.47% | 89.47% |

From these five validation cases, Greedy Strategy 1 was optimal in 3 out of 5 cases, while Greedy Strategy 2 was optimal in 2 out of 5 cases. Strategy 1 performed especially well in the sparse, dense, and adversarial cases. Strategy 2 performed well in the sparse and category-heavy cases, and it was very close to optimal in the dense case. However, Strategy 2 struggled badly in the adversarial case, where it reached only 30.00% of the optimal result. Both greedy strategies also missed the optimum in the identical-edge case.

These results show that both greedy strategies can work well, but neither one is always optimal. Greedy Strategy 1 was more consistent overall, while Greedy Strategy 2 showed stronger sensitivity to adversarial input. The brute-force baseline was useful because it gave a reliable optimal benchmark for comparing both greedy methods.

## Part 3: Benchmarking and Analysis

### Test Scenarios

I created the following four required test scenarios:

1. **Sparse scenario**  
   This case has fewer conflicts and enough resource capacity, so greedy strategies are expected to perform well.

2. **Dense scenario**  
   This case has many overlapping tasks and tighter resource limits, making the scheduling decisions more difficult.

3. **Category-heavy scenario**  
   Most tasks belong to the same category and the category limit is small, which highlights the effect of the category constraint.

4. **Adversarial scenario**  
   This case was intentionally designed to make one greedy strategy perform poorly and show that greedy decisions are not always optimal.

### Benchmarking Table

| Input Size | Earliest Finish | Weight/Resource Ratio | Brute Force |
|-----------|-----------------|-----------------------|-------------|
| 10        | Measured        | Measured              | Measured    |
| 50        | Measured        | Measured              | N/A         |
| 100       | Measured        | Measured              | N/A         |
| 500       | Measured        | Measured              | N/A         |
| 1000      | Measured        | Measured              | N/A         |

The timing results are saved in:
- `results/timing_comparison.json`
- `results/timing_chart.txt`

The quality comparison against the brute-force baseline is saved in:
- `results/quality_comparison.json`

### Written Analysis

Based on my validation results, the earliest-finish strategy performed better overall because it matched the optimal result in more cases and was more stable across different inputs. It worked especially well in the sparse case and the dense case, where preserving future flexibility helped the algorithm make strong scheduling decisions. It also handled the adversarial case very well.

The weight-to-resource-ratio strategy was strongest when resource efficiency mattered more. It matched the optimum in the category-heavy case and came very close in the dense case. This suggests that the strategy can be effective when capacity is tight and selecting efficient tasks is more important than preserving time flexibility.

At the same time, each strategy had clear weaknesses. The earliest-finish strategy missed the optimum in the category-heavy and identical-edge cases. The weight-to-resource-ratio strategy had its biggest failure in the adversarial case, where it achieved only 30.00% of optimal. This happened because a task that looked good locally based on ratio prevented a better overall combination.

The category constraint made the problem harder because it introduced another form of conflict beyond time and resource usage. Even when the total resource capacity was still available, a schedule could become invalid because too many overlapping tasks belonged to the same category. This shows why the problem is more complex than standard interval scheduling.

## Part 4: Reflection

This problem cannot generally be solved optimally by a single greedy strategy because the decision at one step can affect many later choices in different ways. A task that looks best at the moment may use too much resource capacity, block better future tasks, or create category conflicts later. Because of these interactions, the greedy-choice property does not hold for the problem in general.

For a greedy method to always be optimal, the problem would need a stronger structure where one locally best choice can always be extended to a globally optimal schedule. That is true for some simpler problems, such as classic interval scheduling, but it is not true here because of the added weight, resource, and category constraints.

If I were solving this problem in a production environment, I would still use greedy strategies because they are fast and practical for large inputs. However, I would combine them with a stronger optimization method when better solution quality is required. For example, I might use branch-and-bound, dynamic programming for restricted cases, or integer linear programming for exact optimization. In practice, greedy would be a fast heuristic, while a stronger method would be used when accuracy matters more.