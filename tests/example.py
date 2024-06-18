import random
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SelfBalancingRing import SelfBalancingRing

# Example usage
initial_nodes = list(range(3))  # Initialize with 10 nodes
ring = SelfBalancingRing(initial_nodes, upper_bound=35, lower_bound=5, variance_factor=2)
new_key = f'key{random.randint(100, 999)}'

# Insert a large number of keys
for i in range(246):
    while new_key in ring.keys:
        new_key = f'key{random.randint(100, 999)}'  # Generate a new key
    ring.insert_key(new_key)

# Display the current ring structure and key distribution
print("Current ring structure:", ring.ring)
print("Current nodes and their keys:")
for node, keys in ring.nodes.items():
    print(f"Node {node}: {keys}")

# Simulate client movement by randomly removing and adding keys
actions = ['join', 'leave', 'move']

for _ in range(5000):  # Adjust the number of iterations for your simulation needs
    action = random.choice(actions)
    
    if action == 'join':
        new_key = f'key{random.randint(100, 999)}'
        while new_key in ring.keys:
            new_key = f'key{random.randint(100, 999)}'  # Generate a new key
        ring.insert_key(new_key)
    elif action == 'leave':
        if ring.keys:
            key_to_remove = random.choice(list(ring.keys.keys()))
            ring.remove_key(key_to_remove)
    elif action == 'move':
        if ring.keys:
            key_to_move = random.choice(list(ring.keys.keys()))
            available_nodes = [node for node in ring.nodes if len(ring.nodes[node]) < ring.upper_bound]
            current_node = ring.keys[key_to_move]
            if (current_node in available_nodes): available_nodes.remove(current_node)  # Exclude the current node
            if available_nodes:
                new_node = random.choice(available_nodes)
                ring.remap(key_to_move, new_node)

ring.print_node_sizes()

# Display the updated ring structure and key distribution
print("\nAfter simulating client movement:")
print("Current ring structure:", ring.ring)
print("Current nodes and their keys:")
for node, keys in ring.nodes.items():
    print(f"Node {node}: {keys}")

# Insert a large number of keys
for i in range(264):
    while new_key in ring.keys:
        new_key = f'key{random.randint(100, 999)}'  # Generate a new key
    ring.insert_key(new_key)

ring.print_node_sizes()
