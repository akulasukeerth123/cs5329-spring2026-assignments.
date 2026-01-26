# Linear Search vs Binary Search Performance Comparison

## Overview
This project compares the performance of **Linear Search** and **Binary Search** algorithms using Python.  
The program measures and prints the **average execution time** for each search method across different input sizes.

This experiment helps demonstrate why algorithmic efficiency matters:
- **Linear Search → O(n)** (slower for large lists)
- **Binary Search → O(log n)** (much faster, but requires sorted data)

---

## Files Included
- `linear_vs_binary_search.py` → Main Python script that runs the comparison.

---

## Requirements
- Python 3.x

No external libraries are required (only built-in modules).

---

## How It Works
1. The program creates sorted lists of different sizes.
2. It searches for the **last element** in the list (worst case for linear search).
3. Each search is repeated many times (`runs = 1000`).
4. The program calculates and prints:
   - Linear Search average time
   - Binary Search average time

Timing is done using `time.perf_counter()` for high precision.

---

## How to Run
Open a terminal and run:

```bash
python linear_vs_binary_search.py
