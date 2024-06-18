import unittest
import random
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SelfBalancingRing import SelfBalancingRing

class TestSelfBalancingRing(unittest.TestCase):

    def setUp(self):
        initial_nodes = list(range(10))
        self.ring = SelfBalancingRing(initial_nodes, upper_bound=10, lower_bound=3)

    def test_insert_key(self):
        for i in range(100):
            self.ring.insert_key(f'key{i}')
        for node, keys in self.ring.nodes.items():
            self.assertLessEqual(len(keys), self.ring.upper_bound)
            self.assertGreaterEqual(len(keys), self.ring.lower_bound)

    def test_remove_key(self):
        for i in range(100):
            self.ring.insert_key(f'key{i}')
        for i in range(100):
            self.ring.remove_key(f'key{i}')
        self.assertEqual(len(self.ring.keys), 0)
        for keys in self.ring.nodes.values():
            self.assertEqual(len(keys), 0)

    def test_simulate_client_movement(self):
        for i in range(100):
            self.ring.insert_key(f'key{i}')
        for _ in range(50):
            key_to_move = random.choice(list(self.ring.keys.keys()))
            self.ring.remove_key(key_to_move)
            self.ring.insert_key(key_to_move)
        for node, keys in self.ring.nodes.items():
            self.assertLessEqual(len(keys), self.ring.upper_bound)
            self.assertGreaterEqual(len(keys), self.ring.lower_bound)

    def test_add_remove_nodes(self):
        for i in range(10, 15):
            self.ring.insert_node(i)
        for i in range(5):
            self.ring.remove_node(i)
        for node, keys in self.ring.nodes.items():
            self.assertLessEqual(len(keys), self.ring.upper_bound)
            self.assertGreaterEqual(len(keys), self.ring.lower_bound)

    def test_lookup_key(self):
        for i in range(100):
            self.ring.insert_key(f'key{i}')
        for i in range(100):
            node = self.ring.lookup(f'key{i}')
            self.assertIn(f'key{i}', self.ring.nodes[node])

if __name__ == '__main__':
    unittest.main()
