import random
import numpy as np


class BitFlipper:
    def __init__(self, N, dv, dc):
        self.dv = dv
        self.dc = dc
        self.codeword_size = N
        self.information_size = int(N * dv / dc)
        self.H = self.generate_H()

    def generate_H(self):
        num_rows = self.information_size
        submatrix_rows = int(self.codeword_size / self.dc)

        H = np.zeros((num_rows, self.codeword_size), dtype=int)

        for i in range(self.dv):
            submatrix = np.zeros((submatrix_rows, self.codeword_size), dtype=int)
            for col in range(self.codeword_size):
                row = col % submatrix_rows
                submatrix[row, col] = 1
            np.random.shuffle(submatrix.T)
            H[i * submatrix_rows: (i + 1) * submatrix_rows, :] = submatrix
        return H
        # subH1 = np.zeros((int(self.codeword_size / self.dc), self.codeword_size))
        # for i in range(0, int(self.codeword_size / self.dc)):
        #     for j in range(0, self.dc):
        #         subH1[i, i * self.dc + j] = 1
        #
        # permutation = np.random.permutation(self.codeword_size)
        # subH2 = subH1[:, permutation]
        #
        # permutation = np.random.permutation(self.codeword_size)
        # subH3 = subH1[:, permutation]
        #
        # permutation = np.random.permutation(self.codeword_size)
        # subH4 = subH1[:, permutation]
        #
        # H = np.vstack((subH4, subH2, subH3))
        #
        # return H

    def decode(self, received, max_iter=100):
        rows, cols = self.H.shape
        iteration = 0

        while iteration < max_iter:
            error_counts = np.zeros(cols, dtype=int)
            for row in range(rows):
                indices = np.where(self.H[row, :] == 1)[0]
                parity = 0
                for index in indices:
                    parity ^= received[index]

                if parity == 1:
                    for index in indices:
                        error_counts[index] += 1

            if np.sum(error_counts) == 0:
                break

            max_error_count = np.max(error_counts)
            candidates_to_flip = np.where(error_counts == max_error_count)[0]
            bit_to_flip = random.choice(candidates_to_flip)
            received[bit_to_flip] ^= 1
            iteration += 1

        return received
