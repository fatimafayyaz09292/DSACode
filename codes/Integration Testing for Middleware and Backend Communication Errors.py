import logging
import random
import unittest
from queue import PriorityQueue

# Configure logging
logging.basicConfig(
    filename='middleware_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# MiddlewareProcessor Implementation
class MiddlewareProcessor:
    def __init__(self):
        self.errors = 0
        self.lock = False  # Simulate lock for race conditions
        self.priority_queue = PriorityQueue()

    def receive_request(self, interface_type, request_data, priority=1):
        """Simulates receiving a request."""
        # Check for valid interface type
        if interface_type not in ["SOAP", "HTTP", "JML", "CLI"]:
            logging.error(f"Invalid interface type: {interface_type}")
            raise ValueError(f"Invalid interface type: {interface_type}")

        # Simulate data validation error (random 10% chance)
        if random.random() < 0.10:
            logging.error(f"Invalid data received in request: {request_data}")
            logging.warning(f"Skipping invalid task with data: {request_data}")
            return

        # Simulate system lock condition
        if self.lock:
            logging.warning("System is locked. Request rejected.")
            raise Exception("System lock in place. Please try again later.")

        # Add valid task to the priority queue
        self.priority_queue.put((priority, request_data))
        logging.info(f"Received and enqueued task with priority {priority}: {request_data}")

    def process_task(self, task, simulate_error=False):
        """Simulates processing a single task."""
        try:
            logging.info(f"Sending to backend {task['interface']}: {task['action']} service_id={task['service_id']}")

            # Force error simulation for testing
            if simulate_error or random.random() < 0.10:
                raise Exception(f"Error forwarding to backend: Simulated backend failure for {task['interface']}.")

            logging.info(f"Processed Task: {task['action']} for service_id={task['service_id']}")
        except Exception as e:
            self.errors += 1
            logging.error(f"Failed to process task: {task['action']} due to {str(e)}")
            raise

    def process_tasks(self, simulate_error=False):
        """Processes all tasks in the priority queue."""
        while not self.priority_queue.empty():
            priority, task = self.priority_queue.get()
            logging.info(f"Processing task with priority {priority}: {task}")
            self.process_task(task, simulate_error=simulate_error)


# Integration Testing with unittest
class TestMiddlewareIntegration(unittest.TestCase):
    def setUp(self):
        self.processor = MiddlewareProcessor()

    def test_unsupported_interface_type(self):
        """Test handling unsupported interface types."""
        with self.assertRaises(ValueError):
            self.processor.receive_request("FTP", {"service_id": "SVC1015", "action": "activate"})

    def test_data_validation_error(self):
        """Test random data validation error."""
        try:
            self.processor.receive_request("CLI", {"service_id": "SVC1016", "action": "invalid"}, priority=1)
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

    def test_system_lock(self):
        """Test system lock prevents processing."""
        self.processor.lock = True
        with self.assertRaises(Exception):
            self.processor.receive_request("CLI", {"service_id": "SVC1016", "action": "deactivate"})

    def test_backend_communication_error(self):
        """Test backend communication error."""
        # Add a task to the queue
        self.processor.receive_request("CLI", {"service_id": "SVC1014", "action": "fail", "interface": "CLI"}, priority=1)

        # Process tasks with error simulation enabled
        with self.assertRaises(Exception):
            while not self.processor.priority_queue.empty():
                _, task = self.processor.priority_queue.get()
                self.processor.process_task(task, simulate_error=True)

    def test_successful_task_processing(self):
        """Test successful task processing."""
        self.processor.receive_request("CLI", {"service_id": "SVC1012", "action": "activate", "interface": "CLI"}, priority=1)
        self.processor.receive_request("HTTP", {"service_id": "SVC1013", "action": "deactivate", "interface": "HTTP"}, priority=2)
        self.processor.process_tasks()

    def test_empty_queue_processing(self):
        """Test handling of an empty queue."""
        try:
            self.processor.process_tasks()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)