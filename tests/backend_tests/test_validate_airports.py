import time
from backend.auth import Auth
from backend.airports import Airports
import backend.helpers.backend_helpers as backend_helpers
import requests
import pytest
import logging
import os
import json


@pytest.mark.backend_tests
class TestAirports:
    @pytest.mark.validate_iata
    def test_validate_fetch_airports_iata(self):
        logging.info("Authenticating to get token...")
        session = requests.Session()
        auth = Auth()
        response = auth.get_token(
            "jamesmdavies88@gmail.com", "James123", session=session
        )

        assert (
            response.status_code == 200
        ), f"Authentication failed with status {response.status_code}"
        token = response.json()["token"]

        logging.info(
            "Initialising API clients, will tidy this up so everything can be initialised in one place..."
        )
        airports = Airports(session=session)

        logging.info("Fetching all airports, paginating if necessary...")
        response = airports.get_all_airports(token)
        assert (
            response.status_code == 200
        ), f"Failed to retrieve airports, status {response.status_code}"

        headers = response.headers
        logging.info(f"Response Headers: {headers}")

        original_data = response.json()["data"]
        last_page = response.json()["links"]["last"]

        # Get total pages
        total_pages = backend_helpers.get_total_pages(last_page)
        logging.info(f"Total pages: {total_pages}")

        logging.info("Fetching only the first page to avoid hitting the rate limit.")

        iata_values = [item["attributes"]["iata"] for item in original_data]
        logging.info(f"Validating IATA values: {iata_values}")

        for iata in iata_values:
            response = airports.get_airport_by_iata(iata, token)
            assert (
                response.status_code == 200
            ), f"Failed to fetch airport {iata}, status {response.status_code}"

            single_airport = response.json()["data"]
            assert (
                single_airport in original_data
            ), f"Airport data mismatch for IATA '{iata}'"

    @pytest.mark.test_airport_distance
    def test_airport_distance(self):
        session = requests.Session()
        auth = Auth()

        logging.info("Get token")
        response = auth.get_token(
            "jamesmdavies88@gmail.com", "James123", session=session
        )
        assert (
            response.status_code == 200
        ), f"Authentication failed: {response.status_code}"
        token = response.json()["token"]

        airports = Airports(session=session)

        logging.info("Load in some test data for IATA values")
        test_data_path = os.path.join(
            "tests", "backend_tests", "data", "iata_distances.json"
        )
        with open(test_data_path) as f:
            test_data = json.load(f)

        for iata in test_data:
            r = airports.get_distance_between_iata(
                iata["iata_one"], iata["iata_two"], token
            )
            assert r.status_code == 200
            assert (
                r.json()["data"]["attributes"]["from_airport"]["iata"]
                == iata["iata_one"]
            )
            assert (
                r.json()["data"]["attributes"]["to_airport"]["iata"] == iata["iata_two"]
            )
            assert r.json()["data"]["attributes"]["kilometers"] == iata["kilometers"]
            assert r.json()["data"]["attributes"]["miles"] == iata["miles"]
            assert (
                r.json()["data"]["attributes"]["nautical_miles"]
                == iata["nautical_miles"]
            )
