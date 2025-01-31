from frontend.helpers.common_elements import CommonElements
from selenium import webdriver


class Login(CommonElements):
    def __init__(self, driver: "webdriver.Remote"):
        super().__init__(driver)

    def enter_email(self, email):
        self.input_following_label_xpath("Email address", email)

    def enter_password(self, password):
        self.input_following_label_xpath("Password", password)

    def click_login(self):
        self.click_button_text("Login")

    def verify_email_error_message(self):
        self.wait_for_text_contains("Please enter a valid email address.")

    def verify_password_error_message(self):
        self.wait_for_text_contains("Please enter a valid password.")
