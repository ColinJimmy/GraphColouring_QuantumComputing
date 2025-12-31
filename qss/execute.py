import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from quantum_graph_coloring import QuantumGraphColoring

# Define a sample graph (edges represent vertices that must have different colors)
# Example: A graph with 5 vertices and various edges
edges = [
    (0, 1), (0, 2),
    (1, 2), (1, 3),
    (2, 3), (2, 4),
    (3, 4)
]

num_vertices = 5
num_colors = 3

# Create and execute quantum graph coloring solver
qgc = QuantumGraphColoring(edges, num_vertices, num_colors)
result = qgc.execute(shots=1024, num_iterations=2)

print("=" * 60)
print("QUANTUM GRAPH COLORING RESULTS")
print("=" * 60)
print(f"Graph: {num_vertices} vertices, {len(edges)} edges")
print(f"Colors attempted: {num_colors}")
print(f"Total shots: {result['total_shots']}")
print(f"Valid colorings found: {result['num_valid_solutions']}")

if result['best_coloring']:
    print(f"\nBest coloring found: {result['best_coloring']}")
    print(f"Colors used: {result['num_colors_used']}")
    print(f"\nAll valid colorings (count):")
    for coloring, count in sorted(result['valid_colorings'].items()):
        print(f"  {coloring}: {count} times")
else:
    print("No valid colorings found in this run.")
print("=" * 60)