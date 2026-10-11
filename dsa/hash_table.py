class HashTable:
    """Simple hash table for O(1) average PNR lookup."""

    def __init__(self):
        self.table = {}

    def set(self, key, value):
        self.table[key] = value

    def get(self, key, default=None):
        return self.table.get(key, default)

    def delete(self, key):
        if key in self.table:
            del self.table[key]

    def contains(self, key):
        return key in self.table

    def size(self):
        return len(self.table)
