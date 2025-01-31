import json
import logging
import os
import time
import pytest
from frontend.pages.home import Home
from frontend.pages.login import Login
from frontend.pages.navigation import Navigation
from frontend.pages.account import Account
import frontend.helpers.driver_utils as driver_utils


class TestOrderHistory:

    TEST_ORDER_HISTORY_TEST_DATA_PATH = os.path.join(
        "tests", "frontend_tests", "data", "order_history_test_data.json"
    )

    with open(TEST_ORDER_HISTORY_TEST_DATA_PATH) as f:
        test_data = json.load(f)

    @pytest.mark.order_history
    @pytest.mark.usefixtures("setup")
    @pytest.mark.parametrize("data", test_data)
    def test_order_history_details(self, setup, data):
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        login = Login(driver)
        account = Account(driver)

        EMAIL = data["email"]
        PASSWORD = data["password"]
        ORDER_HISTORY = data["order_history"]

        logging.info(f"Logging in with {EMAIL} and {PASSWORD}")
        home.open_url()
        navigation.click_login()
        login.enter_email(EMAIL)
        login.enter_password(PASSWORD)
        driver_utils.take_screenshot(driver, "Login Details")
        login.click_login()
        account.wait_for_your_account()
        account.wait_for_welcome_back_email(EMAIL)
        account.verify_order_history(ORDER_HISTORY)
        logging.info("Login successful")
