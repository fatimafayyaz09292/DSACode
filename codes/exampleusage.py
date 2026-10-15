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
