from .node import Node

class LinkedList:
    """A singly linked list implementation."""

    def __init__(self):
        """Initializes an empty linked list."""
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

    def prepend(self, data):
        """Prepends a new node with the given data to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """Deletes the first occurrence of a node with the given data."""
        current_node = self.head

        if current_node and current_node.data == data:
            self.head = current_node.next
            current_node = None
            return

        prev = None
        while current_node and current_node.data != data:
            prev = current_node
            current_node = current_node.next

        if current_node is None:
            return

        prev.next = current_node.next
        current_node = None

    def insert_after(self, prev_node_data, data):
        """Inserts a new node with the given data after the first occurrence of a node with the given previous node data."""
        current_node = self.head
        while current_node and current_node.data != prev_node_data:
            current_node = current_node.next

        if current_node:
            new_node = Node(data)
            new_node.next = current_node.next
            current_node.next = new_node

    def to_list(self):
        """Converts the linked list to a Python list."""
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(current_node.data)
            current_node = current_node.next
        return nodes

    def __str__(self):
        """Returns a string representation of the linked list."""
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(nodes)
