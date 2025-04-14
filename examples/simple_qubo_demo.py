"""
Simple QUBO (Quadratic Unconstrained Binary Optimization) Demonstrator

This script demonstrates a simple QUBO problem and solves it using brute force,
avoiding the complex Qiskit dependencies that might cause version compatibility issues.
"""

import numpy as np
from itertools import product

def solve_qubo_brute_force(Q, constant=0.0):
    """
    Solve a QUBO problem using brute force enumeration.
    
    Args:
        Q (dict): Dictionary with (i,j) tuples as keys and coefficients as values
        constant (float): Constant term in the objective function
        
    Returns:
        tuple: (optimal_x, optimal_value)
    """
    # Determine the number of variables
    variables = set()
    for i, j in Q.keys():
        variables.add(i)
        variables.add(j)
    n = max(variables) + 1
    
    # Evaluate all possible binary combinations
    best_value = float('inf')
    best_x = None
    
    for x in product([0, 1], repeat=n):
        value = constant
        for (i, j), coeff in Q.items():
            value += coeff * x[i] * x[j]
        
        if value < best_value:
            best_value = value
            best_x = x
    
    return best_x, best_value

def run_simple_qubo_example():
    """
    Run a simple QUBO example without Qiskit dependencies.
    """
    print("Running Simple QUBO Example...")
    
    # Define the same QUBO problem as in the original script
    # f(x0, x1) = -x0 - x1 + 2*x0*x1
    Q = {(0, 0): -1, (1, 1): -1, (0, 1): 2}
    
    print("\nQUBO Problem:")
    print("Minimize: f(x0, x1) = -x0 - x1 + 2*x0*x1")
    
    # Solve using brute force
    solution, value = solve_qubo_brute_force(Q)
    
    print("\n--- Solution ---")
    print(f"Optimal solution: x = {solution}")
    print(f"Optimal value: f(x) = {value}")
    
    # Explanation
    print("\n--- Explanation ---")
    print("For this simple QUBO problem:")
    print("  f(0,0) = 0")
    print("  f(0,1) = -1")
    print("  f(1,0) = -1")
    print("  f(1,1) = -1-1+2 = 0")
    print(f"Therefore, the minimum is {value} achieved at x = {solution}")
    
    return {"solution": solution, "value": value}

if __name__ == "__main__":
    results = run_simple_qubo_example()
    print("\nExecution complete!")
