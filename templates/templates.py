"""
Template code for creating new quantum modules.
"""

# Define application templates
templates = {
    "Basic Circuit": """
from qiskit import QuantumCircuit
# Initialize your quantum circuit here
qc = QuantumCircuit(2, 2)
# Add gates to your circuit
qc.h(0)
qc.cx(0, 1)
# Add measurements
qc.measure([0, 1], [0, 1])
# Run simulation
counts = run_with_simulator(qc)
print(counts)
""",
    "Algorithm Implementation": """
from qiskit import QuantumCircuit
# Define your quantum algorithm here
def my_algorithm(params):
    qc = QuantumCircuit(3, 3)
    # Implement algorithm steps
    qc.h(range(3))
    # Add application-specific gates
    # Add measurements
    qc.measure(range(3), range(3))
    return qc

# Run the algorithm with your parameters
circuit = my_algorithm([1.0, 0.5])
counts = run_with_simulator(circuit)
print(counts)
""",
    "Quantum Machine Learning": """
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.datasets import ad_hoc_data
import numpy as np
from utils.simulator import run_with_simulator, global_simulator # Import the simulator function and global simulator

# Generate simple dataset
num_samples = 20
X, y = ad_hoc_data(num_samples, feature_dimension=2, noise=0.1)
feature_map = ZZFeatureMap(2)
ansatz = RealAmplitudes(2, reps=1)
vqc = VQC(
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=COBYLA(maxiter=100),
    quantum_instance=global_simulator
)

# Just print the setup (full training would be too intensive)
print(f"Created VQC with {num_samples} data points")
print(f"Feature map: {feature_map.name}")
print(f"Ansatz: {ansatz.name}")
"""
}
