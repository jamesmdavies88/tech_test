import time
from backend.auth import Auth
from backend.airports import Airports
import backend.helpers.backend_helpers as backend_helpers
import requests
import pytest
import logging


class TestRatelimit:
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
