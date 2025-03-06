import os
import unittest
from src.utils.text import read_lines
from src.utils.audio import save_audio

class TestUtils(unittest.TestCase):

    def test_read_lines(self):
        # Test reading lines from a sample text file
        lines = read_lines('data/input/sample.txt')
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

    def test_save_audio(self):
        # Test saving audio to a file
        audio_data = b'\x00\x01\x02'  # Sample audio data
        output_path = 'data/output/test_audio.wav'
        save_audio(audio_data, output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)  # Clean up after test

if __name__ == '__main__':
    unittest.main()