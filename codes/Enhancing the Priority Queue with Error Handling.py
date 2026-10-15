import heapq
import logging

# Configure logging
logging.basicConfig(filename='midd.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

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

        Raises:
            ValueError: If the priority is not a positive integer.
        """
        if not isinstance(priority, int) or priority < 1:
            logging.error(f"Invalid priority level: {priority}. Must be a positive integer.")
            raise ValueError("Priority must be a positive integer.")
        try:
            heapq.heappush(self.heap, (priority, self.count, task))
            self.count += 1
        except Exception as e:
            logging.error(f"Error inserting task '{task}' with priority {priority}: {e}")
            raise

    def remove(self):
        """
        Remove and return the highest-priority task from the queue.

        Returns:
            tuple: A tuple containing (priority, task).

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            logging.error("Attempted to remove from an empty priority queue.")
            raise IndexError("remove from empty priority queue")
        try:
            priority, count, task = heapq.heappop(self.heap)
            return (priority, task)
        except Exception as e:
            logging.error(f"Error removing task from queue: {e}")
            raise
        def peek(self):
            """
            Return the highest-priority task without removing it from the queue.

            Returns:
                tuple: A tuple containing (priority, task).

            Raises:
                IndexError: If the priority queue is empty.
            """
        if self.is_empty():
            logging.error("Attempted to peek into an empty priority queue.")
            raise IndexError("peek from empty priority queue")
        try:
            priority, count, task = self.heap[0]
            return (priority, task)
        except Exception as e:
            logging.error(f"Error peeking into queue: {e}")
            raise

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

    def clear(self):
        """
        Empty the entire priority queue.
        """
        try:
            self.heap.clear()
            self.count = 0
        except Exception as e:
            logging.error(f"Error clearing the priority queue: {e}")
            raise


    


            
          
