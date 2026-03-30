import heapq

def get_top_k_heap(data, k):
    """
    Optimized approach using Min-Heap
    Time: O(n log k)
    """
    heap = []

    for item in data:
        if len(heap) < k:
            heapq.heappush(heap, (item['score'], item))
        else:
            if item['score'] > heap[0][0]:
                heapq.heappushpop(heap, (item['score'], item))

    # Extract results and sort descending
    return [x[1] for x in sorted(heap, reverse=True)]