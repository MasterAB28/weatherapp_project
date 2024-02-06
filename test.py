"""
Author: Aviad Barel
Reviewer: Tomer
"""

import unittest
import requests
import os


class TestWebsiteReachable(unittest.TestCase):
    def setUp(self):
        os.system("docker compose -f /home/aviad/Git/devops/containers-docker/compose.yaml up -d")

    def test_website_reachable(self):
        status_code = requests.get("http://172.17.0.1:8000/").status_code
        self.assertEqual(status_code, 200, "OOPS the website is not reachable")

    def tearDown(self):
        os.system("docker compose -f /home/aviad/Git/devops/containers-docker/compose.yaml kill")


if __name__ == "__main__":
    unittest.main()
