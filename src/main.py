from utils import *
from hamming import Hamming
from bit_flipper import BitFlipper
import matplotlib.pyplot as plt

SIMULATION_SAMPLE = 1008

def save_results(filename, SNR, non_coded_ber, hamming_ber, bit_flipping_ber):
    with open(filename, 'w') as file:
        file.write("SNR_dB NonCoded_BER Hamming_BER BitFlipping_BER\n")
        for i in range(len(SNR)):
            file.write(f"{SNR[i]:.2f} {non_coded_ber[i]:.6e} {hamming_ber[i]:.6e} {bit_flipping_ber[i]:.6e}\n")

def main():

    SNR = [i/2 for i in range(0, 11)]

    q = 0.5
    distribution = np.random.uniform(low=0, high=1, size=SIMULATION_SAMPLE)
    bits = np.where(distribution < q, 1, 0)

    non_coded_ber = []

    hamming_ber = []
    hamming = Hamming()
    hamming_rate = hamming.rate

    bit_flipping_ber = []

    llr_ber = []

    llr_modified_ber = []


    for EbN0_dB in SNR:

        EbN0 = 10**(EbN0_dB/10)
        EiN0 = EbN0 / hamming_rate

        # Non-coded System:
        non_coded_ber.append(simulate_non_coded(EiN0, bits))

        # Hamming System:
        hamming_ber.append(simulate_hamming(EbN0, bits, hamming))

        # Bit Flipping System:
        bit_flipper = BitFlipper(SIMULATION_SAMPLE, hamming_rate)
        bit_flipping_ber.append(simulate_bit_flipping(EbN0, bits, bit_flipper))

    save_results("ber_results.txt", SNR, non_coded_ber, hamming_ber, bit_flipping_ber)


    plt.figure()
    plt.plot(SNR / hamming_rate, non_coded_ber, label="Non-coded")
    plt.plot(SNR, hamming_ber, label="Hamming")
    plt.plot(SNR, bit_flipping_ber, label="Bit Flipping")
    # plt.plot(SNR, llr_ber, label="LLR Decoder")
    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("Bit Error Rate")
    # plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.title("Bit Error Rate vs. $E_i/N_0$")
    plt.show()
    

if __name__ == "__main__":
    main()