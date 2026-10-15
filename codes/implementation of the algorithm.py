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
        print(f"Received and enqueued task: [{priority}] {task_description}")

    def assign_priority(self, interface_type, request_data):
        """
        Assign a priority to the request based on its type and content.

        Args:
            interface_type (str): The type of interface.
            request_data (dict): The data associated with the request.
            
        Returns:
            int: The priority level (1 is highest).
        """
        # Example priority assignment logic
        if interface_type == "CLI":
            return 1  # Highest priority for CLI-based requests
        elif request_data.get("action") in ["activate", "deactivate"]:
            return 2
        elif interface_type == "SOAP":
            return 3
        else:
            return 4  # Lowest priority for other types

    def create_task_description(self, interface_type, request_data):
        """
        Create a descriptive task string based on the request data.

        Args:
            interface_type (str): The type of interface.
            request_data (dict): The data associated with the request.

        Returns:
            str: A descriptive task string.
        """
        service_id = request_data.get("service_id", "Unknown")
        action = request_data.get("action", "No Action Specified")
        return f"{action.capitalize()} service [{service_id}] via {interface_type}"

    def process_tasks(self):
        """
        Process tasks in the priority queue by forwarding them to the backend.
        """
        while not self.priority_queue.is_empty():
            priority, task = self.priority_queue.remove()
            self.forward_to_backend(task)
            print(f"Processed Task: [{priority}] {task}")

    def forward_to_backend(self, task_description):
        """
        Transform the task description and send it to the backend CLI.

        Args:
            task_description (str): The description of the task.
        """
        # Example transformation: Convert task description to CLI command
        cli_command = self.transform_to_cli(task_description)
        # Simulate sending the CLI command to the backend
        print(f"Sending to backend CLI: {cli_command}")
        # Here, you would include actual code to interface with the backend system

    def transform_to_cli(self, task_description):
        """
        Transform the task description into a CLI command.
        Args:
            task_description (str): The description of the task.

        Returns:
            str: The CLI command.
        """
        # Simple transformation logic for demonstration
        action, service_info, via_interface = task_description.split(" ", 2)
        service_id = service_info.strip("[]")
        cli_command = f"{action.lower()} service_id={service_id}"
        return cli_command
    5.3. Demonstration of the Middleware Processor
    def middleware_demo():
        # Initialize the middleware processor
        processor = MiddlewareProcessor()
        
        # Simulate receiving service requests from different interfaces
        processor.receive_request(
            interface_type="SOAP",
            request_data={"service_id": "SVC1001", "action": "activate"}
        )
        processor.receive_request(
            interface_type="HTTP",
            request_data={"service_id": "SVC1002", "action": "deactivate"}
        )
        processor.receive_request(
            processor.receive_request(
        interface_type="CLI",
        request_data={"service_id": "SVC1003", "action": "update"}
    )
    processor.receive_request(
        interface_type="JML",
        request_data={"service_id": "SVC1004", "action": "activate"}
    )

    print("\n--- Processing Tasks ---\n")
    # Process all tasks based on priority
    processor.process_tasks()

# Call the middleware demo function
if __name__ == "__main__":
    middleware_demo()
           