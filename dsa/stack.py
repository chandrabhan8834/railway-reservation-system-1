class RailwayStack:
    """Stack implementation for cancellation history."""

    def __init__(self):
        self.items = []

    def push(self, value):
        # Stack: Push is O(1) as we append to the top of the stack.
        self.items.append(value)

    def pop(self):
        # Stack: Pop is O(1) as we remove the latest item from the top.
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)
