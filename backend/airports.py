from api.client import Get


class Airports:
    def __init__(self, session=None):
        self.get = Get("https://airportgap.com/api", session=session)

    def get_all_airports(self, token, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token}"
        return self.get.request("/airports", headers=headers)

    def get_airport_by_iata(self, iata, token, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token}"
        return self.get.request(f"/airports/{iata}", headers=headers)
