import os
import numpy as np
import pywt
from pydub import AudioSegment


def embed_signature(audio_path, signature_path):
    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Decompose the audio signal using DWT (Haar wavelet, one-level decomposition) with periodization mode
    coeffs = pywt.wavedec(samples, 'haar', level=1, mode='periodization')
    cA, cD = coeffs

    # Convert detail coefficients to integer type for bitwise operations
    cD_int = np.round(cD).astype(np.int32)

    # Read the signature and convert it to a binary string
    with open(signature_path, 'rb') as sig_file:
        signature = sig_file.read()
    sig_bits = ''.join(format(byte, '08b') for byte in signature)

    # Embed the signature bits into the least significant bit of the detail coefficients
    for i, bit in enumerate(sig_bits):
        if i < len(cD_int):
            cD_int[i] = (cD_int[i] & ~1) | int(bit)

    # Reconstruct the coefficients with modified detail coefficients
    coeffs_modified = [cA, cD_int.astype(np.float64)]
    stego_samples = pywt.waverec(coeffs_modified, 'haar', mode='periodization').astype(np.int16)
    stego_audio = audio._spawn(stego_samples.tobytes())

    # Save the stego audio file in the data folder
    data_dir = os.path.dirname(signature_path)
    stego_audio_path = os.path.join(data_dir, 'stego_audio.wav')
    stego_audio.export(stego_audio_path, format='wav')
    print("Signature embedded. Stego audio saved in:", stego_audio_path)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    audio_path = os.path.join(project_root, 'data', 'audio.wav')
    signature_path = os.path.join(project_root, 'data', 'signature.sig')
    embed_signature(audio_path, signature_path)
