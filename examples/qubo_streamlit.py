"""
QUBO (Quadratic Unconstrained Binary Optimization) Streamlit Interface
This script provides a Streamlit interface for the QUBO example.
"""

import streamlit as st
from run_qubo_example import run_qubo_example
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Quantum QUBO Solver",
    page_icon="🔬",
    layout="wide",
)

# Add custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .result-box {
        background-color: #1a1a2e;
        border: 1px solid #00ffcc;
        border-radius: 5px;
        padding: 15px;
        margin-top: 10px;
    }
    pre {
        max-height: 500px !important;
        overflow-y: auto !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown("<h1 class='main-header'>Quantum QUBO Solver</h1>", unsafe_allow_html=True)
st.write("""
This app demonstrates solving a Quadratic Unconstrained Binary Optimization (QUBO) problem 
using both classical and quantum-inspired approaches.
""")

# Create a collapsible section for explanation
with st.expander("What is QUBO?", expanded=False):
    st.write("""
    **Quadratic Unconstrained Binary Optimization (QUBO)** is a formulation used to express 
    combinatorial optimization problems in a form that can be solved using quantum computing.
    
    The QUBO form is:
    
    Minimize: $f(x) = x^T Q x$
    
    where:
    - $x$ is a vector of binary variables (0 or 1)
    - $Q$ is a matrix of coefficients
    
    Many real-world problems can be expressed in QUBO form, including:
    - Maximum Cut
    - Graph Coloring
    - Traveling Salesman Problem
    - Portfolio Optimization
    
    In this example, we solve a simple QUBO problem: $f(x_0, x_1) = -x_0 - x_1 + 2x_0x_1$
    """)

# Run QUBO example button
st.markdown("<h2 class='section-header'>Run the QUBO Example</h2>", unsafe_allow_html=True)
st.write("Click the button below to solve the QUBO problem using both classical and quantum approaches.")

if st.button("Solve QUBO Problem", key="solve_button", type="primary"):
    with st.spinner("Running QUBO example..."):
        # Create 3 columns for displaying results
        results_container = st.container()
        
        # Run the QUBO example and get results
        with st.status("Running QUBO solver...", expanded=True) as status:
            st.write("Initializing QUBO problem...")
            results = run_qubo_example()
            st.write("Solving with classical approach...")
            st.write("Solving with quantum-inspired approach...")
            status.update(label="Computation complete!", state="complete", expanded=False)
        
        # Display QUBO problem
        results_container.markdown("<h3 class='section-header'>QUBO Problem Formulation</h3>", unsafe_allow_html=True)
        qubo_problem = results["qubo"].prettyprint()
        results_container.markdown("<div class='result-box'><pre>" + qubo_problem + "</pre></div>", unsafe_allow_html=True)
        
        # Display classical solution
        results_container.markdown("<h3 class='section-header'>Classical Solution</h3>", unsafe_allow_html=True)
        classical_result = results["classical_result"].prettyprint()
        results_container.markdown("<div class='result-box'><pre>" + classical_result + "</pre></div>", unsafe_allow_html=True)
        
        # Display quantum solution
        results_container.markdown("<h3 class='section-header'>Quantum-inspired Solution</h3>", unsafe_allow_html=True)
        quantum_result = results["quantum_result"].prettyprint()
        results_container.markdown("<div class='result-box'><pre>" + quantum_result + "</pre></div>", unsafe_allow_html=True)
        
        # Create a comparative table
        results_container.markdown("<h3 class='section-header'>Solution Comparison</h3>", unsafe_allow_html=True)
        
        # Extract data for comparison
        classical_x0 = results["classical_result"].x[0]
        classical_x1 = results["classical_result"].x[1]
        classical_fval = results["classical_result"].fval
        
        quantum_x0 = results["quantum_result"].x[0]
        quantum_x1 = results["quantum_result"].x[1]
        quantum_fval = results["quantum_result"].fval
        
        # Create comparison dataframe
        comparison_data = {
            "Method": ["Classical", "Quantum-inspired"],
            "x0": [classical_x0, quantum_x0],
            "x1": [classical_x1, quantum_x1],
            "Objective Value": [classical_fval, quantum_fval]
        }
        
        df = pd.DataFrame(comparison_data)
        results_container.table(df)
        
        # Add some interpretation
        if classical_fval == quantum_fval:
            results_container.success("Both methods found the same optimal solution!")
        else:
            results_container.warning("The methods found different solutions. The classical solution is guaranteed to be optimal.")
else:
    st.info("Click the button above to run the QUBO solver.")

# Add references section
st.markdown("<h2 class='section-header'>References</h2>", unsafe_allow_html=True)
st.write("""
- [Qiskit Optimization Documentation](https://qiskit.org/documentation/optimization/)
- [QUBO Wikipedia](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization)
- [Variational Quantum Eigensolver (VQE)](https://qiskit.org/documentation/tutorials/algorithms/04_vqe_advanced.html)
""")

# Add footer
st.markdown("---")
st.markdown("Quantum QUBO Solver App | Created with Streamlit and Qiskit")
