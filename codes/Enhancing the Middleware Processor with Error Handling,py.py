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

        Raises:
            ValueError: If the interface type is unsupported or request data is invalid.
        """
        try:
            priority = self.assign_priority(interface_type, request_data)
            task_description = self.create_task_description(interface_type, request_data)
            self.priority_queue.insert(priority, task_description)
            print(f"Received and enqueued task: [{priority}] {task_description}")
        except ValueError as ve:
            logging.error(f"ValueError in receive_request: {ve}")
            print(f"Error: {ve}")
        except Exception as e:
            logging.error(f"Unexpected error in receive_request: {e}")
            print("An unexpected error occurred while receiving the request.")
            
    def assign_priority(self, interface_type, request_data):
        """
        Assign a priority to the request based on its type and content.

        Args:
            interface_type (str): The type of interface.
            request_data (dict): The data associated with the request.

        Returns:
            int: The priority level (1 is highest).

        Raises:
            ValueError: If the interface type is unsupported.
        """
        valid_interfaces = ["CLI", "SOAP", "HTTP", "JML"]
        if interface_type not in valid_interfaces:
            logging.error(f"Unsupported interface type received: {interface_type}")
            raise ValueError(f"Unsupported interface type: {interface_type}")

        # Example priority assignment logic
        action = request_data.get("action", "").lower()
        if interface_type == "CLI":
            return 1  # Highest priority for CLI-based requests
        elif action in ["activate", "deactivate"]:
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
            try:
                priority, task = self.priority_queue.remove()
                self.forward_to_backend(task)
                print(f"Processed Task: [{priority}] {task}")
            except Exception as e:
                logging.error(f"Error processing task '{task}': {e}")
                print(f"Failed to process task: '{task}'")

    def forward_to_backend(self, task_description):
        """
        Transform the task description and send it to the backend CLI.

        Args:
            task_description (str): The description of the task.

        Raises:
            RuntimeError: If transformation fails or backend communication fails.
        """
        try:
            cli_command = self.transform_to_cli(task_description)
            # Simulate sending the CLI command to the backend
            self.execute_cli_command(cli_command)
            print(f"Sending to backend CLI: {cli_command}")
        except Exception as e:
            logging.error(f"Error forwarding to backend: {e}")
            raise RuntimeError("Failed to forward task to backend.")

    def transform_to_cli(self, task_description):
        """
        Transform the task description into a CLI command.
        
        Args:
            task_description (str): The description of the task.

        Returns:
            str: The CLI command.

        Raises:
            ValueError: If the task description format is invalid.
        """
        try:
            action, service_info, via_interface = task_description.split(" ", 2)
            service_id = service_info.strip("[]")
            cli_command = f"{action.lower()} service_id={service_id}"
            return cli_command
        except ValueError as ve:
            logging.error(f"Invalid task description format: {task_description}")
            raise ValueError("Invalid task description format.") from ve
        except Exception as e:
            logging.error(f"Error transforming task to CLI: {e}")
            raise

    def execute_cli_command(self, cli_command):
        """
        Execute the CLI command on the backend system.

        Args:
            cli_command (str): The CLI command to execute.

        Raises:
            ConnectionError: If unable to communicate with the backend.
            RuntimeError: If the CLI command execution fails.
        """
        try:
            # Placeholder for actual CLI execution logic
            # For demonstration, we'll simulate successful execution
            if not cli_command:
                raise RuntimeError("Empty CLI command.")
            # Simulate a potential failure
            if "fail" in cli_command:
                raise RuntimeError("Simulated CLI command failure.")
            # Simulate successful execution
        except RuntimeError as re:
            logging.error(f"CLI command execution error: {re}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during CLI command execution: {e}")
            raise ConnectionError("Failed to communicate with backend CLI.") from e


