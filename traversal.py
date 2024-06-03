import math

"""
A closer look at the balanced traversal sequence, requiring a static environment with a predetermined number of nodes.

Attributes:
    n (int): The number of nodes, or size of the circular array.
    k (int): Approximately half the size of the circular array, used in traversal steps.
    i (int): Internal counter to keep track of the current step in the traversal pattern.
    current (int): The current position in the traversal.
    sequence (list): The generated sequence or traversal order.
    num_visits (map): A map tracking the number of times each node has been visited (for simulation purposes).

Methods:
    __init__(self, n): Initializes the BalancedTraversal instance with the size of the circular array.
    next(self): Gets the next node in the traversal sequence.
    generate(self, length): Runs the traversal up to a specified length.
"""
class Traversal:

    def __init__(self, n):
        # n, number of nodes, or size of the circular array.
        self.n = n
        # k, approximately half the size of the circular array.
        self.k = math.ceil(n / 2)
        # Number of times each node has been visited.
        self.num_visits = {i: 0 for i in range(n)}
        # Current number in the sequence, or index of the circular array.
        self.current = 0
        # The generated sequence, or traversal order.
        self.sequence = []
        # Internal step counter
        self.i = 0

    def next(self):
        if self.i == 0:
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

        # Update the sequence.
        self.sequence.append(next)
        self.num_visits[next] = self.num_visits.get(next, 0) + 1
        self.current = next

        # Increment step counter
        self.i += 1

        return next

    def generate(self, length):
        # Reset any previous sequence and visits
        self.sequence = []
        self.num_visits = {i: 0 for i in range(self.n)}
        self.current = 0
        self.i = 0

        for _ in range(length):
            self.next()

        return self.sequence, self.num_visits

# Usage
t = Traversal(9)
# Runs the traversal for a fixed length
sequence, num_visits = t.generate(77)
print("Sequence:", sequence)
print("Number of visits:", num_visits)
# Get the next node in the sequence
next = t.next()
print("Next node:", next)
