import requests


class Get:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = (
            session  # Use session if provided, otherwise use direct requests.
        )

    def request(self, endpoint, params=None, headers=None):
        """
        Sends a GET request to the specified endpoint.

        :param endpoint: API endpoint to send the request to.
        :param params: Query parameters as a dictionary (optional).
        :param headers: Headers as a dictionary (optional).
        :return: Response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if self.session:
            return self.session.get(url, params=params, headers=headers)
        else:
            return requests.get(url, params=params, headers=headers)


class Post:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = (
            session  # Use session if provided, otherwise use direct requests.
        )

    def post_with_json_payload(self, endpoint, json=None, headers=None):
        """
        Sends a POST request to the specified endpoint.

        :param endpoint: API endpoint to send the request to.
        :param data: Form data as a dictionary (optional).
        :param json: JSON data as a dictionary (optional).
        :param headers: Headers as a dictionary (optional).
        :return: Response object.
        """
        if self.session is not None:
            return self.session.post(
                f"{self.base_url}/{endpoint}", json=json, headers=headers
            )
        else:
            return requests.post(
                f"{self.base_url}/{endpoint}", json=json, headers=headers
            )
