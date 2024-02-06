"""
Author: Aviad Barel
Reviewer: Tomer
"""
import unittest
from selenium import webdriver

from selenium.webdriver.common.by import By


class TestSelenium(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(command_executor='http://selenium:4444', options=options)

    def test_positive(self):
        self.driver.get("http://172.17.0.1:8000/")
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Ashdod")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        self.assertTrue(driver.find_element(By.NAME, "found").is_enabled())

    def test_negative(self):
        self.driver.get("http://172.17.0.1:8000/")
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Gaza")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        self.assertTrue(driver.find_element(By.NAME, "not-found").is_enabled())

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
