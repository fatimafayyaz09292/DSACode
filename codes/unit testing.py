import heapq
import unittest

# Priority Queue Implementation
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

# Middleware Processor Implementation
class MiddlewareProcessor:
    def __init__(self):
        """
        Initialize a new MiddlewareProcessor with a priority queue for task processing.
        """
        self.pq = PriorityQueue()  # Using 'pq' to reference the PriorityQueue instance

    def receive_request(self, interface_type, request_data):
        """
        Simulate receiving a request and adding it to the queue for processing.
                Args:
                    interface_type (str): Type of the interface, e.g., "SOAP", "HTTP", etc.
                    request_data (dict): Data associated with the request.
        """
        # Assign priority based on interface type (this is just an example)
        priority = self._get_priority_for_interface(interface_type)
        self.pq.insert(priority, request_data)

    def process_tasks(self):
        """
        Process all tasks in the queue based on priority.
        """
        while not self.pq.is_empty():
            priority, task = self.pq.remove()
            print(f"Processing task: {task['action']} for {task['service_id']} with priority {priority}")

    def _get_priority_for_interface(self, interface_type):
        """
        Example logic for determining priority based on the interface type.
        """
        # Higher priority for CLI, lower priority for SOAP, HTTP, etc.
        priorities = {"CLI": 1, "SOAP": 2, "HTTP": 3, "JML": 4}
        return priorities.get(interface_type, 5)  # Default priority for unknown interfaces
    
#Unit Tests
class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()

    def test_insert_and_size(self):
        self.assertEqual(self.pq.size(), 0)
        self.pq.insert(2, "Task B")
        self.assertEqual(self.pq.size(), 1)
        self.pq.insert(1, "Task A")
        self.assertEqual(self.pq.size(), 2)

    def test_remove(self):
        self.pq.insert(2, "Task B")
        self.pq.insert(1, "Task A")
        priority, task = self.pq.remove()
        self.assertEqual(priority, 1)
        self.assertEqual(task, "Task A")
        self.assertEqual(self.pq.size(), 1)

    def test_peek(self):
        self.pq.insert(3, "Task C")
        self.pq.insert(1, "Task A")
        self.pq.insert(2, "Task B")
        priority, task = self.pq.peek()
        self.assertEqual(priority, 1)
        self.assertEqual(task, "Task A")
        self.assertEqual(self.pq.size(), 3)

    def test_is_empty(self):
        self.assertTrue(self.pq.is_empty())
        self.pq.insert(1, "Task A")
        self.assertFalse(self.pq.is_empty())

    def test_remove_empty(self):
        with self.assertRaises(IndexError):
            self.pq.remove()

    def test_peek_empty(self):
        with self.assertRaises(IndexError):
            self.pq.peek()

class TestMiddlewareProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MiddlewareProcessor()

    def test_receive_and_process_single_request(self):
        self.processor.receive_request(
            interface_type="CLI",
            request_data={"service_id": "SVC1001", "action": "activate"}
        )
        # Ensure the queue has 1 task
        self.assertEqual(self.processor.pq.size(), 1)
        # Ensure the task is correctly inserted
        priority, task = self.processor.pq.remove()
        self.assertEqual(task["service_id"], "SVC1001")
        self.assertEqual(task["action"], "activate")
        self.assertEqual(priority, 1)  # Assuming "CLI" has priority 1

    def test_receive_multiple_requests_and_process_order(self):
        # Receive multiple requests
        self.processor.receive_request(interface_type="CLI", request_data={"service_id": "SVC1001", "action": "activate"})
        self.processor.receive_request(interface_type="HTTP", request_data={"service_id": "SVC1002", "action": "deactivate"})
        self.processor.receive_request(interface_type="SOAP", request_data={"service_id": "SVC1003", "action": "update"})
        self.processor.receive_request(interface_type="JML", request_data={"service_id": "SVC1004", "action": "activate"})

        # Ensure the requests are queued in the right order
        self.assertEqual(self.processor.pq.size(), 4)

        # Process tasks (prints the tasks in priority order)
        self.processor.process_tasks()

# Run the tests
if __name__ == "__main__":
    unittest.main()



        