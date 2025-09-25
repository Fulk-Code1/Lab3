import unittest
from history_service import app as history_app
import os
import json

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.app = history_app.test_client()
        if os.path.exists("history.json"):
            os.remove("history.json")

    def test_add_history(self):
        response = self.app.post('/history/add', json={"file": "mp3_file.mp3", "action": "Loaded"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "History updated")

if __name__ == '__main__':
    unittest.main()