import json
import logging
import os
import time
import pytest
from frontend.pages.home import Home
from frontend.pages.navigation import Navigation
from frontend.pages.sweets import Sweets
import frontend.helpers.driver_utils as driver_utils


class TestCatalog:

    @pytest.mark.catalog_verify
    @pytest.mark.usefixtures("setup")
    def test_verify_catalog(self, setup):
        driver = setup
        home = Home(driver)
        navigation = Navigation(driver)
        sweets = Sweets(driver)

        TEST_CATALOG_DATA_TEST_DATA_PATH = os.path.join(
            "tests", "frontend_tests", "data", "catalog_items.json"
        )

        with open(TEST_CATALOG_DATA_TEST_DATA_PATH) as f:
            test_data = json.load(f)

        logging.info(f"Verifying items show in the catalog")
        home.open_url()
        navigation.click_sweets()
        sweets.verify_sweet_page_loads()
        driver_utils.take_screenshot(driver, "Catalog Items")
        for data in test_data:
            sweets.verify_catalog_item_present(
                data["name"], data["subtitle"], data["price"]
            )
