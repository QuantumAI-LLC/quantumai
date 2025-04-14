"""
Predefined quantum circuit examples for the Quantum Circuit Simulator.
"""

# Define predefined quantum circuit examples
examples = {
    "1. Empty Circuit": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(1)
print("Empty circuit created.")
""",
    "2. Single Qubit Hadamard": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
counts = run_with_simulator(qc)
print(counts)
""",
    "3. Bell State": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
counts = run_with_simulator(qc)
print(counts)
""",
    "4. GHZ State": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure([0, 1, 2], [0, 1, 2])
counts = run_with_simulator(qc)
print(counts)
""",
    "5. Deutsch Algorithm": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 1)
qc.h([0, 1])
qc.cx(0, 1)
qc.h(0)
qc.measure(0, 0)
counts = run_with_simulator(qc)
print(counts)
""",
    "6. Quantum Teleportation": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
qc.h(1)
qc.cx(1, 2)
qc.cx(0, 1)
qc.h(0)
qc.measure([0, 1], [0, 1])
qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)
counts = run_with_simulator(qc)
print(counts)
""",
    "7. DNA Base Pair Encoding": """
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
# DNA Base Pair Encoding: A -> 00, T -> 01, G -> 10, C -> 11
qc.x(0)  # Example encoding for T (01)
qc.measure([0, 1], [0, 1])
counts = run_with_simulator(qc)
print(counts)
""",
    "8. QUBO": """
# Install the required Qiskit packages if not already installed:
# !pip install qiskit qiskit-optimization

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.primitives import Sampler
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit.utils import algorithm_globals

# For reproducibility
algorithm_globals.random_seed = 42

# Step 1: Define the QUBO
qubo = QuadraticProgram("SimpleQUBO")
qubo.binary_var('x0')
qubo.binary_var('x1')

# Objective: f(x0, x1) = -x0 - x1 + 2*x0*x1
qubo.minimize(quadratic={('x0', 'x0'): -1,
                         ('x1', 'x1'): -1,
                         ('x0', 'x1'): 2})

print("QUBO Problem:")
print(qubo.prettyprint())

# Step 2: Solve with classical solver
print("\\n--- Classical Solution ---")
exact_solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
classical_result = exact_solver.solve(qubo)
print(classical_result.prettyprint())

# Step 3: Solve with QAOA using Sampler primitive
print("\\n--- QAOA Quantum Solution ---")
qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA(maxiter=100))
quantum_solver = MinimumEigenOptimizer(qaoa)
quantum_result = quantum_solver.solve(qubo)
print(quantum_result.prettyprint())
    """,
    "9. DNA Sequence Matching with Grover's Algorithm": """
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GroverOperator
# Define the oracle circuit to mark the solution state |01>
def create_oracle():
    oracle_circuit = QuantumCircuit(2)
    oracle_circuit.cz(0, 1)  # Mark |01> as the solution
    return oracle_circuit
# Define the full Grover search circuit
def create_grover_circuit():
    oracle = create_oracle()
    grover_circuit = QuantumCircuit(2, 2)
    # Apply Hadamard to all qubits
    grover_circuit.h([0, 1])
    # Apply the oracle
    grover_circuit.append(oracle.to_gate(), [0, 1])
    # Apply Grover diffusion operator
    grover_circuit.h([0, 1])
    grover_circuit.x([0, 1])
    grover_circuit.h(1)
    grover_circuit.cz(0, 1)
    grover_circuit.h(1)
    grover_circuit.x([0, 1])
    grover_circuit.h([0, 1])
    # Measure the qubits
    grover_circuit.measure([0, 1], [0, 1])
    return grover_circuit
# Create the Grover circuit
grover_circuit = create_grover_circuit()
# Run with the simulator
counts = run_with_simulator(grover_circuit)
print(counts)
""",
    "10. Transverse Field Ising Model Hamiltonian": """
import numpy as np
from qiskit import QuantumCircuit
# from qiskit.opflow import X, Z, I # Deprecated
from qiskit.quantum_info import SparsePauliOp # Use new module
from qiskit.algorithms.minimum_eigensolvers import VQE, NumPyMinimumEigensolver # Updated import path
from qiskit.algorithms.optimizers import COBYLA
# from qiskit.utils import QuantumInstance # Deprecated and often replaced by primitives or specific simulator backends
from qiskit_aer.primitives import Estimator # Example using Aer Estimator primitive

# Number of qubits in our system
num_qubits = 4

# Define parameters for the Hamiltonian
J = 1.0  # Interaction strength
h = 0.5  # Transverse field strength

# Construct the Hamiltonian: H = -J∑(Z_i Z_{i+1}) - h∑(X_i)
# hamiltonian = 0 # Old opflow initialization

# Initialize lists for Pauli strings and coefficients
pauli_list = []
coeffs = []

# Add ZZ interaction terms (with periodic boundary)
for i in range(num_qubits):
    pauli_str = ['I'] * num_qubits
    pauli_str[i] = 'Z'
    pauli_str[(i + 1) % num_qubits] = 'Z' # Periodic boundary
    pauli_list.append("".join(pauli_str))
    coeffs.append(-J)
    # op = I # Old opflow
    # for j in range(num_qubits):
    #     if j == i:
    #         op = op ^ Z
    #     elif j == (i + 1) % num_qubits:  # Periodic boundary
    #         op = op ^ Z
    #     else:
    #         op = op ^ I
    # hamiltonian -= J * op # Old opflow

# Add X field terms
for i in range(num_qubits):
    pauli_str = ['I'] * num_qubits
    pauli_str[i] = 'X'
    pauli_list.append("".join(pauli_str))
    coeffs.append(-h)
    # op = I # Old opflow
    # for j in range(num_qubits):
    #     if j == i:
    #         op = op ^ X
    #     else:
    #         op = op ^ I
    # hamiltonian -= h * op # Old opflow

# Create the SparsePauliOp Hamiltonian
hamiltonian = SparsePauliOp(pauli_list, coeffs=coeffs)


print("TFIM Hamiltonian constructed with parameters:")
print(f"Number of qubits: {num_qubits}")
print(f"J (interaction): {J}")
print(f"h (transverse field): {h}")

# Classical solution for comparison
print("\\\\nFinding the ground state energy classically...")
numpy_solver = NumPyMinimumEigensolver()
result = numpy_solver.compute_minimum_eigenvalue(operator=hamiltonian)
print(f"Ground state energy: {result.eigenvalue.real:.6f}")

# Now set up for VQE algorithm
print("\\nSetting up VQE (Variational Quantum Eigensolver)...")

# Create a simple parameterized circuit as the ansatz
def create_ansatz(num_qubits, depth=2):
    qc = QuantumCircuit(num_qubits)
    
    # Initial state: superposition
    for i in range(num_qubits):
        qc.h(i)
    
    # Variational form
    for d in range(depth):
        # ZZ interactions
        for i in range(num_qubits):
            qc.cx(i, (i + 1) % num_qubits)
        
        # Rotation gates (parameterized)
        for i in range(num_qubits):
            qc.rx(0.1, i)  # Initial parameter value
            qc.rz(0.1, i)  # Initial parameter value
    
    return qc

# Create ansatz
ansatz = create_ansatz(num_qubits)
print(f"Created ansatz circuit with {ansatz.num_parameters} parameters")

# Demonstrating how to set up VQE
print("\\nNote: Full VQE would run hundreds of iterations to estimate the ground state.")
print("For demonstration, we're just showing the setup procedure.")

# Output the total setup summary
print("\\nITFIM Hamiltonian Simulation Summary:")
print(f"- System: {num_qubits} qubits")
print(f"- Hamiltonian: H = -J∑(Z_i Z_(i+1)) - h∑(X_i)")
print(f"- Classical ground state energy: {result.eigenvalue.real:.6f}")
"""
}
