import math

'''
The BalancedRing implements a circular array with a symmetric traversal pattern, facilitating evenly 
distributed lookup or storage of elements. The class supports key-value insertion, removal, and retrieval, 
ensuring that the ring remains balanced. The traversal follows a +k, +1, -k, +1 pattern, providing efficient 
distribution across the array. This structure is ideal for applications requiring balanced data 
distribution and efficient traversal.
'''
class BalancedRing:

    def __init__(self, size):
        """
        Initializes the BalancedRing object.
        Args:
            size (int): The size of the circular array.
        """
        self.size = size  # The size of the circular array.
        self.k = math.ceil(size / 2)  # Calculate k as the ceiling of size / 2.
        self.pattern = [+self.k, +1, -self.k, +1]  # The traversal step pattern.
        
        self.array = [None] * size  # Initialize the buckets.
        self.keys = {}  # Initialize the map of keys to buckets.
        self.current = 0  # Start traversal at index 0.
        self.i = 0  # Index to track the current step in the pattern.

    def insert(self, key, value):
        """
        Inserts a key-value pair into the ring in a balanced manner and updates the map.
        Args:
            key: The key to insert.
            value: The value associated with the key.
        """
        if key in self.keys:
            raise KeyError("Key already exists in the ring.")

        # Get the next index for insertion
        next = self.next()

        # Insert the key-value pair into the ring and update the map
        self.array[next] = value
        self.keys[key] = next

    def lookup(self, key):
        """
        Retrieves the value associated with a key in the ring.
        Args:
            key: The key to retrieve the value for.
        Returns:
            The value associated with the key.
        """
        if key not in self.keys:
            raise KeyError("Key not found in the ring.")

        # Get the index of the key and return the associated value
        index = self.keys[key]
        return self.array[index]

    def next(self):
        """
        Calculates the next index based on the balanced traversal rule.
        Returns:
            int: The next index.
        """
        step = self.pattern[self.i % 4]  # Determine the step based on the pattern.
        # Calculate the next index and update current
        next = (self.current + step) % self.size
        self.current = next

        self.i += 1  # Increment the step index.
        return next  # Return the new current index.

    def previous(self):
        """
        Calculates the previous index based on the balanced traversal rule.
        Returns:
            int: The previous index.
        """
        self.i -= 1  # Decrement the step index.
        step = self.pattern[(self.i) % 4]  # Determine the reverse step.
        # Calculate the previous index and update current
        prev = (self.current - step) % self.size
        self.current = prev

        return prev  # Return the new current index.

    def traverse(self, length):
        """
        Generates a traversal sequence based on the balanced traversal rule.
        Args:
            length (int): The length of the traversal sequence to generate.
        Returns:
            list: The traversal sequence.
        """
        sequence = [self.current]  # Start the sequence with the current index.

        for i in range(1, length):
            self.current = self.next()  # Calculate the next index.
            sequence.append(self.current)  # Append the index to the sequence.

        return sequence  # Return the generated sequence.
    
# Example usage
balanced_ring = BalancedRing(size=9)

# Generate a traversal sequence of specified length
traversal_sequence = balanced_ring.traverse(length=20)
print("Traversal Sequence:", traversal_sequence)

# Insert and lookup values in the circular array
balanced_ring.insert("key1", "A")
print("lookup 'key1':", balanced_ring.lookup("key1"))

# Get the next and previous indices based on the traversal pattern
print("Current Index:", balanced_ring.current)
print("Previous Index:", balanced_ring.previous())
print("Previous Index:", balanced_ring.previous())
print("Next Index:", balanced_ring.next())
print("Next Index:", balanced_ring.next())
print("Next Index:", balanced_ring.next())
