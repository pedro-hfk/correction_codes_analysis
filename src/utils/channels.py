import numpy as np

class BinarySymmetricChannel:

    def __init__(self, error_probability):
        if 0 < error_probability < 1:
            self.error_probability=error_probability
        else:
            raise ValueError("Error probability must be between 0 and 1.")
    
    def transmit(self, message):
        error_vector = np.random.uniform(low=0, high=1, size=message.size)
        return np.where(error_vector < self.error_probability, 1-message, message)
    

class GaussianChannel:

    def __init__(self, noise_variance):
        self.noise_variance = noise_variance

    def modulate_BPSK(self, Eb, bits):
        amplitude = np.sqrt(Eb)
        return np.where(bits == 1, amplitude, -amplitude)
    
    def transmit(self, signal):
        noise = np.random.normal(loc=0, scale=np.sqrt(self.noise_variance), size=signal.size)
        return signal + noise

    def demodulate(self, received):
        return np.where(received > 0, 1, 0)
    