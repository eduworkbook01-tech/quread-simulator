import numpy as np

class QuantumCircuit:
    def __init__(self):
        # 2 Qubits means 2^2 = 4 possible states: |00>, |01>, |10>, |11>
        # We initialize to |00> (the first position is 1)
        self.state = np.zeros(4, dtype=complex)
        self.state[0] = 1.0

    def apply_gate(self, gate_name, target_qubit):
        """
        This is the hardest part of Quantum Simulators!
        We have to scale a small 2x2 gate up to a 4x4 matrix using the Kronecker Product.
        """
        
        # Define 2x2 Basic Gates
        X = np.array([[0, 1], [1, 0]])
        H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        I = np.eye(2) # Identity (Do nothing)
        
        # Select the matrix based on name
        if gate_name == "X":
            matrix = X
        elif gate_name == "H":
            matrix = H
        
        # BUILD THE 4x4 OPERATOR
        # If we apply gate to Qubit 0:  Gate (tensor) Identity
        # If we apply gate to Qubit 1:  Identity (tensor) Gate
        if target_qubit == 0:
            # np.kron is the "Kronecker Product"
            full_operator = np.kron(matrix, I)
        else:
            full_operator = np.kron(I, matrix)
            
        # Update the state
        self.state = np.dot(full_operator, self.state)

    def apply_cnot(self):
        """
        The CNOT Gate: Flips Qubit 1 ONLY IF Qubit 0 is |1>
        Matrix:
        1 0 0 0
        0 1 0 0
        0 0 0 1
        0 0 1 0
        """
        CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])
        self.state = np.dot(CNOT, self.state)

    def measure(self):
        probabilities = np.abs(self.state) ** 2
        probabilities /= np.sum(probabilities) # Normalize
        return probabilities
    def collapse(self):
        """
        Simulates the act of measurement. 
        1. Calculate probabilities.
        2. Roll the dice to pick a winner.
        3. FORCE the vector to become that winner (100%).
        """
        # 1. Get probabilities
        probabilities = np.abs(self.state) ** 2
        probabilities /= np.sum(probabilities) # Safety normalize
        
        # 2. Pick a state (0, 1, 2, or 3) based on those probs
        outcome_index = np.random.choice([0, 1, 2, 3], p=probabilities)
        
        # 3. COLLAPSE THE WAVEFUNCTION
        # Reset entire vector to 0
        self.state = np.zeros(4, dtype=complex)
        # Set the winner to 1.0
        self.state[outcome_index] = 1.0
        
        # Return the binary string (e.g., "00", "01")
        binary_map = {0: "00", 1: "01", 2: "10", 3: "11"}
        return binary_map[outcome_index]