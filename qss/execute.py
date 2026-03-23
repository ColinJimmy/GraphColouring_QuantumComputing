import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from quantum_graph_coloring import QuantumGraphColoring

# Practical simulator budget for this project setup.
MAX_SIMULATOR_QUBITS = 24


def qubits_per_vertex(num_colors):
    """Return the qubit count needed to encode one vertex color."""
    if num_colors < 2:
        raise ValueError("num_colors must be >= 2")
    return math.ceil(math.log2(num_colors))


def max_vertices_for_colors(num_colors, max_qubits=MAX_SIMULATOR_QUBITS):
    """Compute maximum vertices that fit inside the simulator qubit budget."""
    qpv = qubits_per_vertex(num_colors)
    return max_qubits // qpv


def normalize_edges(edges, num_vertices):
    """Validate and normalize edge list to unique undirected edges."""
    normalized = set()
    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError(f"Invalid edge format: {edge}. Expected (u, v).")

        u, v = int(edge[0]), int(edge[1])
        if u == v:
            raise ValueError(f"Self-loop is not allowed: ({u}, {v})")
        if u < 0 or v < 0 or u >= num_vertices or v >= num_vertices:
            raise ValueError(
                f"Edge ({u}, {v}) is out of range for {num_vertices} vertices"
            )

        normalized.add((min(u, v), max(u, v)))

    return sorted(normalized)


def run_graph_coloring(edges, num_vertices, num_colors, shots=1024, num_iterations=2):
    """Execute graph coloring with validated runtime parameters."""
    num_vertices = int(num_vertices)
    num_colors = int(num_colors)
    shots = int(shots)
    num_iterations = int(num_iterations)

    if num_vertices < 2:
        raise ValueError("num_vertices must be >= 2")
    if num_colors < 2:
        raise ValueError("num_colors must be >= 2")
    if shots < 1:
        raise ValueError("shots must be >= 1")
    if num_iterations < 1:
        raise ValueError("num_iterations must be >= 1")

    allowed_max_vertices = max_vertices_for_colors(num_colors)
    if num_vertices > allowed_max_vertices:
        raise ValueError(
            "num_vertices exceeds simulator limit for this color count. "
            f"Given={num_vertices}, allowed={allowed_max_vertices}, "
            f"max_qubits={MAX_SIMULATOR_QUBITS}."
        )

    clean_edges = normalize_edges(edges, num_vertices)
    qgc = QuantumGraphColoring(clean_edges, num_vertices, num_colors)
    result = qgc.execute(shots=shots, num_iterations=num_iterations)

    qubits_used = num_vertices * qubits_per_vertex(num_colors)
    result["num_vertices"] = num_vertices
    result["num_edges"] = len(clean_edges)
    result["num_colors"] = num_colors
    result["qubits_used"] = qubits_used
    result["max_qubits"] = MAX_SIMULATOR_QUBITS
    result["max_vertices_for_colors"] = allowed_max_vertices

    return result


def default_stress_graph():
    """Return a 6-vertex graph suitable for 3-coloring (QAOA-friendly)."""
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),
        (3, 5),
        (2, 4),
        (1, 5),
    ]
    return edges, 6, 3


def print_result(result):
    """Pretty-print execution results for CLI usage."""
    print("=" * 60)
    print("QUANTUM GRAPH COLORING RESULTS")
    print("=" * 60)
    print(f"Graph: {result['num_vertices']} vertices, {result['num_edges']} edges")
    print(f"Colors attempted: {result['num_colors']}")
    print(
        f"Qubits used:      {result['qubits_used']} "
        f"(budget: {result['max_qubits']})"
    )
    print(f"Total shots: {result['total_shots']}")
    print(f"Valid colorings found: {result['num_valid_solutions']}")

    if result["best_coloring"]:
        print(f"\nBest coloring found: {result['best_coloring']}")
        print(f"Colors used: {result['num_colors_used']}")
        print("\nAll valid colorings (count):")
        for coloring, count in sorted(result["valid_colorings"].items()):
            print(f"  {coloring}: {count} times")
    else:
        print("No valid colorings found in this run.")
    print("=" * 60)


def main():
    """CLI entrypoint using the maximum-scale stress graph defaults."""
    edges, num_vertices, num_colors = default_stress_graph()
    result = run_graph_coloring(
        edges=edges,
        num_vertices=num_vertices,
        num_colors=num_colors,
        shots=1024,
        num_iterations=2,
    )
    print_result(result)


if __name__ == "__main__":
    main()