from utils.simulators import simulate_non_coded, simulate_hamming, simulate_bit_flipping, simulate_llr_coder
from hamming.hamming import Hamming
from bit_flipper.bit_flipper import BitFlipper
from llrs.llr import LLRCoder
import matplotlib.pyplot as plt
import numpy as np

SIMULATION_SAMPLE = 1008


# def save_results(filename, SNR, non_coded_ber, hamming_ber, bit_flipping_ber):
#     with open(filename, 'w') as file:
#         file.write("SNR_dB NonCoded_BER Hamming_BER BitFlipping_BER\n")
#         for i in range(len(SNR)):
#             file.write(f"{SNR[i]:.2f} {non_coded_ber[i]:.6e} {hamming_ber[i]:.6e} {bit_flipping_ber[i]:.6e}\n")

def main():
    SNR = [i for i in range(0, 11)]

    # q = 0.1
    # distribution = np.random.uniform(low=0, high=1, size=SIMULATION_SAMPLE)
    # bits = np.where(distribution < q, 1, 0)
    bits = np.zeros(SIMULATION_SAMPLE, dtype=int)

    dv, dc = 3, 7

    non_coded_ber = []
    hamming_ber = []
    bit_flipping_ber = []
    llr_original_ber = []

    hamming = Hamming(dv, dc)
    hamming_rate = hamming.rate

    bit_flipper = BitFlipper(SIMULATION_SAMPLE, dv, dc)

    # llr_coder = LLRCoder(SIMULATION_SAMPLE, dv, dc)

    for EbN0_dB in SNR:
        EbN0 = 10 ** (EbN0_dB / 10)
        EiN0 = EbN0 / hamming_rate

        # Non-coded System:
        ber_non_coded = simulate_non_coded(EiN0, bits)
        non_coded_ber.append(ber_non_coded)

        # Hamming System:
        ber_hamming = simulate_hamming(EbN0, bits, hamming)
        hamming_ber.append(ber_hamming)

        # Bit Flipping System:
        ber_bit_flipping = simulate_bit_flipping(EbN0, bits, bit_flipper)
        bit_flipping_ber.append(ber_bit_flipping)

        # LLR System with dv, dc = 3, 7
        # ber_llr_original = simulate_llr_coder(EbN0, bits, llr_coder)
        # llr_original_ber.append(ber_llr_original)

    # save_results("ber_results.txt", SNR, non_coded_ber, hamming_ber, bit_flipping_ber)

    plt.figure()
    plt.plot(SNR, non_coded_ber, label="Non-coded", marker='o')
    plt.plot(SNR, hamming_ber, label="Hamming", marker='s')
    plt.plot(SNR, bit_flipping_ber, label="Bit Flipping", marker='x')
    # plt.plot(SNR, llr_original_ber, label="LLR", marker='+')
    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("Bit Error Rate")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.title("Bit Error Rate vs. $E_i/N_0$")
    plt.show()


if __name__ == "__main__":
    main()
