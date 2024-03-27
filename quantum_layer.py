import tensorflow as tf
import numpy as np
class QuantumLikeLayer(tf.keras.layers.Layer):
    def __init__(self, num_qubits, depth, activation=None, trainable=True):
        super(QuantumLikeLayer, self).__init__(trainable=trainable)
        self.num_qubits = num_qubits
        self.depth = depth
        self.activation = activation
        self.gates_sequence = self.create_gates_sequence()

    def create_hadamard_gate(self):
        H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=np.float32)
        hadamard_full = H
        for _ in range(1, self.num_qubits):
            hadamard_full = np.kron(hadamard_full, H)
        return hadamard_full

    def create_cz_gate(self):
        CZ = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=np.float32)
        cz_full = CZ
        for _ in range(2, self.num_qubits):
            cz_full = np.kron(cz_full, np.eye(2, dtype=np.float32))
        return cz_full

    def create_gates_sequence(self):
        # Sequence of Hadamard and CZ gates, simulated over depth
        gates_sequence = []
        for _ in range(self.depth):
            hadamard_gate = self.create_hadamard_gate()
            cz_gate = self.create_cz_gate()
            gates_sequence.append((hadamard_gate, cz_gate))
        return gates_sequence

    def call(self, inputs):
        inputs = tf.cast(inputs, tf.float32)
        state = inputs
        for hadamard_gate, cz_gate in self.gates_sequence:

            state = tf.linalg.matvec(hadamard_gate, state)
            state = tf.linalg.matvec(cz_gate, state)

        if self.activation:
            state = self.activation(state)

        return state