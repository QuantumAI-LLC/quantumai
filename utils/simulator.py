"""
Quantum simulator utilities for the Quantum Circuit Simulator.
"""
from qiskit import transpile
from qiskit_aer import AerSimulator
import json
import os
import streamlit as st

# Create a global AerSimulator instance that can be used by all examples
global_simulator = AerSimulator()

def run_with_simulator(circuit, shots=1024):
    """
    Run a quantum circuit using the global AerSimulator
    
    Args:
        circuit (QuantumCircuit): The quantum circuit to simulate
        shots (int): Number of repetitions of each experiment
        
    Returns:
        dict: Measurement counts from the simulation
    """
    # Transpile the circuit for the AerSimulator
    transpiled_circuit = transpile(circuit, global_simulator)

    # Run the simulation
    result = global_simulator.run(transpiled_circuit, shots=shots).result()

    # Get the counts (measurement results)
    return result.get_counts()

# Function to load saved user applications
def load_user_applications():
    """Load user-defined applications from the save file"""
    try:
        if os.path.exists("user_applications.json"):
            with open("user_applications.json", "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading user applications: {e}")
        return {}

# Function to save user applications
def save_user_applications(user_apps):
    """Save user-defined applications to a file"""
    try:
        with open("user_applications.json", "w") as f:
            json.dump(user_apps, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving user applications: {e}")
        return False

# Add a sidebar for user interaction
st.sidebar.title("Quantum Circuit Simulator Sidebar")

# File uploader for quantum circuits
uploaded_file = st.sidebar.file_uploader("Upload a Quantum Circuit (QASM format)", type=["qasm"])
if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!")
    # Placeholder for processing the uploaded file
    st.write("Uploaded file content:")
    st.code(uploaded_file.getvalue().decode("utf-8"))

# Settings configuration
shots = st.sidebar.number_input("Number of Shots", min_value=1, max_value=10000, value=1024)
st.sidebar.write(f"Current shots: {shots}")
