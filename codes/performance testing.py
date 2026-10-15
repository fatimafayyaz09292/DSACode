import heapq
import time
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

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
            task (dict): A structured dictionary describing the task.
        """    
        heapq.heappush(self.heap, (priority, self.count, task))
        self.count += 1
        logging.debug(f"Inserted task into queue: Priority={priority}, Task={task}")

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
        logging.debug(f"Removed task from queue: Priority={priority}, Task={task}")
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
        logging.debug(f"Peeked at queue: Priority={priority}, Task={task}")
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

class MiddlewareProcessor:
    def __init__(self):
        """
        Initialize the Middleware Processor with a Priority Queue.
        """
        self.priority_queue = PriorityQueue()

    def receive_request(self, interface_type, request_data):
        """
        Receive a service request from a front-end interface and assign a priority.

        Args:
            interface_type (str): The type of interface (SOAP, HTTP, JML, CLI).
            request_data (dict): The data associated with the request.
        """
        # Determine priority based on interface type or request content
        priority = self.assign_priority(interface_type, request_data)
        task_description = self.create_task_description(interface_type, request_data)
        self.priority_queue.insert(priority, task_description)
        logging.debug(f"Received and enqueued task: Priority={priority}, Task={task_description}")

    def assign_priority(self, interface_type, request_data):
        """
        Assign a priority to the request based on its type and content.
            Args:
                interface_type (str): The type of interface.
                request_data (dict): The data associated with the request.

        Returns:
            int: The priority level (1 is highest).
        """
        # Configurable priority rules
        priority_rules = {
            "CLI": 1,
            "HTTP": 2,
            "SOAP": 3,
            "JML": 4
        }

        action_priority = {
            "activate": 2,
            "deactivate": 2,
            "update": 3,
            "create": 2,
            "delete": 1  # Example of higher priority for delete actions
        }

        base_priority = priority_rules.get(interface_type.upper(), 5)  # Default low priority
        action = request_data.get("action", "update").lower()
        # Determine priority based on action and interface type
        action_prio = action_priority.get(action, 5)
        final_priority = min(base_priority, action_prio)

        logging.debug(f"Assigned priority: Interface={interface_type}, Action={action}, Priority={final_priority}")
        return final_priority

    def create_task_description(self, interface_type, request_data):
        """
        Create a structured task dictionary based on the request data.

        Args:
            interface_type (str): The type of interface.
            request_data (dict): The data associated with the request.

        Returns:
            dict: A dictionary containing task details.
        """
        service_id = request_data.get("service_id", "Unknown")
        action = request_data.get("action", "No Action Specified").capitalize()
        task = {
            "interface_type": interface_type,
            "service_id": service_id,
            "action": action
        }
        logging.debug(f"Created task description: {task}")
        return task
        
    async def process_tasks_async(self):
        """
        Asynchronously process tasks in the priority queue by forwarding them to the backend.
        """
        while not self.priority_queue.is_empty():
            priority, task = self.priority_queue.remove()
            await self.forward_to_backend_async(task)
            logging.debug(f"Processed Task: Priority={priority}, Task={task}")

    async def forward_to_backend_async(self, task_description):
        """
        Asynchronously transform the task description and send it to the backend CLI.

        Args:
            task_description (dict): The description of the task.
        """
        cli_command = self.transform_to_cli(task_description)
        # Simulate asynchronous sending to the backend
        await self.simulate_backend_interaction(cli_command)
        logging.debug(f"Sent to backend CLI: {cli_command}")

    async def simulate_backend_interaction(self, cli_command):
        """
        Simulate interaction with the backend CLI asynchronously.

        Args:
            cli_command (str): The CLI command to send.
        """
        # Simulate network or processing delay
        await asyncio.sleep(0)  # Replace with actual async backend call if available

    def transform_to_cli(self, task_description):
        """
        Transform the task description into a CLI command.

        Args:
            task_description (dict): The description of the task.

        Returns:
            str: The CLI command.
        """
        action = task_description["action"].lower()
        service_id = task_description["service_id"]
        cli_command = f"{action} service_id={service_id}"
        logging.debug(f"Transformed to CLI command: {cli_command}")
        return cli_command

def performance_test():
    """
    Conduct a performance test by inserting and processing a large number of requests.
    """
    processor = MiddlewareProcessor()  # Initialize the middleware processor
    num_requests = 10000  # Number of requests to simulate
    # Disable debug logging during performance test to reduce overhead
    logging.getLogger().setLevel(logging.INFO)

    # Simulate inserting a large number of requests
    start_time = time.time()  # Start time measurement
    for i in range(num_requests):
        # Cycle through different interface types and actions
        if i % 4 == 0:
            interface = "SOAP"
        elif i % 4 == 1:
            interface = "HTTP"
        elif i % 4 == 2:
            interface = "JML"
        else:
            interface = "CLI"

        if i % 3 == 0:
            action = "activate"
        elif i % 3 == 1:
            action = "deactivate"
        else:
            action = "update"

        service_id = f"SVC{i:05d}"  # Create unique service IDs

        # Receive the request and add it to the priority queue
        processor.receive_request(
            interface_type=interface,
            request_data={"service_id": service_id, "action": action}
        )

    insertion_time = time.time() - start_time  # Calculate the insertion time
    logging.info(f"Inserted {num_requests} requests in {insertion_time:.2f} seconds.")

    # Simulate processing all requests
    start_time = time.time()  # Start time measurement for processing
    asyncio.run(processor.process_tasks_async())
    processing_time = time.time() - start_time  # Calculate processing time
    logging.info(f"Processed {num_requests} requests in {processing_time:.2f} seconds.")

if __name__ == "__main__":
    performance_test()  # Run the performance test

            






