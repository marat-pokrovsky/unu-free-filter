class HashTable:
    """A hash table implementation."""

    def __init__(self, size=10):
        """Initializes a new hash table."""
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """Hashes the given key."""
        return hash(key) % self.size

    def set(self, key, value):
        """Sets the value for the given key."""
        key_hash = self._hash(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """Gets the value for the given key."""
        key_hash = self._hash(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """Deletes the given key and its associated value."""
        key_hash = self._hash(key)
        if self.table[key_hash] is not None:
            for i in range(len(self.table[key_hash])):
                if self.table[key_hash][i][0] == key:
                    self.table[key_hash].pop(i)
                    return True
        return False
