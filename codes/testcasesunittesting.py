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
        """Initialize a new PriorityQueue."""
        self.heap = []
        self.count = 0  # To maintain insertion order for tasks with the same priority

    def insert(self, priority, task):
        """Insert a new task with the given priority into the queue."""
        if not isinstance(priority, int) or priority < 1:
            logging.error(f"Invalid priority level: {priority}. Must be a positive integer.")
            raise ValueError("Priority must be a positive integer.")
        heapq.heappush(self.heap, (priority, self.count, task))
        self.count += 1

    def remove(self):
        """Remove and return the highest-priority task from the queue."""
        if self.is_empty():
            logging.error("Attempted to remove from an empty priority queue.")
            raise IndexError("remove from empty priority queue")
        priority, _, task = heapq.heappop(self.heap)
        return (priority, task)

    def peek(self):
        """Return the highest-priority task without removing it from the queue."""
        if self.is_empty():
            logging.error("Attempted to peek into an empty priority queue.")
            raise IndexError("peek from empty priority queue")
        priority, _, task = self.heap[0]
        return (priority, task)

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self.heap) == 0

    def size(self):
        """Return the number of tasks in the priority queue."""
        return len(self.heap)

    def clear(self):
        """Empty the entire priority queue."""
        self.heap.clear()
        self.count = 0


# MiddlewareProcessor Implementation
class MiddlewareProcessor:
    def __init__(self):
        """Initialize the Middleware Processor with a Priority Queue."""
        self.priority_queue = PriorityQueue()

    def receive_request(self, interface_type, request_data):
        """Receive a service request from a front-end interface and assign a priority."""
        priority = self.assign_priority(interface_type, request_data)
        task_description = self.create_task_description(interface_type, request_data)
        self.priority_queue.insert(priority, task_description)

    def assign_priority(self, interface_type, request_data):
        """Assign a priority to the request based on its type and content."""
        valid_interfaces = ["CLI", "SOAP", "HTTP", "JML"]
        if interface_type not in valid_interfaces:
            logging.error(f"Unsupported interface type received: {interface_type}")
            raise ValueError(f"Unsupported interface type: {interface_type}")
        
        action = request_data.get("action", "").lower()
        if interface_type == "CLI":
            return 1
        elif action in ["activate", "deactivate"]:
            return 2
        elif interface_type == "SOAP":
            return 3
        return 4

    def create_task_description(self, interface_type, request_data):
        """Create a descriptive task string based on the request data."""
        service_id = request_data.get("service_id", "Unknown")
        action = request_data.get("action", "No Action Specified")
        return f"{action.capitalize()} service [{service_id}] via {interface_type}"

    def process_tasks(self):
        """Process tasks in the priority queue by forwarding them to the backend."""
        while not self.priority_queue.is_empty():
            _, task = self.priority_queue.remove()
            self.forward_to_backend(task)

    def forward_to_backend(self, task_description):
        """Transform the task description and send it to the backend CLI."""
        cli_command = self.transform_to_cli(task_description)
        self.execute_cli_command(cli_command)

    def transform_to_cli(self, task_description):
        """Transform the task description into a CLI command."""
        try:
            action, service_info, via_interface = task_description.split(" ", 2)
            service_id = service_info.strip("[]")
            cli_command = f"{action.lower()} service_id={service_id}"
            return cli_command
        except ValueError:
            logging.error(f"Invalid task description format: {task_description}")
            raise ValueError("Invalid task description format.")

    def execute_cli_command(self, cli_command):
        """Execute the CLI command on the backend system."""
        if not cli_command:
            raise RuntimeError("Empty CLI command.")
        if "fail" in cli_command:
            raise RuntimeError("Simulated CLI command failure.")
        # Simulate successful execution


# Unit Tests for PriorityQueue and MiddlewareProcessor
class TestErrorHandlingAndReporting(unittest.TestCase):

    def setUp(self):
        self.queue = PriorityQueue()
        self.processor = MiddlewareProcessor()

    # PriorityQueue Test Cases
    def test_insert_invalid_priority(self):
        with self.assertRaises(ValueError):
            self.queue.insert(-1, "Invalid Task")
        with self.assertRaises(ValueError):
            self.queue.insert(0, "Another Invalid Task")

    def test_insert_valid_priority(self):
        self.queue.insert(1, "Valid Task")
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek(), (1, "Valid Task"))

    def test_remove_empty_queue(self):
        with self.assertRaises(IndexError):
            self.queue.remove()

    def test_remove_valid(self):
        self.queue.insert(1, "Task 1")
        self.queue.insert(2, "Task 2")
        priority, task = self.queue.remove()
        self.assertEqual(priority, 1)
        self.assertEqual(task, "Task 1")

    def test_peek_empty_queue(self):
        with self.assertRaises(IndexError):
            self.queue.peek()

    def test_peek_valid(self):
        self.queue.insert(1, "Task 1")
        self.assertEqual(self.queue.peek(), (1, "Task 1"))

    def test_clear_queue(self):
        self.queue.insert(1, "Task 1")
        self.queue.insert(2, "Task 2")
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())

    def test_size(self):
        self.queue.insert(1, "Task 1")
        self.queue.insert(2, "Task 2")
        self.assertEqual(self.queue.size(), 2)

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.insert(1, "Task 1")
        self.assertFalse(self.queue.is_empty())

    # MiddlewareProcessor Test Cases
    def test_receive_request_invalid_interface(self):
        with self.assertRaises(ValueError):
            self.processor.receive_request("INVALID_INTERFACE", {"action": "test"})

    def test_receive_request_valid_interface(self):
        self.processor.receive_request("CLI", {"action": "activate"})
        self.assertEqual(self.processor.priority_queue.size(), 1)

    def test_assign_priority_invalid_interface(self):
        with self.assertRaises(ValueError):
            self.processor.assign_priority("INVALID_INTERFACE", {})

    def test_assign_priority_valid_interface(self):
        priority = self.processor.assign_priority("CLI", {"action": "activate"})
        self.assertEqual(priority, 1)

    def test_process_tasks_empty_queue(self):
        self.processor.process_tasks()
        self.assertTrue(self.processor.priority_queue.is_empty())

    def test_process_tasks_valid(self):
        self.processor.receive_request("CLI", {"action": "activate"})
        self.processor.process_tasks()
        self.assertTrue(self.processor.priority_queue.is_empty())

    def test_transform_to_cli_invalid_format(self):
        """Test transforming an invalid task description to CLI command."""
        with self.assertRaises(ValueError):
            self.processor.transform_to_cli("InvalidTaskWithoutSpaces")

    def test_execute_cli_command_empty_command(self):
        with self.assertRaises(RuntimeError):
            self.processor.execute_cli_command("")

    def test_execute_cli_command_fail_simulation(self):
        with self.assertRaises(RuntimeError):
            self.processor.execute_cli_command("fail")


if __name__ == '__main__':
    unittest.main(verbosity=2)