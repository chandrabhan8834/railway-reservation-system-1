from collections import deque


class RailwayQueue:
    """Queue implementation for waiting list management."""

    def __init__(self):
        self.items = deque()

    def enqueue(self, value):
        # Queue: Enqueue is O(1) because we append to the rear of the deque.
        self.items.append(value)

    def dequeue(self):
        # Queue: Dequeue is O(1) because we remove from the front of the deque.
        if self.is_empty():
            return None
        return self.items.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)
