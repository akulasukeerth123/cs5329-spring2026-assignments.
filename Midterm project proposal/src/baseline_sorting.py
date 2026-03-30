def get_top_k_baseline(data, k):
    """
    Baseline approach using full sorting
    Time: O(n log n)
    """
    # Sort entire dataset by score (descending)
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)

    # Return top K elements
    return sorted_data[:k]