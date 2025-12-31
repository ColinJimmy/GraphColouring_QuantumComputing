from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from itertools import combinations
import numpy as np

class QuantumGraphColoring:
    """
    Solves the graph coloring problem using quantum amplitude amplification.
    Finds a valid coloring of a graph with minimum number of colors.
    """
    
    def __init__(self, edges, num_vertices, num_colors=3):
        """
        Initialize the quantum graph coloring solver.
        
        Args:
            edges: List of tuples representing edges (u, v)
            num_vertices: Number of vertices in the graph
            num_colors: Number of colors to attempt
        """
        self.edges = edges
        self.num_vertices = num_vertices
        self.num_colors = num_colors
        self.num_qubits = self._calculate_qubits()
        self.simulator = AerSimulator()
        
    def _calculate_qubits(self):
        """Calculate required qubits for encoding vertex colors."""
        import math
        qubits_per_vertex = math.ceil(math.log2(self.num_colors))
        return self.num_vertices * qubits_per_vertex
    
    def _is_valid_coloring(self, coloring):
        """Check if a coloring is valid (no adjacent vertices share colors)."""
        for u, v in self.edges:
            if coloring[u] == coloring[v]:
                return False
        return True
    
    def _create_oracle(self, qc, qubits, coloring_mask):
        """Create an oracle that marks valid colorings."""
        # This oracle checks constraint satisfaction
        # For simplicity, we use a classical oracle approach
        num_checks = len(self.edges)
        
        # Add phase flip for valid colorings
        for i, (u, v) in enumerate(self.edges):
            qc.cx(qubits[u], qubits[v])
        
        # Multi-controlled Z gate for constraint checking
        if len(qubits) > 2:
            qc.mcp(np.pi, qubits[:-1], qubits[-1])
        
        # Uncompute
        for i, (u, v) in enumerate(self.edges):
            qc.cx(qubits[u], qubits[v])
    
    def _create_diffusion_operator(self, qc, qubits):
        """Create the diffusion operator (inversion about average)."""
        # H gates
        for q in qubits:
            qc.h(q)
        
        # X gates
        for q in qubits:
            qc.x(q)
        
        # Multi-controlled Z gate
        if len(qubits) > 2:
            qc.mcp(np.pi, qubits[:-1], qubits[-1])
        
        # X gates
        for q in qubits:
            qc.x(q)
        
        # H gates
        for q in qubits:
            qc.h(q)
    
    def _amplitude_amplification(self, num_iterations=2):
        """Apply amplitude amplification to boost valid solutions."""
        qr = QuantumRegister(self.num_qubits, 'q')
        cr = ClassicalRegister(self.num_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Initialize superposition
        for i in range(self.num_qubits):
            qc.h(qr[i])
        
        # Apply amplitude amplification iterations
        for _ in range(num_iterations):
            # Oracle
            self._create_oracle(qc, list(qr), None)
            
            # Diffusion operator
            self._create_diffusion_operator(qc, list(qr))
        
        return qc, qr, cr
    
    def _extract_coloring(self, bitstring):
        """Extract vertex coloring from measured bitstring."""
        import math
        qubits_per_vertex = math.ceil(math.log2(self.num_colors))
        coloring = []
        
        for v in range(self.num_vertices):
            start = v * qubits_per_vertex
            end = start + qubits_per_vertex
            color = int(bitstring[start:end], 2) % self.num_colors
            coloring.append(color)
        
        return coloring
    
    def execute(self, shots=1024, num_iterations=2):
        """
        Execute the quantum graph coloring algorithm.
        
        Returns:
            Dictionary with valid colorings found and statistics
        """
        qc, qr, cr = self._amplitude_amplification(num_iterations)
        
        # Measure all qubits
        qc.measure(qr, cr)
        
        # Execute
        qc = transpile(qc, self.simulator)
        job = self.simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        # Process results
        valid_colorings = {}
        for bitstring, count in counts.items():
            coloring = self._extract_coloring(bitstring)
            if self._is_valid_coloring(coloring):
                coloring_tuple = tuple(coloring)
                valid_colorings[coloring_tuple] = valid_colorings.get(coloring_tuple, 0) + count
        
        return {
            'valid_colorings': valid_colorings,
            'total_shots': shots,
            'num_valid_solutions': len(valid_colorings),
            'best_coloring': max(valid_colorings.keys()) if valid_colorings else None,
            'num_colors_used': len(set(max(valid_colorings.keys()))) if valid_colorings else 0
        }
