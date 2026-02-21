import heapq

def create_scheduler():
    heap = []
    current_version = {}   # event_id -> latest version (if present)
    return heap, current_version

def add_event(heap, current_version, event_id, priority, created_time, payload):
    """
    Adds a new event to the scheduler.
    Heap entry: (priority, created_time, version, event_id, payload)
    """
    version = current_version.get(event_id, 0) + 1
    current_version[event_id] = version
    heapq.heappush(heap, (priority, created_time, version, event_id, payload))

def update_priority(heap, current_version, event_id, new_priority, update_time):
    if event_id not in current_version:
        return False  # cannot update something not scheduled (or cancelled)

    new_version = current_version[event_id] + 1
    current_version[event_id] = new_version

    # Payload can be anything; for this assignment, we just note it's an update.
    payload = {"type": "update", "msg": f"Priority updated to {new_priority}"}
    heapq.heappush(heap, (new_priority, update_time, new_version, event_id, payload))
    return True

def cancel_event(current_version, event_id):
    """
    Cancels an event so it will never be processed.
    Lazy cancellation:
      - Remove it from current_version
      - discard_stale_top will later drop all heap entries for it.
    Returns True if cancelled, False if it wasn't scheduled.
    """
    return current_version.pop(event_id, None) is not None

def discard_stale_top(heap, current_version):
    """
    Removes stale entries from the top of the heap.
    Stale means:
      - event_id is not in current_version (cancelled or already processed)
      - or version doesn't match latest version
    """
    while heap:
        priority, created_time, version, event_id, payload = heap[0]
        latest = current_version.get(event_id)

        if latest is None or version != latest:
            heapq.heappop(heap)
        else:
            break

def peek_next(heap, current_version):
    discard_stale_top(heap, current_version)
    return heap[0] if heap else None

def pop_next(heap, current_version):
    discard_stale_top(heap, current_version)
    if not heap:
        return None

    priority, created_time, version, event_id, payload = heapq.heappop(heap)

    # If it's still current, mark it done by removing from current_version
    if current_version.get(event_id) == version:
        del current_version[event_id]

    return (priority, created_time, version, event_id, payload)

def main():
    heap, current_version = create_scheduler()

    print("=== ADD EVENTS ===")
    add_event(heap, current_version, "E1", 3, 1001, {"type": "helpdesk", "msg": "Password reset"})
    add_event(heap, current_version, "E2", 1, 1002, {"type": "clinic", "msg": "Chest pain intake"})
    add_event(heap, current_version, "E3", 2, 1003, {"type": "dispatch", "msg": "Bus delay report"})
    add_event(heap, current_version, "E4", 1, 1004, {"type": "emergency", "msg": "Supply shortage"})
    add_event(heap, current_version, "E5", 4, 1005, {"type": "tutoring", "msg": "Need math help"})
    add_event(heap, current_version, "E6", 2, 1006, {"type": "it", "msg": "Laptop not booting"})

    print("Peek after adds:", peek_next(heap, current_version))

    print("\n=== UPDATE PRIORITY (LAZY) ===")
    ok = update_priority(heap, current_version, "E3", new_priority=1, update_time=1007)
    print("Updated E3 to priority 1:", ok)
    print("Peek after update:", peek_next(heap, current_version))

    print("\n=== CANCEL EVENT (LAZY) ===")
    ok = cancel_event(current_version, "E5")
    print("Cancelled E5:", ok)
    print("Peek after cancel:", peek_next(heap, current_version))

    print("\n=== FINAL PROCESSING ORDER ===")
    while True:
        nxt = pop_next(heap, current_version)
        if nxt is None:
            break
        print(nxt)

if __name__ == "__main__":
    main()