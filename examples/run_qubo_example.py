"""
QUBO (Quadratic Unconstrained Binary Optimization) Example Runner
This script runs the QUBO example separately from the main Streamlit application.
"""

# Install the required Qiskit packages if not already installed:
# !pip install qiskit qiskit-optimization

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
import numpy as np
from qiskit.utils import algorithm_globals
from qiskit.quantum_info import SparsePauliOp

# For compatibility with newer Qiskit versions
import importlib
from packaging import version
import qiskit

# Import appropriate components based on Qiskit version
try:
    # Try newer Qiskit version approach first
    from qiskit.primitives import Sampler
    from qiskit_algorithms.minimum_eigensolvers import NumPyMinimumEigensolver, VQE
except ImportError:
    try:
        # For intermediate Qiskit versions
        from qiskit.primitives import BaseSamplerV1 as BaseSampler
        from qiskit_algorithms.minimum_eigensolvers import NumPyMinimumEigensolver, VQE
    except ImportError:
        # Fall back to older Qiskit versions
        from qiskit.algorithms import NumPyMinimumEigensolver, VQE
        from qiskit import Aer

def run_qubo_example():
    """
    Runs the QUBO example and returns the results.
    """
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
    print("\n--- Classical Solution ---")
    exact_solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    classical_result = exact_solver.solve(qubo)
    print(classical_result.prettyprint())

    # Step 3: Solve with custom sampling minimum eigensolver
    print("\n--- Quantum-inspired Solution ---")
    
    # Create a VQE-based solver that works with current Qiskit version
    ansatz = TwoLocal(2, 'ry', 'cz', reps=1, entanglement='full')
    optimizer = COBYLA(maxiter=100)
    
    # Create a VQE solver compatible with installed Qiskit version
    try:
        # Try newer Qiskit approach first (0.40.0+)
        sampler = Sampler()
        vqe = VQE(
            ansatz=ansatz,
            optimizer=optimizer,
            sampler=sampler
        )
    except (ImportError, TypeError, AttributeError):
        try:
            # For intermediate versions
            from qiskit import Aer
            backend = Aer.get_backend('statevector_simulator')
            vqe = VQE(
                ansatz=ansatz,
                optimizer=optimizer,
                quantum_instance=backend
            )
        except (ImportError, TypeError):
            # For older versions
            from qiskit import Aer
            backend = Aer.get_backend('statevector_simulator')
            vqe = VQE(
                ansatz=ansatz,
                optimizer=optimizer,
                quantum_instance=backend
            )
    
    quantum_solver = MinimumEigenOptimizer(vqe)
    quantum_result = quantum_solver.solve(qubo)
    print(quantum_result.prettyprint())
    
    return {
        "qubo": qubo,
        "classical_result": classical_result,
        "quantum_result": quantum_result
    }

if __name__ == "__main__":
    # If this script is run directly, execute the QUBO example
    print("Running QUBO Example...")
    results = run_qubo_example()
    print("\nExecution complete!")
