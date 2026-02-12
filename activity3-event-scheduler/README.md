# Activity 3 – Event_Scheduler

**Course:** CS 5329 – Algorithm Design and Analysis  
**Student Name:** Akula Sukeerth Net ID (xob17)
**Semester:** Spring 2026

---

## Week 1 Reflection

A heap works better than a regular list for this scheduler because it always keeps the most urgent event ready at the top without needing to sort the entire structure every time. If I used a list, I would have to scan or re-sort it repeatedly to figure out which request should be handled next, which becomes inefficient as more events are added. In this system, the operation that happens most often is selecting and removing the next highest-priority event. Using a heap makes that process fast and scalable, which is important in real event-driven systems.
