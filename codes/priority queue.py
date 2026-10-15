import heapq

class PriorityQueue:
    def __init__(self):
        """
        Initialize a new PriorityQueue.
        """
        self.heap = []
        self.count = 0  # To maintain the order of insertion for tasks with the same priority

    def insert(self, priority, task):
        """
        Insert a new task with the given priority into the queue.

        Args:
            priority (int): The priority level of the task. Lower numbers indicate higher priority.
            task (str): A description of the task.
        """
        heapq.heappush(self.heap, (priority, self.count, task))
        self.count += 1

    def remove(self):
        """
        Remove and return the highest-priority task from the queue.

        Returns:
            tuple: A tuple containing (priority, task).

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
           raise IndexError("remove from empty priority queue")
        priority, count, task = heapq.heappop(self.heap)
        return (priority, task)

    def peek(self):
        """
        Return the highest-priority task without removing it from the queue.

        Returns:
            tuple: A tuple containing (priority, task).

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        priority, count, task = self.heap[0]
        return (priority, task)

    def is_empty(self):
        """
        Check if the priority queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.heap) == 0
    def size(self):
        """
        Return the number of tasks in the priority queue.

        Returns:
            int: The size of the queue.
        """
        return len(self.heap)

def example_usage():
    # Initialize the priority queue
    pq = PriorityQueue()

    # Insert tasks with varying priorities
    pq.insert(priority=1, task="Configure network switch")
    pq.insert(priority=3, task="Service request for customer A")
    pq.insert(priority=2, task="Update device firmware")
    pq.insert(priority=4, task="Routine network check")

    # Display the size of the queue
    print(f"Queue Size: {pq.size()}")  # Output: Queue Size: 4

    # Peek at the highest-priority task
    priority, task = pq.peek()
    print(f"Highest Priority Task: [{priority}] {task}")  # Output: [1] Configure network switch

    # Remove and process tasks based on priority
    while not pq.is_empty():
        priority, task = pq.remove()
        print(f"Processing Task: [{priority}] {task}")

# Call the example usage function
if __name__ == "__main__":
    example_usage()
