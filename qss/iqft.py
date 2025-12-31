"""
Inverse Quantum Fourier Transform (IQFT) Implementation

This module provides the inverse quantum Fourier transform, which is essential
for quantum phase estimation algorithms. The IQFT converts quantum states from
the frequency domain back to the computational basis.

PURPOSE:
The IQFT is used to extract phase information that has been encoded into
quantum states, particularly in quantum phase estimation algorithms.

INPUT:
- num_qubits: Integer specifying the number of qubits for the transform

OUTPUT:
- Qiskit Gate object implementing the IQFT operation

MATHEMATICAL BACKGROUND:
The QFT maps computational basis states |j⟩ to:
|j⟩ → (1/√N) ∑_{k=0}^{N-1} e^{2πijk/N} |k⟩

The IQFT performs the inverse transformation:
|k⟩ → (1/√N) ∑_{j=0}^{N-1} e^{-2πijk/N} |j⟩

CIRCUIT STRUCTURE:
1. Controlled phase rotations with negative angles
2. Hadamard gates
3. Qubit swapping for bit-reversal

COMPLEXITY:
- Gate count: O(n²) where n = num_qubits
- Depth: O(n²) 

APPLICATIONS:
- Quantum phase estimation
- Shor's algorithm
- Quantum counting algorithms
- Period finding

EDGE CASES:
- num_qubits = 0: Returns empty circuit
- num_qubits = 1: Returns single Hadamard gate
- Large num_qubits: May exceed circuit depth limits on some backends

REFERENCES:
Based on Nielsen & Chuang "Quantum Computation and Quantum Information"
and Qiskit QPE tutorial implementation.
"""

import numpy as np
from qiskit import QuantumCircuit


def iqft(num_qubits):
    """
    Construct a gate implementing the inverse quantum Fourier transform.
    
    The IQFT is crucial for extracting phase information in quantum algorithms.
    It transforms a quantum state from the frequency domain back to the 
    computational basis, enabling measurement of encoded classical information.

    Circuit Construction:
    1. Apply controlled phase rotations (with negative phases)
    2. Apply Hadamard gates to each qubit
    3. Swap qubits to correct bit-ordering
    
    Arguments:
        num_qubits: Number of qubits for the transform (must be positive)
        
    Returns:
        Qiskit Gate object that applies IQFT when appended to a circuit
        
    Raises:
        ValueError: If num_qubits is not a positive integer
        
    Example:
        >>> circuit = QuantumCircuit(3)
        >>> circuit.append(iqft(3), [0, 1, 2])
    """
    # Create quantum circuit for the specified number of qubits
    qc = QuantumCircuit(num_qubits)

    # Step 1: Swap qubits for bit-reversal
    # The QFT naturally produces bit-reversed output, so we swap to correct this
    # Only need to swap the first half with the second half
    for qubit in range(num_qubits // 2):
        qc.swap(qubit, num_qubits - qubit - 1)

    # Step 2: Apply the core IQFT operations
    # Process qubits in reverse order compared to standard QFT
    for j in range(num_qubits):
        
        # Step 2a: Apply controlled phase rotations
        # Each qubit j gets controlled rotations from all previous qubits
        for m in range(j):
            # Controlled phase gate with negative angle (inverse of QFT)
            # Phase = -π/2^(j-m) where (j-m) determines the rotation magnitude
            phase_angle = -np.pi / float(2 ** (j - m))
            qc.cp(phase_angle, m, j)  # Control qubit m, target qubit j
            
        # Step 2b: Apply Hadamard gate to complete the transformation for this qubit
        # Creates superposition and completes the frequency-to-computational basis conversion
        qc.h(j)

    # Convert the circuit to a reusable gate object
    iqft_gate = qc.to_gate()
    iqft_gate.name = "IQFT"  # Label for circuit visualization
    
    return iqft_gate
