"""
Minimal QUBO Example for Qiskit with optimization package
"""

import sys
import traceback

def main():
    try:
        print("Starting minimal QUBO example...")
        
        # Install the required Qiskit packages if not already installed:
        # !pip install qiskit qiskit-optimization
        
        # Import Qiskit optimization components
        print("Importing Qiskit components...")
        from qiskit_optimization import QuadraticProgram
        from qiskit_optimization.algorithms import MinimumEigenOptimizer
        from qiskit.algorithms import QAOA
        from qiskit.primitives import Sampler
        from qiskit.algorithms.optimizers import COBYLA
        from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
        from qiskit.utils import algorithm_globals
        
        # For reproducibility
        algorithm_globals.random_seed = 42
        
        print("# Step 1: Define the QUBO")
        qubo = QuadraticProgram("SimpleQUBO")
        qubo.binary_var('x0')
        qubo.binary_var('x1')
        
        # Objective: f(x0, x1) = -x0 - x1 + 2*x0*x1
        qubo.minimize(quadratic={(0, 0): -1, (1, 1): -1, (0, 1): 2})
        
        print("QUBO problem formulated:")
        print(qubo.export_as_lp_string())
        
        print("\n# Step 2: Solve with NumPy minimum eigensolver (classical)")
        numpy_solver = NumPyMinimumEigensolver()
        optimizer = MinimumEigenOptimizer(numpy_solver)
        result = optimizer.solve(qubo)
        
        print("Results from classical solver:")
        print(f"x0 = {result.x[0]}, x1 = {result.x[1]}")
        print(f"Objective value: {result.fval}")
        
        print("\n# Step 3: Solve with QAOA (quantum)")
        qaoa = QAOA(sampler=Sampler(), optimizer=COBYLA())
        optimizer = MinimumEigenOptimizer(qaoa)
        result_qaoa = optimizer.solve(qubo)
        
        print("Results from QAOA solver:")
        print(f"x0 = {result_qaoa.x[0]}, x1 = {result_qaoa.x[1]}")
        print(f"Objective value: {result_qaoa.fval}")
        
        print("Execution complete!")
        return True
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"Script completed {'successfully' if success else 'with errors'}")
