import math
from collections import deque

class SelfBalancingRing:
    def __init__(self, initial_nodes, upper_bound, lower_bound, variance_factor):
        """
        Initializes the SelfBalancingRing object.
        Args:
            initial_nodes (list): Initial list of nodes.
            upper_bound (int): The upper limit of keys a node can have before triggering rebalancing.
            lower_bound (int): The lower limit of keys a node can have before triggering rebalancing.
        """
        self.ring = initial_nodes or []
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.variance_factor = variance_factor
        
        self.current = 0
        self.keys = {}
        self.nodes = {node: deque() for node in self.ring}  # Map nodes to keys using deque
        self.i = 0
        self._update_k()

    def insert_node(self, node):
        """
        Inserts a node into the ring and updates the traversal pattern.
        Args:
            node (int): The node to insert.
        """
        if node in self.ring:
            raise ValueError("Node already exists in the ring.")
    
        self.ring.append(node) # Add node to ring
        self.nodes[node] = deque() # Create new queue for node
        self._update_k()  # Update k and the step pattern
        self._redistribute_to(node)

        # Debug
        print(f"Node {node} inserted. Current ring: {self.ring}")
        self.print_node_sizes()

    def remove_node(self, node):
        """
        Removes a node from the ring and updates the traversal pattern.
        Args:
            node (int): The node to remove.
        """
        if node not in self.ring:
            raise ValueError("Node not found in the ring.")

        self._redistribute_from(node) 
        self.ring.remove(node) # Remove node after redistributing
        self._update_k()  # Update k and the step pattern

        # Debug 
        print(f"Node {node} removed. Current ring: {self.ring}")
        self.print_node_sizes()

    def insert_key(self, key):
        """
        Inserts or updates a key-value pair in the ring in a balanced manner and updates the map.
        Args:
            key: The key to insert or update.
        """
        if key in self.keys:
            raise ValueError("Key already exists in the ring.")
        
        # Look for next available space
        for _ in range(len(self.ring)):
            node = self.next()
            next = self.next()
            self.previous() # Restore the step counter after getting the next

            if abs(next - node) == self.k:
                if len(self.nodes[node]) <= len(self.nodes[next]) + self.variance_factor:
                    break
                    
        if len(self.nodes[node]) >= self.upper_bound:
            # All nodes are full, add a new node and recursively try again
            new_node = max(self.ring) + 1
            self.insert_node(new_node)
            node = new_node  # Recursive call to insert the key in case something became available during search

        # Add to maps
        self.keys[key] = node
        self.nodes[node].append(key)

    def remove_key(self, key):
        """
        Removes a key from the ring and updates the map.
        Args:
            key: The key to remove.
        """
        if key not in self.keys:
            raise KeyError("Key not found in the ring.")
        
        # Locate the node, and remove from maps
        node = self.keys[key]
        del self.keys[key]
        self.nodes[node].remove(key)

        # Handle underflow
        if len(self.nodes[node]) < self.lower_bound:
            self.remove_node(node)

    def lookup(self, key):
        """
        Retrieves the value associated with a key in the ring.
        Args:
            key: The key to retrieve the value for.
        Returns:
            int: The node responsible for the key.
        """
        if key not in self.keys:
            raise KeyError("Key not found in the ring.")
        return self.keys[key]

    def remap(self, key, node):
        """
        Remaps a key to a specific node.
        Args:
            key: The key to remap.
            node: The node to map the key to.
        """
        if key in self.keys:
            old_node = self.keys[key]
            self.nodes[old_node].remove(key)
        else:
            raise KeyError("Key not found in the ring.")
        self.keys[key] = node
        self.nodes[node].append(key)
    
    def next(self):
        """
        Calculates the next index based on the balanced traversal.
        Returns:
            int: The next index.
        """
        if self.i == 0:
            self.current = 0
        else:
            step = self.pattern[self.i % 4]  # Determine the step based on the pattern
            self.current = (self.current + step) % len(self.ring)  # Calculate the next index
            
        self.i += 1  # Increment the step index
        return self.current  # Return the new current index

    def previous(self):
        """
        Calculates the previous index based on the balanced traversal rule.
        Returns:
            int: The previous index.
        """
        self.i -= 1  # Decrement the step index
        step = self.pattern[self.i % 4]  # Determine the reverse step
        self.current = (self.current - step) % len(self.ring) # Calculate the previous index
        return self.current  # Return the new current index

    def _update_k(self):
        """
        Updates the value of k based on the current number of nodes.
        """
        self.k = math.ceil(len(self.ring) / 2)  # Calculate k as the ceiling of the number of nodes / 2
        self.pattern = [+self.k, +1, -self.k, +1]  # The traversal step pattern

    def _redistribute_to(self, new_node):
        """
        Redistributes keys from existing nodes to the new node to maintain balance.
        """
        ideal = len(self.keys) // len(self.ring)
        to_move = []

        # Distribute keys from the most loaded nodes to the new node
        for node, keys in self.nodes.items():
            while len(self.nodes[new_node]) <= ideal and len(keys) > ideal and (len(to_move) < ideal):
                key = keys.popleft()  # Use popleft to follow the queue principle
                to_move.append(key)

        for key in to_move:
            self.keys[key] = node
            self.nodes[node].append(key)
        
        print(f"Node {new_node} redistributed keys. Current node sizes: {[len(self.nodes[n]) for n in self.nodes]}")

    def _redistribute_from(self, node):
        """
        Redistributes keys from a removed node to the remaining nodes.
        """
        if node not in self.nodes:
            raise ValueError("Node not found in the ring.")
        
        to_move = self.nodes[node].copy()
        del self.nodes[node]

        for key in to_move:
            node_found = False
            for n, keys in self.nodes.items():
                if len(keys) < self.upper_bound:
                    self.remap(key, n)
                    node_found = True
                    break

            if not node_found:
                # All other nodes are at the upper threshold, add a new node
                new_node = max(self.ring) + 1
                self.insert_node(new_node)

    def print_node_sizes(self):
        """
        Prints the sizes of all nodes for debugging.
        """
        print("Node sizes:")
        for node, keys in self.nodes.items():
            print(f"Node {node}: {len(keys)} keys")

