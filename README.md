# Quantum Graph Coloring

This repository implements a quantum approach to the graph coloring problem:

<i>Given a graph with vertices \(V\) and edges \(E\), assign one of \(k\) colors to each vertex so that no two adjacent vertices share the same color.</i>

The code leverages amplitude amplification (Grover-style) to boost valid colorings within a superposition of candidate assignments.

## Installation

After cloning the repository and navigating into the resulting directory, install locally:

`pip install .`

Import the module:

`import qss`

## Execution

Example usage:

```
import qss

# Edges where each tuple connects two adjacent vertices
edges = [
    (0, 1), (0, 2),
    (1, 2), (1, 3),
    (2, 3), (2, 4),
    (3, 4)
]

num_vertices = 5
num_colors = 3

q = qss.QuantumGraphColoring(edges, num_vertices, num_colors)
result = q.execute(shots=1024, num_iterations=2)
print(result)
```

Example output (valid colorings with their counts):

```
{
  'valid_colorings': {(0, 1, 2, 0, 1): 57, (1, 2, 0, 1, 2): 41},
  'total_shots': 1024,
  'num_valid_solutions': 2,
  'best_coloring': (1, 2, 0, 1, 2),
  'num_colors_used': 3
}
```

Raw measurement counts (bitstrings to frequencies) can still be inspected via the backend result for deeper analysis.

## Experimental Results

### Classical Simulation

Running the above example on a simulator yields a distribution with peaks at bitstrings encoding valid colorings. Each contiguous block of qubits maps to a vertex color in binary; peaks correspond to assignments where adjacent vertices differ.

### IBM Quantum Computers

The same circuit can be executed on IBM Quantum hardware, subject to qubit availability and connectivity constraints. Smaller graphs fit current public devices; larger instances require more qubits or transpilation-aware layout choices.

## Tests

Run unit tests with:

`python -m unittest qss/test_quantum_graph_coloring.py`

## References

* Boyer, Brassard, Høyer, Tapp. "Tight bounds on quantum searching." (1998).
* Qiskit.org. Grover's Algorithm. <https://qiskit.org/textbook/ch-algorithms/grover.html>
* Qiskit.org. Phase Kickback. <https://qiskit.org/textbook/ch-gates/phase-kickback.html>
* Qiskit.org. Quantum Fourier Transform. <https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html>
* Qiskit.org. Quantum Phase Estimation. <https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html>

