# Quantum Graph Coloring Solver

## Project Overview

This project implements a **quantum algorithm solution** to the **Graph Coloring Problem** using quantum amplitude amplification and superposition principles. It demonstrates how quantum computing can be applied to solve NP-complete combinatorial optimization problems.

## Problem Statement

### Classical Graph Coloring Problem
Given a graph G = (V, E) with vertices V and edges E, assign colors to vertices such that:
- No two adjacent vertices share the same color
- Minimize the number of colors used (chromatic number)

### Applications
- **Register Allocation**: Compiler optimization
- **Frequency Assignment**: Cellular network spectrum allocation
- **Scheduling**: Timetable and shift scheduling
- **Map Coloring**: Geographic region coloring
- **Sudoku Solving**: Constraint satisfaction

## Quantum Algorithm Approach

### Key Quantum Techniques

#### 1. **Amplitude Amplification**
- Generalizes Grover's algorithm
- Amplifies probability amplitudes of valid solutions
- Reduces search space from 2^n to O(√2^n)
- Implementation: Oracle + Diffusion operator iterations

#### 2. **Superposition**
- Initialize qubits in equal superposition (Hadamard gates)
- Explores all possible colorings simultaneously
- Fundamental quantum speedup mechanism

#### 3. **Quantum Oracle**
- Marks valid colorings (no adjacent same colors)
- Uses controlled operations to flip phase of valid states
- Enables amplitude amplification to work

#### 4. **Diffusion Operator**
- Inversion about average operation
- Amplifies marked states
- Constructed using Hadamard, X, and multi-controlled Z gates

## Algorithm Workflow

```
1. Initialize: Create superposition of all possible colorings
   └─ Apply H gates to all qubits
   
2. Amplitude Amplification Loop (√N iterations):
   ├─ Oracle: Mark valid colorings with phase flip
   └─ Diffusion: Amplify marked state amplitudes
   
3. Measurement: Collapse to classical coloring
   └─ Extract vertex-color assignments from bitstring
   
4. Validation: Check if coloring is valid
   └─ Return result statistics
```

## Implementation Details

### Qubit Encoding
```
Qubits per vertex = ceil(log2(num_colors))
Total qubits = num_vertices × qubits_per_vertex

Example: 5 vertices, 3 colors = 5 × 2 = 10 qubits
```

### Component Functions

| Function | Purpose |
|----------|---------|
| `_calculate_qubits()` | Determine required quantum resources |
| `_is_valid_coloring()` | Classical validation of colorings |
| `_create_oracle()` | Quantum oracle for constraint checking |
| `_create_diffusion_operator()` | Diffusion operator for amplification |
| `_amplitude_amplification()` | Main quantum algorithm implementation |
| `_extract_coloring()` | Parse measurement results |
| `execute()` | Run complete algorithm with statistics |

## Usage Example

```python
from quantum_graph_coloring import QuantumGraphColoring

# Define graph edges
edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
num_vertices = 4
num_colors = 3

# Create solver
solver = QuantumGraphColoring(edges, num_vertices, num_colors)

# Execute
result = solver.execute(shots=1024, num_iterations=2)

# Access results
print(result['best_coloring'])  # Optimal coloring
print(result['num_colors_used'])  # Chromatic number
```

## Performance Analysis

### Quantum Advantage
- **Classical**: O(k^n) where k=colors, n=vertices
- **Quantum**: O(√(k^n)) with amplitude amplification
- **Speedup**: √(k^n) times faster for large instances

### Practical Limits
- Current simulators: ~20-25 qubits practical
- NISQ devices: Limited coherence time
- Error rates: Affect solution quality

### Scalability
| Vertices | Classical | Quantum Est. | Qubits Needed |
|----------|-----------|--------------|---------------|
| 5        | O(243)    | O(15.6)      | 10            |
| 10       | O(59k)    | O(243)       | 20            |
| 15       | O(14M)    | O(3.8k)      | 30            |
| 20       | O(3.5B)   | O(59k)       | 40            |

## Project Structure

```
quantum_project/
├── requirements.txt              # Dependencies
├── PROJECT.md                   # This file
└── qss/
    ├── execute.py              # Main execution script
    └── quantum_graph_coloring.py # Core algorithm
```

## Dependencies

- **qiskit**: Quantum circuit framework
- **qiskit-aer**: Quantum simulator
- **qiskit-ibmq-provider**: IBM quantum backend access
- **numpy**: Numerical computations
- **scipy**: Scientific computing

See `requirements.txt` for complete list.

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run graph coloring solver
python qss/execute.py
```

## Expected Output

```
============================================================
QUANTUM GRAPH COLORING RESULTS
============================================================
Graph: 5 vertices, 7 edges
Colors attempted: 3
Total shots: 1024
Valid colorings found: 8

Best coloring found: (0, 1, 0, 1, 2)
Colors used: 3

All valid colorings (count):
  (0, 1, 0, 1, 2): 256 times
  (0, 1, 0, 2, 1): 128 times
  ...
============================================================
```

## Advantages Over Classical Approach

1. **Exponential Speedup**: √(k^n) times faster for large graphs
2. **Solution Verification**: Natural parallel exploration of solution space
3. **Optimization Ready**: Can be extended with cost functions
4. **Educational Value**: Demonstrates quantum computing fundamentals

## Limitations & Future Work

### Current Limitations
- Simulator-based (no real quantum hardware)
- Limited by circuit depth and qubit coherence
- Classically simulated for verification
- Scaling challenges for large graphs

### Future Enhancements
1. **Variational Approach**: Use VQE (Variational Quantum Eigensolver)
2. **QAOA**: Quantum Approximate Optimization Algorithm
3. **Hardware Optimization**: Test on real quantum devices
4. **Multi-Constraint**: Add additional graph properties
5. **Hybrid Algorithms**: Combine classical + quantum methods

## References

- Grover, L. K. (1996). "A fast quantum mechanical algorithm for database search"
- Qiskit Documentation: https://qiskit.org/documentation/
- Graph Coloring Problem: https://en.wikipedia.org/wiki/Graph_coloring
- Quantum Amplitude Amplification: Nielsen & Chuang, "Quantum Computation and Quantum Information"

## Author Notes

This project demonstrates quantum algorithm design principles applicable to various NP-complete problems. The amplitude amplification technique generalizes to constraint satisfaction, optimization, and search problems.

---

**Project Status**: Complete and Functional
**Last Updated**: 2024
**Quantum Framework**: Qiskit 0.34.2+
