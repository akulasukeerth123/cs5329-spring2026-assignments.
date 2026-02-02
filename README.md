# Activity 2.1 – Recurrence Experimentation and Analysis

**Course:** CS 5329 – Algorithm Design and Analysis  
**Student Name:** Akula Sukeerth Net ID (xob17)
**Semester:** Spring 2026

---


## Overview
This assignment compares a naive recursive Fibonacci implementation with a dynamic
programming (memoized) Fibonacci implementation to observe performance differences as
input size grows.

---

## How to Run the Code
From the repository directory, run:

```bash
python assignment2_fibonacci.py

## Sample Output

n=10: fib_recursive -> 55 (time 0.0001s), fib_dp -> 55 (time 0.0000s)
n=20: fib_recursive -> 6765 (time 0.0013s), fib_dp -> 6765 (time 0.0000s)
n=30: fib_recursive -> 832040 (time 0.1420s), fib_dp -> 832040 (time 0.0001s)
n=35: fib_recursive -> 9227465 (time 1.5124s), fib_dp -> 9227465 (time 0.0001s)

## Analysis Questions and Answers

### a. Why does `fib_recursive` slow down so dramatically as n increases?
`fib_recursive` repeatedly recomputes the same Fibonacci values. Each function call makes two more recursive calls, which creates many overlapping subproblems. As n increases, the number of function calls grows exponentially, causing the runtime to increase very rapidly.

### b. What is the Big-O time complexity of each approach?
- **`fib_recursive`** has exponential time complexity, approximately **O(φ^n)** (often written as **O(2^n)**).
- **`fib_dp`** (dynamic programming) has linear time complexity, **O(n)**, because each Fibonacci value is computed only once.

### c. Would `fib_recursive(50)` be feasible? Explain your reasoning.
No, `fib_recursive(50)` is not feasible. The exponential number of recursive calls would make the program take an extremely long time to finish. This is why large input values should only be tested using the dynamic programming approach.

### d. How does memoization change the nature of the recurrence?
Memoization stores the result of each subproblem the first time it is computed and reuses it for future calls. This eliminates repeated calculations and transforms the recurrence from exponential growth into linear growth, since each Fibonacci value is computed only once.

