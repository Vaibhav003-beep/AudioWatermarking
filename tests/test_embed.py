import unittest
from src import embed_signature

class TestEmbedSignature(unittest.TestCase):
    def test_embedding(self):
        # Here, you could include more comprehensive tests if you compare input/output
        try:
            embed_signature.embed_signature('../data/input_audio.wav', '../data/signature.sig')
        except Exception as e:
            self.fail(f"Embedding failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
