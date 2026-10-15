import heapq
import logging
import unittest

# Configure logging
logging.basicConfig(
    filename='middleware_errors.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# PriorityQueue Implementation
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0  # Maintain insertion order for tasks with the same priority
        self.tasks_set = set()  # Track tasks to prevent duplicates

    def insert(self, priority, task):
        if not isinstance(priority, int) or priority <= 0:
            raise ValueError("Priority must be a positive integer.")
        if not task or not isinstance(task, str):
            raise ValueError("Task description must be a non-empty string.")
        if task in self.tasks_set:
            raise ValueError(f"Task '{task}' already exists in the queue.")
        heapq.heappush(self.heap, (priority, self.count, task))
        self.tasks_set.add(task)
        self.count += 1

    def remove(self):
        if self.is_empty():
            raise IndexError("Cannot remove from an empty priority queue.")
        priority, _, task = heapq.heappop(self.heap)
        self.tasks_set.remove(task)
        return priority, task

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty priority queue.")
        priority, _, task = self.heap[0]
        return priority, task

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)


# MiddlewareProcessor Implementation
class MiddlewareProcessor:
    def __init__(self):
        self.priority_queue = PriorityQueue()

    def receive_request(self, interface_type, request_data):
        if interface_type not in ["SOAP", "HTTP", "JML", "CLI"]:
            raise ValueError(f"Error: Unsupported interface type: {interface_type}")
        priority = self.assign_priority(interface_type, request_data)
        task_description = f"Process {request_data.get('action', 'unknown')} [{request_data.get('service_id', 'unknown')}]"
        self.priority_queue.insert(priority, task_description)

    def assign_priority(self, interface_type, request_data):
        action = request_data.get("action", "").lower()
        if interface_type == "CLI":
            return 1
        elif action in ["activate", "deactivate"]:
            return 2
        elif interface_type == "SOAP":
            return 3
        return 4

    def process_tasks(self):
        while not self.priority_queue.is_empty():
            priority, task = self.priority_queue.remove()
            self.execute_cli_command(task)

    def execute_cli_command(self, command):
        if command == "fail service_id=SVC1010":
            raise RuntimeError("Simulated CLI command failure.")
        print(f"Executed: {command}")


# Integration Testing with unittest
class TestIntegrationErrorHandling(unittest.TestCase):
    def setUp(self):
        self.processor = MiddlewareProcessor()

    def test_unsupported_interface_type(self):
        """Test handling unsupported interface types."""
        with self.assertRaises(ValueError):
            self.processor.receive_request("FTP", {"action": "activate", "service_id": "SVC1009"})

    def test_duplicate_task_insertion(self):
        """Test handling duplicate tasks in the priority queue."""
        self.processor.priority_queue.insert(1, "Task 1")
        with self.assertRaises(ValueError):
            self.processor.priority_queue.insert(1, "Task 1")

    def test_invalid_priority_assignment(self):
        """Test handling invalid priority assignments."""
        with self.assertRaises(ValueError):
            self.processor.priority_queue.insert(0, "Invalid Task")

    def test_malformed_task_description(self):
        """Test handling malformed task descriptions."""
        with self.assertRaises(ValueError):
            self.processor.priority_queue.insert(1, "")

    def test_backend_cli_failure(self):
        """Test handling CLI command failure."""
        self.processor.priority_queue.insert(1, "fail service_id=SVC1010")
        with self.assertRaises(RuntimeError):
            self.processor.process_tasks()

    def test_successful_task_processing(self):
        """Test successful task processing."""
        self.processor.receive_request("CLI", {"action": "activate", "service_id": "SVC1011"})
        self.processor.receive_request("SOAP", {"action": "deactivate", "service_id": "SVC1012"})
        self.processor.process_tasks()
        self.assertTrue(self.processor.priority_queue.is_empty())

    def test_empty_queue_removal(self):
        """Test handling task removal from an empty queue."""
        with self.assertRaises(IndexError):
            self.processor.priority_queue.remove()

    def test_empty_queue_peek(self):
        """Test handling peek operation on an empty queue."""
        with self.assertRaises(IndexError):
            self.processor.priority_queue.peek()


if __name__ == '__main__':
    unittest.main(verbosity=2)

