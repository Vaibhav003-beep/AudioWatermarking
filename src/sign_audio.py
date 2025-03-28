import os
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def sign_audio(audio_path):
    # Determine the directory of the current script and data folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')

    # Load the newly generated private key
    private_key_path = os.path.join(data_dir, 'private.pem')
    with open(private_key_path, 'rb') as priv_file:
        private_key = RSA.import_key(priv_file.read())

    # Read the audio file data
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Compute the SHA-256 hash of the audio data
    hash_obj = SHA256.new(audio_data)

    # Sign the hash using the private key
    signature = pkcs1_15.new(private_key).sign(hash_obj)

    # Save the signature to the data folder
    signature_path = os.path.join(data_dir, 'signature.sig')
    with open(signature_path, 'wb') as sig_file:
        sig_file.write(signature)

    print("Audio signed. Signature saved in:", signature_path)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    audio_path = os.path.join(project_root, 'data', 'audio.wav')
    sign_audio(audio_path)
