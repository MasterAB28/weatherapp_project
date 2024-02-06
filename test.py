"""
Author: Aviad Barel
Reviewer: Tomer
"""
import time
import unittest
import requests
import os


class TestWebsiteReachable(unittest.TestCase):

    def test_website_reachable(self):
<<<<<<< HEAD
        
=======
        time.sleep(30)
>>>>>>> d14501c800ae5826bd8c2abe45c8cdc5fb68df86
        status_code = requests.get("http://172.17.0.1:8000/").status_code
        self.assertEqual(status_code, 200, "OOPS the website is not reachable")


if __name__ == "__main__":
    unittest.main()
