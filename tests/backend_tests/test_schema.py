import time
import json
import os
from jsonschema import validate, ValidationError
from backend.auth import Auth
from backend.airports import Airports
import backend.helpers.backend_helpers as backend_helpers
import requests
import pytest
import logging


@pytest.mark.backend_tests
class TestSchema:

    @pytest.mark.validate_airport_schema
    def test_airport_schema(self):
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

        logging.info("Load in some test data for IATA values")
        test_data_path = os.path.join(
            "tests", "backend_tests", "data", "iata_values.json"
        )
        with open(test_data_path) as f:
            test_data = json.load(f)

        iata_values = test_data["iata"]

        logging.info("Create the schema")
        airport_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "type": {"type": "string"},
                "attributes": {
                    "type": "object",
                    "properties": {
                        "iata": {"type": "string"},
                        "icao": {"type": "string"},
                        "name": {"type": "string"},
                        "location": {"type": "string"},
                        "country": {"type": "string"},
                        "latitude": {"type": "string"},
                        "longitude": {"type": "string"},
                        "altitude": {"type": "number"},
                        "timezone": {"type": "string"},
                    },
                },
            },
        }

        logging.info(f"Validating IATA values: {iata_values}")

        for iata in iata_values:
            response = airports.get_airport_by_iata(iata, token)
            assert (
                response.status_code == 200
            ), f"Failed to fetch airport {iata}, status {response.status_code}"

            single_airport = response.json()["data"]
            validate(instance=single_airport, schema=airport_schema)
