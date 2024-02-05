"""
Author: Aviad Barel
Reviewer: Tomer
"""
import time
import unittest
from selenium import webdriver
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class TestSelenium(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options,
                                        service=webdriver.FirefoxService(executable_path='/snap/bin/geckodriver'))
        self.driver.get("http://172.17.0.1:8000/")

    def test_positive(self):
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Ashdod")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        self.assertTrue(driver.find_element(By.NAME, "found").is_enabled())

    def test_negative(self):
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Gaza")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        self.assertTrue(driver.find_element(By.NAME, "not-found").is_enabled())

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
