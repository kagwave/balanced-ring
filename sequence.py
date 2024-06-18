import math

"""
A closer look at the traversal sequence.

Attributes:
    n (int): The number of nodes, or size of the circular array.
    k (int): Approximately half the size of the circular array, used in traversal steps.
    i (int): Internal counter to keep track of the current step in the traversal pattern.
    current (int): The current position in the traversal.
    sequence (list): The generated sequence or traversal order.
    num_visits (map): A map tracking the number of times each node has been visited (for simulation purposes).

Methods:
    __init__(self, n): Initializes the BalancedSequence instance with the size of the circular array.
    next(self): Gets the next node in the traversal sequence.
    generate(self, length): Runs the traversal up to a specified length.
"""
class Sequence:

    def __init__(self, n):
        # n, number of nodes, or size of the circular array.
        self.n = n
        # k, approximately half the size of the circular array.
        self.k = math.ceil(n / 2)
        # Internal step counter
        self.i = 0
        # Current number in the sequence, or index of the circular array.
        self.current = 0
        # The generated sequence, or traversal order.
        self.sequence = []
        # Number of times each node has been visited.
        self.num_visits = {i: 0 for i in range(n)}
    
    def generate(self, length):
        # Reset any previous sequence and visits
        self.i = 0
        self.current = 0
        self.sequence = []
        self.num_visits = {i: 0 for i in range(self.n)}

        for _ in range(length):
            next = self.next()
            # Update the sequence.
            self.sequence.append(next)
            self.num_visits[next] = self.num_visits.get(next, 0) + 1

        return self.sequence, self.num_visits

    def next(self):
        if self.i == 0:
            # Start with 0
            next = 0
        else:
            """
            (+k, +1, -k, +1) pattern.
                Gets the next index of the circular array.
            """
            if self.i % 4 == 1:
                next = self.current + self.k
            elif self.i % 4 == 2:
                next = self.current + 1
            elif self.i % 4 == 3:
                next = self.current - self.k
            elif self.i % 4 == 0:
                next = self.current + 1

        # Keep the index within the circular array.
        next = next % self.n

        # Update current
        self.current = next

        # Increment step counter
        self.i += 1

        return next

    """
    This function takes a segment of the sequence, preferrably of length n, 
    and reflects each element around the midpoint (n-1)/2, and then reverses 
    the order of the elements. This function is an involution that when done
    once, provides a later segment of the sequence.

    Args:
        segment (list of int): The segment of the permutation to be transformed.
        n (int): The size of the full permutation (number of nodes in the ring).

    Returns:
        list of int: The transformed segment.
    """
    def reflect_and_reverse(permutation, n):
        return reverse(reflect(permutation, n))

    
def reverse(permutation):
    return permutation[::-1]

def reflect(permutation, n):
    return [(n - 1) - v for v in permutation]

# Usage
s = Sequence(17)
# Runs the traversal for a fixed length
sequence, num_visits = s.generate(178)

print("Sequence:", sequence)
print("Number of visits:", num_visits)
print("Next node:", s.next())
