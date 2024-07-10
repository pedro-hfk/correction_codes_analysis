import numpy as np
from hamming import Hamming
from bit_flipper import BitFlipper
from .channels import GaussianChannel

def simulate_non_coded(EiN0, bits):
    errors = 0
    Ei = 1
    N0 = Ei / EiN0

    gaussian = GaussianChannel(N0/2)

    modulated = gaussian.modulate_BPSK(Ei, bits)
    received = gaussian.transmit(modulated)
    demodulated = gaussian.demodulate(received)
    errors += np.abs(demodulated - bits)

    return errors / len(bits)

def simulate_hamming(EbN0, bits, hamming):

    errors = 0
    n = hamming.codeword_size
    k = hamming.information_size

    info_number = len(bits) // k

    Eb = 1
    N0 = Eb / EbN0

    gaussian = GaussianChannel(N0/2)

    for i in range(info_number):
        encoded = hamming.encode(bits[k*i:k*(i+1)])
        modulated = gaussian.modulate_BPSK(Eb, encoded)
        received = gaussian.transmit(modulated)
        demodulated = gaussian.demodulate(received)
        decoded = hamming.decode(demodulated)
        errors += np.sum(np.abs(decoded - bits[k*i:k*(i+1)]))

    return errors / len(bits)

def simulate_bit_flipping(EbN0, bits, bit_flipper):
    
    errors = 0
    n = bit_flipper.codeword_size
    k = bit_flipper.information_size

    info_number = len(bits) // k

    Eb = 1
    N0 = Eb / EbN0

    gaussian = GaussianChannel(N0/2)

    for i in range(info_number):
        encoded = bit_flipper.encode(bits[k*i:k*(i+1)])
        modulated = gaussian.modulate_BPSK(Eb, encoded)
        received = gaussian.transmit(modulated)
        demodulated = gaussian.demodulate(received)
        decoded = bit_flipper.decode(demodulated)
        errors += np.abs(decoded - bits[k*i:k*(i+1)])

    return errors / len(bits)