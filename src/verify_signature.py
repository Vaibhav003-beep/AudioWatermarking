import os
import numpy as np
import pywt
from pydub import AudioSegment
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def verify_signature(stego_audio_path, original_audio_path):
    # Load the stego audio file
    stego_audio = AudioSegment.from_wav(stego_audio_path)
    stego_samples = np.array(stego_audio.get_array_of_samples())

    # Decompose the stego audio signal using DWT with periodization mode
    coeffs = pywt.wavedec(stego_samples, 'haar', level=1, mode='periodization')
    cA, cD = coeffs

    # Determine the number of bits in the original signature
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    signature_path = os.path.join(data_dir, 'signature.sig')
    with open(signature_path, 'rb') as sig_file:
        original_signature = sig_file.read()
    num_bits = len(original_signature) * 8

    # Extract the signature bits from the detail coefficients
    extracted_bits = [str(int(round(cD[i])) & 1) for i in range(num_bits)]
    extracted_sig_bits = ''.join(extracted_bits)

    # Reconstruct the signature from the extracted bits (grouping into bytes)
    extracted_sig_bytes = bytes(int(extracted_sig_bits[i:i + 8], 2) for i in range(0, num_bits, 8))

    # Debug: show the original and extracted signatures in hexadecimal
    print("Original signature (hex):", original_signature.hex())
    print("Extracted signature (hex):", extracted_sig_bytes.hex())

    # Load the public key from the data folder
    public_key_path = os.path.join(data_dir, 'public.pem')
    with open(public_key_path, 'rb') as pub_file:
        public_key = RSA.import_key(pub_file.read())

    # Read the original audio file (used for hash computation)
    with open(original_audio_path, 'rb') as audio_file:
        original_audio_data = audio_file.read()

    # Compute the SHA-256 hash of the original audio data
    hash_obj = SHA256.new(original_audio_data)

    # Verify the signature using the public key
    verification_message = ""
    try:
        pkcs1_15.new(public_key).verify(hash_obj, extracted_sig_bytes)
        verification_message = "The signature is valid. Audio integrity is verified."
        print(verification_message)
    except (ValueError, TypeError):
        verification_message = "The signature is invalid. Audio may have been tampered with."
        print(verification_message)

    return verification_message


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    stego_audio_path = os.path.join(project_root, 'data', 'stego_audio.wav')
    original_audio_path = os.path.join(project_root, 'data', 'audio.wav')
    verify_signature(stego_audio_path, original_audio_path)
