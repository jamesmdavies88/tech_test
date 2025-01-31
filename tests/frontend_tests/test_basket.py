import json
import logging
import os
import random
import pytest
from frontend.pages.home import Home
from frontend.pages.navigation import Navigation
from frontend.pages.sweets import Sweets
import frontend.helpers.driver_utils as driver_utils


class TestBasket:

    TEST_BASKET_OPERATIONS_TEST_DATA_PATH = os.path.join(
        "tests", "frontend_tests", "data", "basket_operations_test_data.json"
    )

    with open(TEST_BASKET_OPERATIONS_TEST_DATA_PATH) as f:
        test_data = json.load(f)
    @pytest.mark.basket_operations
    @pytest.mark.parametrize("data", test_data)
    @pytest.mark.usefixtures("setup")
    def test_basket_operations(self, setup, data):
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        sweets = Sweets(driver)

        TEST_CATALOG_DATA_TEST_DATA_PATH = os.path.join(
            "tests", "frontend_tests", "data", "catalog_items.json"
        )
        ITEMS = data["items"]

        with open(TEST_CATALOG_DATA_TEST_DATA_PATH) as f:
            test_data = json.load(f)

        logging.info(f"Verifying items show in the catalog")
        home.open_url()
        navigation.click_sweets()
        sweets.verify_sweet_page_loads()
        driver_utils.take_screenshot(driver, "Catalog Items")
        
        for item in range(1, ITEMS):
            logging.info(f"Adding item {item} to basket")
            sample_data = random.sample(test_data, 1)
            sweets.add_to_basket(sample_data[0]["name"], sample_data[0]["subtitle"], sample_data[0]["price"])
            driver_utils.take_screenshot(driver, f"Item {item} added to basket")
