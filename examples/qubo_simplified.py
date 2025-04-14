"""
Simplified QUBO (Quadratic Unconstrained Binary Optimization) Example for Qiskit 2.0
This script provides a simplified implementation of the QUBO example that works with Qiskit 2.0.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import SamplerV1
from qiskit.utils import algorithm_globals
from qiskit.quantum_info import SparsePauliOp

def create_qubo_matrix():
    """
    Create a simple 2-variable QUBO problem.
    The objective function is: f(x0, x1) = -x0 - x1 + 2*x0*x1
    """
    # Create the QUBO matrix (upper triangular form)
    qubo_matrix = np.array([[-1, 2], 
                            [0, -1]])
    return qubo_matrix

def solve_classically(qubo_matrix):
    """
    Solve the QUBO problem by enumeration (classical brute-force).
    """
    n = qubo_matrix.shape[0]
    min_value = float('inf')
    min_state = None
    
    # Try all possible binary strings
    for i in range(2**n):
        # Convert i to a binary state vector
        state = [int(bit) for bit in format(i, f'0{n}b')]
        
        # Calculate the objective value
        value = 0
        for j in range(n):
            for k in range(n):
                value += qubo_matrix[j, k] * state[j] * state[k]
        
        if value < min_value:
            min_value = value
            min_state = state
    
    return {"min_value": min_value, "min_state": min_state}

def qubo_to_ising(qubo_matrix):
    """
    Convert QUBO to Ising Hamiltonian (for quantum computing)
    """
    n = qubo_matrix.shape[0]
    
    # Initialize Ising parameters
    h = np.zeros(n)
    J = np.zeros((n, n))
    
    # Calculate offset
    offset = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                offset += qubo_matrix[i, j] / 4
            else:
                offset += qubo_matrix[i, j] / 8
    
    # Calculate h values
    for i in range(n):
        h[i] = qubo_matrix[i, i] / 2
        for j in range(n):
            if i != j:
                h[i] += qubo_matrix[i, j] / 4
    
    # Calculate J values
    for i in range(n):
        for j in range(i+1, n):
            J[i, j] = qubo_matrix[i, j] / 4
    
    return h, J, offset

def create_hamiltonian(h, J):
    """
    Create a Hamiltonian operator from h and J values
    """
    n = len(h)
    hamiltonian_terms = []
    
    # Add Z terms (h values)
    for i in range(n):
        if h[i] != 0:
            # Create a Pauli Z operator for qubit i
            pauli_str = 'I' * i + 'Z' + 'I' * (n-i-1)
            hamiltonian_terms.append((pauli_str, h[i]))
    
    # Add ZZ terms (J values)
    for i in range(n):
        for j in range(i+1, n):
            if J[i, j] != 0:
                # Create a Pauli ZZ operator for qubits i and j
                pauli_str = ['I'] * n
                pauli_str[i] = 'Z'
                pauli_str[j] = 'Z'
                pauli_str = ''.join(pauli_str)
                hamiltonian_terms.append((pauli_str, J[i, j]))
    
    # Convert to SparsePauliOp
    hamiltonian_op = SparsePauliOp.from_list(hamiltonian_terms)
    return hamiltonian_op

def create_simple_quantum_circuit(n_qubits):
    """
    Create a simple parameterized quantum circuit for the QUBO problem
    """
    circuit = QuantumCircuit(n_qubits)
    
    # Apply Hadamard gates to create superposition
    for i in range(n_qubits):
        circuit.h(i)
    
    # Add some parameterized rotation gates
    for i in range(n_qubits):
        circuit.rx(np.pi/4, i)
    
    # Add some entanglement
    for i in range(n_qubits-1):
        circuit.cx(i, i+1)
    
    # Add final mixing layer
    for i in range(n_qubits):
        circuit.h(i)
        
    return circuit

def simulate_circuit(circuit, shots=1000):
    """
    Simulate the quantum circuit using Qiskit's SamplerV1
    """
    sampler = SamplerV1()
    job = sampler.run(circuit, shots=shots)
    result = job.result()
    
    # Extract and return the distribution
    return result.quasi_dists[0]

def run_qubo_example():
    """
    Runs the simplified QUBO example and returns the results.
    """
    # Set random seed for reproducibility
    algorithm_globals.random_seed = 42
    
    # Define the QUBO problem
    qubo_matrix = create_qubo_matrix()
    print("QUBO Matrix:")
    print(qubo_matrix)
    
    # Solve classically first
    print("\n--- Classical Solution ---")
    classical_result = solve_classically(qubo_matrix)
    print(f"Minimum value: {classical_result['min_value']}")
    print(f"Optimal state: {classical_result['min_state']}")
    
    # Convert to Ising model
    h, J, offset = qubo_to_ising(qubo_matrix)
    print("\n--- Ising Model Parameters ---")
    print(f"h values: {h}")
    print(f"J values: {J}")
    print(f"Constant offset: {offset}")
    
    # Create Hamiltonian
    hamiltonian = create_hamiltonian(h, J)
    print("\nHamiltonian:")
    print(hamiltonian)
    
    # Create a quantum circuit
    print("\n--- Quantum Approach ---")
    circuit = create_simple_quantum_circuit(len(h))
    print("Quantum Circuit:")
    print(circuit)
    
    # Simulate the circuit
    distribution = simulate_circuit(circuit)
    print("\nMeasurement Results:")
    for state, prob in sorted(distribution.items(), key=lambda x: -x[1]):
        binary = format(state, f'0{len(h)}b')
        print(f"State |{binary}⟩: probability = {prob:.4f}")
    
    # Find the state with highest probability
    most_probable_state = max(distribution.items(), key=lambda x: x[1])[0]
    binary_result = [int(bit) for bit in format(most_probable_state, f'0{len(h)}b')]
    
    print("\n--- Quantum-inspired Solution ---")
    print(f"Most probable state: {binary_result}")
    
    # Calculate the corresponding objective value
    quantum_value = 0
    for i in range(len(h)):
        for j in range(len(h)):
            quantum_value += qubo_matrix[i, j] * binary_result[i] * binary_result[j]
    
    print(f"Corresponding objective value: {quantum_value}")
    
    return {
        "qubo_matrix": qubo_matrix,
        "classical_result": classical_result,
        "quantum_result": {
            "state": binary_result,
            "value": quantum_value
        }
    }

if __name__ == "__main__":
    print("Running Simplified QUBO Example with Qiskit 2.0...")
    results = run_qubo_example()
    print("\nExecution complete!")
