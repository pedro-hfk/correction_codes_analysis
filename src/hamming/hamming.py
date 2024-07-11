import numpy as np


class Hamming:

    def __init__(self, dv, dc):
        self.codeword_size = dc
        self.information_size = dc - dv
        self.rate = self.information_size / self.codeword_size
        self.generator_matrix = self.generator_matrix()
        self.parity_matrix = self.parity_matrix()

    def generator_matrix(self):
        return np.array([[1, 0, 0, 0, 1, 1, 1],
                         [0, 1, 0, 0, 1, 0, 1],
                         [0, 0, 1, 0, 1, 1, 0],
                         [0, 0, 0, 1, 0, 1, 1]])
        
    def parity_matrix(self):
        return np.array([[1, 1, 1, 0, 1, 0, 0],
                         [1, 0, 1, 1, 0, 1, 0],
                         [1, 1, 0, 1, 0, 0, 1]]).T
        
    def encode(self, message):
        if len(message) != self.information_size:
            raise ValueError(f"Message length must be equal to information size: {self.information_size}.")
        return np.dot(message, self.generator_matrix) % 2
    
    def decode(self, message):
        if len(message) != self.codeword_size:
            raise ValueError(f"Message length must be equal to codeword size: {self.codeword_size}.")
        
        syndrome = np.dot(message, self.parity_matrix) % 2
        error_vector = np.zeros(self.codeword_size, dtype=int)
        
        for column_index, column in enumerate(self.parity_matrix):
            if np.array_equal(syndrome, column):
                error_vector[column_index] = 1

        corrected = (message + error_vector) % 2

        return corrected[:self.information_size]
