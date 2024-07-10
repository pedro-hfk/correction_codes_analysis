import numpy as np

class BitFlipper:
    def __init__(self, N, R):
        self.N = N
        self.R = R
        self.dv, self.dc = self.calculate_dv_dc()
        self.H = self.generate_H()
        self.codeword_size = self.H.shape[0]
        self.information_size = self.H.shape[1]


    def calculate_dv_dc(self):
        for dv in range(2, self.N):
            dc = int(dv / (1 - self.R))
            if (self.N * dv) % dc == 0:
                return dv, dc
        raise ValueError("No suitable dv and dc found for given N and R.")
    
    def generate_H(self):
        M = (self.N * self.dv) // self.dc
        H = np.zeros((M, self.N), dtype=int)
        col_indices = np.arange(self.N)
        
        # Populate the matrix ensuring dv ones per row
        for i in range(M):
            selected_cols = np.random.choice(col_indices, self.dv, replace=False)
            H[i, selected_cols] = 1
        
        # Ensure each column has exactly dc ones
        for j in range(self.N):
            current_ones = np.where(H[:, j] == 1)[0]
            while len(current_ones) != self.dc:
                if len(current_ones) > self.dc:
                    rows_to_zero = np.random.choice(current_ones, len(current_ones) - self.dc, replace=False)
                    H[rows_to_zero, j] = 0
                else:
                    zero_rows = np.where(H[:, j] == 0)[0]
                    rows_to_one = np.random.choice(zero_rows, self.dc - len(current_ones), replace=False)
                    H[rows_to_one, j] = 1
                current_ones = np.where(H[:, j] == 1)[0]
        
        return H
    
    def encode(self, message):
        if len(message) != self.information_size:
            raise ValueError(f"Message length must be equal to information size: {self.information_size}.")
        return np.dot(message, self.H) % 2
    
    def decode(self, received, max_iter=100):
        decoded = np.copy(received)
        for iter in range(max_iter):
            syndromes = np.mod(decoded, 2)
            if np.sum(syndromes) == 0:
                return decoded
            unsatisfied_parity = np.dot(self.H.T, syndromes)
            bit_to_flip = np.argmax(unsatisfied_parity)
            decoded[bit_to_flip] = 1 - decoded[bit_to_flip]
        return decoded  

