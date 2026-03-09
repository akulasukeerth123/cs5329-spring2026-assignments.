# CS 5329 – Midterm Project Proposal

**Student Name:** Shivani Guda, Sukeerth Akula
**NetID:** epb44, xob17

**Project Title:** Real-Time Leaderboard Ranking Using Heap Structures



# 1. Problem Statement

### Input

The input for this project will be a dataset representing a leaderboard of videos or users with engagement scores. Each record will contain fields such as video ID (or player ID), number of views, likes, comments, and an overall engagement score. The dataset will be stored in **CSV format** and initially contain around **100,000 records**. Larger datasets of **500,000 to 1,000,000 records** may also be generated to evaluate performance at scale.

The data will be loaded from a file and processed by the algorithm to maintain a ranking of the top-performing entries.



### Output

The program will return the **Top K ranked entries** (for example Top 50 videos or players) based on their engagement score.

A correct result means both the baseline algorithm and the optimized algorithm return the **same Top K ranked results** for the same dataset.


### Constraints

The main objective of the project is to support **fast ranking updates on large datasets**.

Performance goals include:

* Efficient ranking updates even with **hundreds of thousands of records**
* Query time ideally **less than 10 milliseconds**
* Memory usage should remain **below 512 MB**

The optimized algorithm should significantly outperform the baseline approach as the dataset size increases.



# 2. Motivation

Real-world systems such as YouTube Trending pages, gaming leaderboards, and social media ranking systems must constantly identify the most popular items from millions of entries. If a naive algorithm sorts the entire dataset each time engagement changes, the system would waste large amounts of computation time and resources. Using a heap structure allows the system to focus only on the **top results**, which significantly improves efficiency and scalability.



# 3. Candidate Approaches

## Approach A: Baseline

### Algorithm/Data Structure

Full Sorting of the Dataset

### Description

The baseline approach will sort the entire dataset based on engagement scores every time the leaderboard needs to be updated. After sorting all records, the system will select the **Top K entries** from the sorted list.

### Theoretical Complexity

**Time Complexity:**
O(n log n)

**Space Complexity:**
O(n)

Where **n** represents the total number of records.



## Approach B: Optimized

### Algorithm/Data Structure

Min-Heap (Priority Queue)

### Description

The optimized approach will maintain a **Min-Heap of size K** that stores only the Top K entries. As the algorithm processes the dataset, each new score will be compared with the smallest element in the heap.

If the new score is larger than the smallest element, it replaces that element and the heap reorganizes itself. This allows the system to maintain the Top K items without sorting the entire dataset.

### Theoretical Complexity

**Time Complexity:**
O(n log k)

**Space Complexity:**
O(k)

Where **k** represents the number of top entries being tracked.



# 4. Evaluation Plan

### Runtime

Execution time will be measured using Python's **time.perf_counter()** function. The runtime of the baseline sorting approach and the heap-based approach will be compared across datasets of different sizes.



### Memory

Memory usage will be measured using Python's **tracemalloc** module to observe how much memory each algorithm consumes during execution.



### Correctness

Correctness will be verified by comparing the Top K results from the optimized algorithm against the results from the baseline sorting approach.



### Dataset Realism

The algorithms will be tested using different types of datasets including:

* Randomly generated scores
* Sorted datasets
* Realistic engagement distributions

This will help analyze how each algorithm performs under different input conditions.



# 5. Dataset Plan

### Source

The dataset will be obtained from Kaggle:

**YouTube Trending Video Statistics Dataset**
[https://www.kaggle.com/datasets/datasnaek/youtube-new](https://www.kaggle.com/datasets/datasnaek/youtube-new)



### Generation / Acquisition

The dataset will be downloaded in **CSV format** from Kaggle. Additional larger datasets may be generated using Python to simulate datasets with **100,000, 500,000, and 1,000,000 records** in order to test algorithm performance at different scales.

