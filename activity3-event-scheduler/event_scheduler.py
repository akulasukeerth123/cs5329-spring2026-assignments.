import heapq

def create_scheduler():
    heap = []
    current_version = {}
    return heap, current_version

def add_event(heap, current_version, event_id, priority, created_time, payload):
    """
    Adds a new event to the scheduler.
    Each heap entry is a tuple:
    (priority, created_time, version, event_id, payload)
    """
    version = current_version.get(event_id, 0) + 1
    current_version[event_id] = version

    entry = (priority, created_time, version, event_id, payload)
    heapq.heappush(heap, entry)

def discard_stale_top(heap, current_version):
    """
    Removes stale entries from the top of the heap.
    This is called before peeking or popping to ensure we only consider valid events.
    """
    while heap:
        priority, created_time, version, event_id, payload = heap[0]
        latest = current_version.get(event_id)

        if latest is None or version != latest:
            heapq.heappop(heap)
        else:
            break

def peek_next(heap, current_version):
    """
    Returns the next event without removing it.
    Returns None if no valid events exist.
    """
    discard_stale_top(heap, current_version)
    if not heap:
        return None
    return heap[0]

def pop_next(heap, current_version):
    """
    Removes and returns the next event.
    Returns None if no valid events exist.
    """
    discard_stale_top(heap, current_version)
    if not heap:
        return None
    event = heapq.heappop(heap)
    priority, created_time, version, event_id, payload = event
    if current_version.get(event_id) == version:
        del current_version[event_id]

    return event

def main():
    heap, current_version = create_scheduler()
    # Add some events with varying priorities and creation times
    add_event(heap, current_version, "E1", 3, 1001, {"type": "helpdesk", "msg": "Password reset"})
    add_event(heap, current_version, "E2", 1, 1002, {"type": "clinic", "msg": "Chest pain intake"})
    add_event(heap, current_version, "E3", 2, 1003, {"type": "dispatch", "msg": "Bus delay report"})
    add_event(heap, current_version, "E4", 1, 1004, {"type": "emergency", "msg": "Supply shortage"})
    add_event(heap, current_version, "E5", 4, 1005, {"type": "tutoring", "msg": "Need math help"})
    add_event(heap, current_version, "E6", 2, 1006, {"type": "it", "msg": "Laptop not booting"})

    
    add_event(heap, current_version, "E3", 1, 1007, {"type": "dispatch", "msg": "Updated: bus breakdown"})

   
    del current_version["E5"]

    print("Peek next:", peek_next(heap, current_version))

    print("\nProcessing order:")
    while True:
        nxt = pop_next(heap, current_version)
        if nxt is None:
            break
        print(nxt)

if __name__ == "__main__":
    main()
