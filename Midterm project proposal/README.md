# Real-Time Leaderboard Ranking Using Heap Structures

Student: Sukeerth Akula , Shivani Guda 
Course: CS 5329 – Algorithm Design and Analysis  
Semester: Spring 2026  

---

## Leaderboard Ranking Algorithm Comparison

### Project Overview  
This project evaluates two different approaches for solving the Top-K ranking problem in large datasets. The goal is to compare a simple baseline sorting algorithm with a more advanced optimized algorithm using a min-heap (priority queue). The system processes synthetic datasets of up to 100,000+ records and measures both runtime performance and memory usage. This project simulates real-world systems like YouTube trending, gaming leaderboards, and recommendation engines.

---

## Algorithms Implemented  

### 1. Baseline Full Sorting  
The baseline approach sorts the entire dataset based on an engagement score and selects the top K elements.  

Score Formula:  
score = views + 2 * likes + 3 * comment_count  

Complexity:  
Time Complexity: O(n log n)  
Space Complexity: O(n)  

Advantages:  
Simple implementation  
Works well for small datasets  

Limitations:  
Requires sorting the entire dataset  
Not suitable for large-scale or real-time systems  

---

### 2. Optimized Min-Heap Approach  
The optimized algorithm uses a min-heap of size K to track only the top K elements while scanning the dataset. This allows efficient ranking without sorting the entire dataset.  

Data Structures Used:  
Min-Heap (priority queue)  

Complexity:  
Time Complexity: O(n log k)  
Space Complexity: O(k)  

Advantages:  
Efficient for Top-K queries  
Faster for large datasets  
Low memory usage  
Suitable for real-time systems  

Trade-off:  
Slightly more complex implementation  

---

## Dataset  

The project uses a synthetic dataset generated using Python.  

Fields included:  
title  
views  
likes  
comment_count  

Dataset sizes tested:  
10,000  
50,000  
100,000 records  

---

## Performance Evaluation  

Benchmark experiments were conducted using:  
time.perf_counter() for runtime measurement  
tracemalloc for memory usage evaluation  

---

## Runtime Results  

Dataset Size    Baseline Runtime    Optimized Runtime  
10k             0.001854            0.000680  
50k             0.005784            0.002065  
100k            0.012792            0.003801  

---

## Memory Usage  

Dataset Size    Baseline Memory     Optimized Memory  
10k             0.2290	            0.0003 
50k             1.1444	            0.0003 
100k            2.2886 	            0.0003

---  

## Performance Visualization  

results/performance_graph.png  

This graph shows how the heap-based approach scales better than sorting as dataset size increases.  

---

## How to Run the Project  

Navigate to the project directory and run:  

Generate Dataset  
python src/generate_large_dataset.py  

Run Benchmark  
python src/benchmark.py  

---

## Project Structure  

leaderboard-ranking-project  

src  
baseline_sorting.py  
heap_leaderboard.py  
evaluation.py  
benchmark.py  
generate_large_dataset.py  

data  
sample_leaderboard_dataset.csv  
dataset_*.csv  

results  
performance_graph.png  

README.md  

---

## Key Takeaways  

The baseline sorting algorithm works well for small datasets but becomes inefficient as data grows.  
The heap-based approach significantly improves performance by focusing only on the top K elements.  
Memory usage is reduced since only K elements are stored.  
The optimized approach is ideal for real-time ranking systems.  

---

## Author  

Sukeerth Akula & Shivani Guda 
CS 5329 – Algorithm Design and Analysis  