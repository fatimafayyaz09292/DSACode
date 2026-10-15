import heapq
import timeit
import tracemalloc

# Priority Queue Class Implementation
class PriorityQueue:
    def __init__(self):
        """Initialize the Priority Queue"""
        self.heap = []

    def insert(self, priority, task):
        """Insert a task with a given priority into the priority queue"""
        heapq.heappush(self.heap, (priority, task))

    def remove(self):
        """Remove and return the task with the highest priority"""
        if not self.is_empty():
            return heapq.heappop(self.heap)
        else:
            raise IndexError("Cannot remove from an empty queue")

    def peek(self):
        """Peek at the task with the highest priority without removing it"""
        if not self.is_empty():
            return self.heap[0]
        else:
            raise IndexError("Cannot peek into an empty queue")

    def is_empty(self):
        """Check if the queue is empty"""
        return len(self.heap) == 0

    def size(self):
        """Return the number of tasks in the priority queue"""
        return len(self.heap)

    def clear(self):
        """Clear all tasks from the priority queue"""
        self.heap = []

# Test Time Complexity of Priority Queue
def test_insert_performance(pq, num_elements):
    for i in range(num_elements):
        pq.insert(i, f"Task {i}")

def test_remove_performance(pq, num_elements):
    for _ in range(num_elements):
        pq.remove()

# Profile Memory Usage for Priority Queue
def profile_memory_usage():
    tracemalloc.start()
    pq = PriorityQueue()
    num_elements = 10000

    for i in range(num_elements):
        pq.insert(i, f"Task {i}")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 10**6:.2f} MB")
    print(f"Peak memory usage: {peak / 10**6:.2f} MB")

    tracemalloc.stop()

# Integrated Test for Time and Space Complexity
def integrated_test():
    tracemalloc.start()
    pq = PriorityQueue()
    num_elements = 10000

    # Measure insertion time and memory
    start_time = timeit.default_timer()
    for i in range(num_elements):
        pq.insert(i, f"Task {i}")
    end_time = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Time to insert {num_elements} elements: {end_time - start_time:.5f} seconds")
    print(f"Current memory usage after insertion: {current / 10**6:.2f} MB")
    print(f"Peak memory usage during insertion: {peak / 10**6:.2f} MB")

    # Reset tracemalloc for removal
    tracemalloc.stop()
    tracemalloc.start()

    # Measure removal time and memory
    start_time = timeit.default_timer()
    for _ in range(num_elements):
        pq.remove()
    end_time = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()

    print(f"Time to remove {num_elements} elements: {end_time - start_time:.5f} seconds")
    print(f"Current memory usage after removal: {current / 10**6:.2f} MB")
    print(f"Peak memory usage during removal: {peak / 10**6:.2f} MB")

    tracemalloc.stop()

# Main Function
if __name__ == "__main__":
    # Priority Queue Usage Example
    pq = PriorityQueue()
    pq.insert(1, "Task 1")
    pq.insert(3, "Task 2")
    pq.insert(2, "Task 3")
    print("Peek:", pq.peek())
    print("Remove:", pq.remove())
    print("Peek after removal:", pq.peek())
    print("Queue Size:", pq.size())

    print("\n--- Time Complexity Test ---")
    num_elements = 10000
    pq = PriorityQueue()
    insert_time = timeit.timeit(lambda: test_insert_performance(pq, num_elements), number=1)
    print(f"Time to insert {num_elements} elements: {insert_time:.5f} seconds")

    pq = PriorityQueue()
    test_insert_performance(pq, num_elements)
    remove_time = timeit.timeit(lambda: test_remove_performance(pq, num_elements), number=1)
    print(f"Time to remove {num_elements} elements: {remove_time:.5f} seconds")

    print("\n--- Space Complexity Test ---")
    profile_memory_usage()

    print("\n--- Integrated Time and Space Test ---")
    integrated_test()
