# Activity 3 – Event_Scheduler

**Course:** CS 5329 – Algorithm Design and Analysis  
**Student Name:** Akula Sukeerth Net ID (xob17)
**Semester:** Spring 2026

---

## Week 2 Event Scheduling with Heaps

In this scheduler, the operations that dominate runtime are the heap insertions and removals (heappush and heappop). Each of these operations runs in O(log n) time, which keeps the system efficient even as the number of events grows. If we used a simple list instead and scanned it every time to find the highest-priority event, that would take O(n) per operation and become slow for large workloads.

Lazy updating is used because Python’s heap does not support efficient in-place updates. Instead of modifying an existing entry, we insert a new version and allow outdated entries to remain in the heap. These stale entries are safely ignored later by checking versions before processing. In practice, this approach is widely used because it keeps the implementation simple while maintaining good performance.
