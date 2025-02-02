import json
import logging
import os
import random
import pytest
from frontend.pages.home import Home
from frontend.pages.navigation import Navigation
from frontend.pages.sweets import Sweets
import frontend.helpers.driver_utils as driver_utils


@pytest.mark.frontend_tests
class TestBasket:

    test_basket_operations_test_data = os.path.join(
        "tests", "frontend_tests", "data", "basket_operations_test_data.json"
    )

    with open(test_basket_operations_test_data) as f:
        test_data = json.load(f)

    @pytest.mark.basket_operations
    @pytest.mark.parametrize("data", test_data)
    @pytest.mark.usefixtures("setup")
    def test_basket_operations(self, setup, data):
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        sweets = Sweets(driver)

        test_catalog_data_path = os.path.join(
            "tests", "frontend_tests", "data", "catalog_items.json"
        )
        items = data["items"]

        with open(test_catalog_data_path) as f:
            catalog_data = json.load(f)

        logging.info(f"Verifying items show in the catalog")
        home.open_url()
        navigation.click_sweets()
        sweets.verify_sweet_page_loads()
        driver_utils.take_screenshot(driver, "Catalog Items")

        sample_data = random.sample(catalog_data, items)
        for product in sample_data:
            logging.info(f"Adding product: {product['name']}")
            sweets.add_to_basket(product["name"])
            driver_utils.take_screenshot(
                driver, f"Item {product['name']} added to basket"
            )
