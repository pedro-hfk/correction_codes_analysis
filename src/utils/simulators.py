import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hamming.hamming import Hamming
from bit_flipper.bit_flipper import BitFlipper
from llrs.llr import LLRCoder
from utils.channels import GaussianChannel


def simulate_non_coded(EiN0, bits, num_simulations=25):
    total_errors = 0

    for _ in range(num_simulations):
        errors = 0
        Ei = 1
        N0 = Ei / EiN0

        gaussian = GaussianChannel(N0 / 2)

        modulated = gaussian.modulate_BPSK(Ei, bits)
        received = gaussian.transmit(modulated)
        demodulated = gaussian.demodulate(received)
        errors += np.sum(np.abs(demodulated - bits))

        total_errors += errors

    average_error = total_errors / (len(bits) * num_simulations)
    return average_error


def simulate_hamming(EbN0, bits, hamming, num_simulations=25):
    total_errors = 0

    for _ in range(num_simulations):
        errors = 0
        n = hamming.codeword_size
        k = hamming.information_size

        info_number = len(bits) // k

        Eb = 1
        N0 = Eb / EbN0

        gaussian = GaussianChannel(N0 / 2)

        for i in range(info_number):
            encoded = hamming.encode(bits[k * i:k * (i + 1)])
            modulated = gaussian.modulate_BPSK(Eb, encoded)
            received = gaussian.transmit(modulated)
            demodulated = gaussian.demodulate(received)
            decoded = hamming.decode(demodulated)
            errors += np.sum(np.abs(decoded - bits[k * i:k * (i + 1)]))

        total_errors += errors

    average_error = total_errors / (len(bits) * num_simulations)
    return average_error


def simulate_bit_flipping(EbN0, bits, bit_flipper, num_simulations=25):
    total_errors = 0

    for _ in range(num_simulations):
        errors = 0

        Eb = 1
        N0 = Eb / EbN0

        gaussian = GaussianChannel(N0 / 2)

        modulated = gaussian.modulate_BPSK(Eb, bits)
        received = gaussian.transmit(modulated)
        demodulated = gaussian.demodulate(received)
        decoded = bit_flipper.decode(demodulated)
        errors += np.count_nonzero(np.bitwise_xor(decoded, bits))

        total_errors += errors

    average_error = total_errors / (len(bits) * num_simulations)
    return average_error


def simulate_llr_coder(EbN0, bits, llr_coder, num_simulations=25):
    total_errors = 0

    Eb = 1
    N0 = Eb / EbN0

    gaussian = GaussianChannel(N0 / 2)

    for _ in range(num_simulations):
        errors = 0

        signal = bits
        encoded_signal = gaussian.modulate_BPSK(Eb, signal)
        received_signal = gaussian.transmit(encoded_signal)
        received_llrs = 2 * received_signal / (N0 / 2)
        decoded = llr_coder.decode(received_llrs)
        errors += np.count_nonzero(np.bitwise_xor(decoded, signal))

        total_errors += errors

    average_error = total_errors / (len(bits) * num_simulations)
    return average_error
