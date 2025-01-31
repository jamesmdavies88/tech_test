from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class CommonWaits:
    def __init__(self, driver: "webdriver.Remote"):
        self.driver = driver

    def wait_for_element_visible(self, locator, locator_type=By.XPATH, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located((locator_type, locator)))
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not visible after {timeout} seconds"
            )

    def wait_for_element_clickable(self, locator, locator_type=By.XPATH, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable((locator_type, locator)))
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not clickable after {timeout} seconds"
            )

    def wait_for_element_present(self, locator, locator_type=By.XPATH, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((locator_type, locator)))
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not present after {timeout} seconds"
            )

    def wait_for_element_invisible(self, locator, locator_type=By.XPATH, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(
                EC.invisibility_of_element_located((locator_type, locator))
            )
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} still visible after {timeout} seconds"
            )
