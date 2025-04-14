#!/usr/bin/env python3
"""
Debug script to test Qiskit 2.0 compatibility
"""

import sys

def main():
    print("=== Qiskit 2.0 Debug Script ===")
    
    try:
        import qiskit
        print(f"Qiskit version: {qiskit.__version__}")
        
        print("\nTesting imports...")
        from qiskit import QuantumCircuit
        print("✓ Imported QuantumCircuit")
        
        from qiskit.primitives import SamplerV1
        print("✓ Imported SamplerV1")
        
        from qiskit.utils import algorithm_globals
        print("✓ Imported algorithm_globals")
        
        # Create a basic circuit
        print("\nCreating a simple quantum circuit...")
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.h(1)
        circuit.cx(0, 1)
        circuit.measure_all()
        print(circuit)
        
        # Run with SamplerV1
        print("\nRunning circuit with SamplerV1...")
        sampler = SamplerV1()
        job = sampler.run(circuit, shots=1000)
        result = job.result()
        print("Results:")
        print(result.quasi_dists[0])
        
        print("\nAll tests passed successfully!")
        return 0
        
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
