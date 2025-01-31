from selenium import webdriver
from selenium.webdriver.common.by import By
from frontend.helpers.common_waits import CommonWaits


class CommonElements(CommonWaits):
    def __init__(self, driver: "webdriver.Remote"):
        self.driver = driver
        super().__init__(driver)

    def input_following_label_xpath(self, label, input_text, timeout=10):
        """Input text in field following a label"""
        if "'" not in label:
            locator = f"//*[text()='{label}']//following::input[1]"
        else:
            parts = label.split("'")
            concat_parts = "',\"'\",'".join(parts)
            locator = f"//*[text()=concat('{concat_parts}')]//following::input[1]"
        self.wait_for_element_visible(locator=locator, timeout=timeout)
        self.driver.find_element(By.XPATH, locator).send_keys(input_text)

    def click_text(self, text, timeout=10, index=1):
        """Click element containing exact text"""
        if "'" not in text:
            locator = f"(//*[text()='{text}'])[{index}]"
        else:
            parts = text.split("'")
            concat_parts = "',\"'\",'".join(parts)
            locator = f"(//*[text()=concat('{concat_parts}')])[{index}]"
        self.wait_for_element_clickable(locator=locator, timeout=timeout)
        self.driver.find_element(By.XPATH, locator).click()

    def click_button_text(self, text, timeout=10, index=1):
        """Click element containing exact text"""
        if "'" not in text:
            locator = f"(//button[text()='{text}'])[{index}]"
        else:
            parts = text.split("'")
            concat_parts = "',\"'\",'".join(parts)
            locator = f"(//button[text()=concat('{concat_parts}')])[{index}]"
        self.wait_for_element_clickable(locator=locator, timeout=timeout)
        self.driver.find_element(By.XPATH, locator).click()

    def wait_for_text(self, text, timeout=10, index=1):
        """Wait for text to be visible on page"""
        if "'" not in text:
            locator = f"(//*[text()='{text}'])[{index}]"
        else:
            parts = text.split("'")
            concat_parts = "',\"'\",'".join(parts)
            locator = f"(//*[text()=concat('{concat_parts}')])[{index}]"
        self.wait_for_element_visible(locator=locator, timeout=timeout)

    def wait_for_text_contains(self, text, timeout=10, index=1):
        """Wait for text to be visible on page using contains"""
        if "'" not in text:
            locator = f"(//*[contains(text(),'{text}')])[{index}]"
        else:
            parts = text.split("'")
            concat_parts = "',\"'\",'".join(parts)
            locator = f"(//*[contains(text(),concat('{concat_parts}'))])[{index}]"
        self.wait_for_element_visible(locator=locator, timeout=timeout)
