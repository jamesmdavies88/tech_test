from frontend.helpers.common_elements import CommonElements
from selenium import webdriver


class Navigation(CommonElements):
    def __init__(self, driver: "webdriver.Remote"):
        super().__init__(driver)

    def click_login(self):
        self.click_text("Login")

    def click_sweets(self):
        self.click_text("Sweets")
