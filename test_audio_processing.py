import unittest
import requests

class TestAudioProcessing(unittest.TestCase):
    def test_load_audio(self):
        response = requests.post('http://localhost:5001/process/load', json={"file_path": "mp3_file.mp3"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Сохранен", response.json()["status"])

if __name__ == '__main__':
    unittest.main()