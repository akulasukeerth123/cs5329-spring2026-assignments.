# Experiment Results

## Objective
Evaluate the performance of two algorithms for maintaining a Top-K leaderboard:

1. Full Sorting (Baseline)
2. Min-Heap (Optimized)


## Dataset

Dataset used: YouTube Trending Video Statistics Dataset  
https://www.kaggle.com/datasets/datasnaek/youtube-new



## Experimental Setup

Top-K Value: 50

Dataset Sizes Tested:
- 10,000 records
- 100,000 records
- 1,000,000 records



## Runtime Results

| Dataset Size | Sorting Time | Heap Time |
|---------------|-------------|-----------|
| 10,000 | TBD | TBD |
| 100,000 | TBD | TBD |
| 1,000,000 | TBD | TBD |



## Observations

- Heap-based Top-K selection should outperform full sorting when K is much smaller than N.
- Sorting processes the entire dataset, while the heap only maintains the Top-K elements.



## Conclusion

The heap-based approach is expected to be more efficient for real-time leaderboard ranking systems such as YouTube trending pages or gaming leaderboards.