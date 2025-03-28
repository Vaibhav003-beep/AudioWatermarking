import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Add the 'src' folder to sys.path so we can import our modules
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from src.generate_keys import generate_keys
from src.sign_audio import sign_audio
from src.embed_signature import embed_signature
from src.verify_signature import verify_signature


def run_full_process():
    # Let the user select an audio file (WAV)
    audio_path = filedialog.askopenfilename(initialdir="data", title="Select Audio File",
                                            filetypes=(("WAV files", "*.wav"),))
    if not audio_path:
        messagebox.showerror("Error", "No audio file selected. Process aborted.")
        return

    try:
        # Step 1: Generate new keys for this audio file
        print("Generating new RSA key pair for the audio file...")
        generate_keys()

        # Step 2: Sign the audio file using the new private key
        print("Signing the audio file...")
        sign_audio(audio_path)

        # Step 3: Embed the signature into the audio file
        signature_path = os.path.join("data", "signature.sig")
        print("Embedding signature into the audio file...")
        embed_signature(audio_path, signature_path)

        # Step 4: Verify the embedded signature using the original audio file
        stego_audio_path = os.path.join("data", "stego_audio.wav")
        print("Verifying the signature from the stego audio...")
        verification_result = verify_signature(stego_audio_path, audio_path)

        # Save the verification result in a text file
        result_file = os.path.join("data", "verification_result.txt")
        with open(result_file, "w") as f:
            f.write(verification_result)

        print("Verification result stored in:", result_file)
        messagebox.showinfo("Process Complete", "Audio processing complete. Check console for details.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during processing: {e}")


# Create the Tkinter UI with a single button for full processing
root = tk.Tk()
root.title("DeepGuard - Audio Watermarking Tool")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

btn_process = tk.Button(frame, text="Process Audio", command=run_full_process, width=30)
btn_process.pack(pady=10)

root.mainloop()
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Add the 'src' folder to sys.path so we can import our modules
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from src.generate_keys import generate_keys
from src.sign_audio import sign_audio
from src.embed_signature import embed_signature
from src.verify_signature import verify_signature


def run_full_process():
    # Let the user select an audio file (WAV)
    audio_path = filedialog.askopenfilename(initialdir="data", title="Select Audio File",
                                            filetypes=(("WAV files", "*.wav"),))
    if not audio_path:
        messagebox.showerror("Error", "No audio file selected. Process aborted.")
        return

    try:
        # Step 1: Generate new keys for this audio file
        print("Generating new RSA key pair for the audio file...")
        generate_keys()

        # Step 2: Sign the audio file using the new private key
        print("Signing the audio file...")
        sign_audio(audio_path)

        # Step 3: Embed the signature into the audio file
        signature_path = os.path.join("data", "signature.sig")
        print("Embedding signature into the audio file...")
        embed_signature(audio_path, signature_path)

        # Step 4: Verify the embedded signature using the original audio file
        stego_audio_path = os.path.join("data", "stego_audio.wav")
        print("Verifying the signature from the stego audio...")
        verification_result = verify_signature(stego_audio_path, audio_path)

        # Save the verification result in a text file
        result_file = os.path.join("data", "verification_result.txt")
        with open(result_file, "w") as f:
            f.write(verification_result)

        print("Verification result stored in:", result_file)
        messagebox.showinfo("Process Complete", "Audio processing complete. Check console for details.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during processing: {e}")


# Create the Tkinter UI with a single button for full processing
root = tk.Tk()
root.title("DeepGuard - Audio Watermarking Tool")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

btn_process = tk.Button(frame, text="Process Audio", command=run_full_process, width=30)
btn_process.pack(pady=10)

root.mainloop()
