from frontend.helpers.common_elements import CommonElements
from selenium import webdriver
from selenium.webdriver.common.by import By


class Sweets(CommonElements):
    def __init__(self, driver: "webdriver.Remote"):
        super().__init__(driver)

    def verify_sweet_page_loads(self):
        self.wait_for_text("Browse our delicious choice of retro sweets.")

    def verify_catalog_item_present(self, name, subtitle, price):
        locator = f'//*[text()="{name}"]/following-sibling::p[text()="{subtitle}"]/following-sibling::p//*[text()="{price}"]'
        # locator = f'//*[contains(normalize-space(.), "{name}") and contains(normalize-space(.), "{subtitle}") and contains(normalize-space(.), "{price}")]'
        self.wait_for_element_present(locator=locator)
    
    def add_to_basket(self, name, subtitle, price):
        xpath = f"//*[text()='{name}']//following::a[1]"
        print(xpath)
        self.driver.find_element(By.XPATH, xpath).click()
