"""
Author: Aviad Barel
Reviewer: Tomer
"""
import time
import unittest
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSelenium(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--timeout=120')
        cls.driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_positive(self):
        self.driver.get("http://172.17.0.1:8000/")
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Ashdod")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        time.sleep(5)
        found_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "found"))
        )

        # Assert that the element is enabled
        self.assertTrue(found_element.is_enabled())

    def test_negative(self):
        self.driver.get("http://172.17.0.1:8000/")
        driver = self.driver
        driver.find_element(by=By.NAME, value="city").send_keys("Gaza")
        driver.find_element(by=By.CSS_SELECTOR, value="button").click()
        time.sleep(5)
        self.assertTrue(driver.find_element(By.NAME, "not-found").is_enabled())


if __name__ == '__main__':
    unittest.main()
