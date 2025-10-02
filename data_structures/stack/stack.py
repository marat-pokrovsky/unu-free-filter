class Stack:
    """A stack implementation."""

    def __init__(self):
        """Initializes an empty stack."""
        self.items = []

    def is_empty(self):
        """Returns True if the stack is empty, False otherwise."""
        return self.items == []

    def push(self, item):
        """Pushes the given item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Pops and returns the item at the top of the stack."""
        return self.items.pop()

    def peek(self):
        """Returns the item at the top of the stack without removing it."""
        return self.items[len(self.items)-1]

    def size(self):
        """Returns the number of items in the stack."""
        return len(self.items)
