import time
from backend.auth import Auth
from backend.airports import Airports
import backend.helpers.backend_helpers as backend_helpers
import requests
import pytest
import logging


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

    @pytest.mark.validate_ratelimit
    def test_rate_limit(self):
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

        start_time = time.time()
        got_rate_limited = False
        calls_made = 0

        for i in range(110):
            calls_made += 1
            rsp = airports.get_all_airports(token)
            if rsp.status_code == 429:
                logging.info(f"Rate-limit reached on call {calls_made}")
                got_rate_limited = True
                break
            if time.time() - start_time > 60:
                logging.warning("Test ran over 60 seconds without hitting rate limit.")
                break

        assert (
            got_rate_limited
        ), "Never received a rate limit response after 100 calls in under a minute."

        logging.info("Wait for rate limit to reset...")
        time.sleep(60)
        r = airports.get_all_airports(token)
        assert r.status_code == 200, f"Failed to fetch airports after rate limit reset."
