class Node:
    """A node in a doubly linked list."""

    def __init__(self, data):
        """Initializes a new node with the given data."""
        self.data = data
        self.next = None
        self.prev = None
