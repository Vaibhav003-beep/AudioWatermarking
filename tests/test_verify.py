import unittest
from src import verify_signature

class TestVerifySignature(unittest.TestCase):
    def test_verification(self):
        try:
            verify_signature.verify_signature('../data/stego_audio.wav', '../data/input_audio.wav')
        except Exception as e:
            self.fail(f"Verification failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
