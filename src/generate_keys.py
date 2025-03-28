import os
from Crypto.PublicKey import RSA


def generate_keys():
    # Determine the directory of the current script and locate the data folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Generate a new RSA key pair for this audio file
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the new keys in the data folder (overwriting any existing keys)
    with open(os.path.join(data_dir, 'private.pem'), 'wb') as priv_file:
        priv_file.write(private_key)
    with open(os.path.join(data_dir, 'public.pem'), 'wb') as pub_file:
        pub_file.write(public_key)

    print("New RSA keys generated and saved in the data folder.")


if __name__ == "__main__":
    generate_keys()
