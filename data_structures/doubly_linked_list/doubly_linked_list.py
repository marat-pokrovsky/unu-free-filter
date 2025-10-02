from .node import Node

class DoublyLinkedList:
    """A doubly linked list implementation."""

    def __init__(self):
        """Initializes an empty doubly linked list."""
        self.head = None

    def append(self, data):
        """Appends a new node with the given data to the end of the list."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node

    def prepend(self, data):
        """Prepends a new node with the given data to the beginning of the list."""
        new_node = Node(data)
        if self.head is not None:
            self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def to_list(self):
        """Converts the doubly linked list to a Python list."""
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(current_node.data)
            current_node = current_node.next
        return nodes
