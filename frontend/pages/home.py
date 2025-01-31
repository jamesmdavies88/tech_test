from frontend.helpers.common_elements import CommonElements
from selenium import webdriver


class Home(CommonElements):
    def __init__(self, driver: "webdriver.Remote"):
        super().__init__(driver)

    def open_url(self):
        self.driver.get("https://sweetshop.netlify.app/")
        self.wait_for_text("Welcome to the sweet shop!")
