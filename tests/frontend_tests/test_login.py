import logging
import time
import pytest
from frontend.pages.home import Home
from frontend.pages.login import Login
from frontend.pages.navigation import Navigation
from frontend.pages.account import Account


@pytest.mark.frontend_tests
class TestLogin:
    @pytest.mark.successful_login
    @pytest.mark.usefixtures("setup")
    @pytest.mark.parametrize(
        "email,password",
        [
            ("user1@example.com", "Password123!"),
            ("test.user@domain.com", "Secure789#"),
            ("john.doe@company.net", "Complex456@"),
        ],
    )
    def test_login_success(self, setup, email, password):
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        login = Login(driver)
        account = Account(driver)

        logging.info(f"Logging in with {email} and {password}")
        home.open_url()
        navigation.click_login()
        login.enter_email(email)
        login.enter_password(password)
        login.click_login()
        account.wait_for_your_account()
        logging.info("Login successful")

    @pytest.mark.unsuccessful_login
    @pytest.mark.usefixtures("setup")
    @pytest.mark.parametrize(
        "email,password,expected_errors",
        [
            ("", "Password123!", ["email"]),  # Empty email
            ("test@example.com", "", ["password"]),  # Empty password
            ("", "", ["email", "password"]),  # Both empty
        ],
    )
    def test_unsuccessful_login(self, setup, email, password, expected_errors):
        """Test unsuccessful login attempts with partial/no credentials"""
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        login = Login(driver)

        logging.info(
            f"Attempting login with email: '{email}' and password: '{password}'"
        )

        home.open_url()
        navigation.click_login()
        login.enter_email(email)
        login.enter_password(password)
        login.click_login()

        for error_type in expected_errors:
            if error_type == "email":
                login.verify_email_error_message()
            elif error_type == "password":
                login.verify_password_error_message()

        logging.info(f"Login failed as expected with errors: {expected_errors}")
