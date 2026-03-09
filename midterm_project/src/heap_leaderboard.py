# Optimized Implementation
# Algorithm: Min-Heap (Priority Queue)
# Description:
# This approach maintains a Min-Heap of size K to store the Top-K
# highest scoring entries. As new scores are processed, they are
# compared with the smallest element in the heap. If the score is
# larger, it replaces the smallest element and the heap reorganizes.
#
# Time Complexity: O(n log k)
# Space Complexity: O(k)