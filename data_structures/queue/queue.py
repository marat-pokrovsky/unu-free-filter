class Queue:
    """A queue implementation."""

    def __init__(self):
        """Initializes an empty queue."""
        self.items = []

    def is_empty(self):
        """Returns True if the queue is empty, False otherwise."""
        return self.items == []

    def enqueue(self, item):
        """Adds the given item to the queue."""
        self.items.insert(0, item)

    def dequeue(self):
        """Removes and returns the item at the front of the queue."""
        return self.items.pop()

    def size(self):
        """Returns the number of items in the queue."""
        return len(self.items)
