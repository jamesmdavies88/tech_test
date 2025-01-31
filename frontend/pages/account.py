from frontend.helpers.common_elements import CommonElements
from selenium import webdriver


class Account(CommonElements):
    def __init__(self, driver: "webdriver.Remote"):
        super().__init__(driver)

    def wait_for_your_account(self):
        self.wait_for_text("Your Account")

    def wait_for_welcome_back_email(self, email):
        self.wait_for_text_contains("Welcome back")
        self.wait_for_text_contains(email)

    def verify_order_history(self, order_history):
        for order in order_history:
            self.wait_for_text_contains(order["order_number"])
            self.wait_for_text_contains(order["date_ordered"])
            for description in order["order_description"]:
                locator = "//td[contains(normalize-space(), '{description}')]"
                self.wait_for_element_invisible(locator=locator)
            self.wait_for_text_contains(order["order_total"])
