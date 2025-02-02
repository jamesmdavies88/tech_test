from api.client import Get, Post


class Airports:
    def __init__(self, session=None):
        self.get = Get("https://airportgap.com/api", session=session)
        self.post = Post("https://airportgap.com/api", session=session)

    def get_all_airports(self, token, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token}"
        return self.get.request("/airports", headers=headers)

    def get_airport_by_iata(self, iata, token, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token}"
        return self.get.request(f"/airports/{iata}", headers=headers)

    def get_distance_between_iata(self, iata_one, iata_two, token, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token}"
        payload = {"from": iata_one, "to": iata_two}
        return self.post.post_with_json_payload(
            f"/airports/distance", payload, headers=headers
        )
